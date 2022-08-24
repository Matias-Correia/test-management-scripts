from sqlalchemy import create_engine
import pymysql
import pandas as pd
import itertools
import threading

requests = []
sends = []
dupsR = []
dupsS = []

def is_record_in_requests(record,requestLatency):
  if len(requests) == 0:
    requests.append((record[0],record[1],record[2],record[3],requestLatency.total_seconds() * 1000.0))
    #print("Requests added")
  else:  
    for item in requests:
      if item[0] == record[0] and item[1] == record[1] and item[2] == record[2]:  
        if item[3] <= record[3]:
          #print("DupsR added")
          dupsR.append((record[0],record[1],record[2],record[3],requestLatency.total_seconds() * 1000.0))
          break
        elif item[3] > record[3]:
          requests.remove(item)
          dupsR.append(item)
          #print("Substitute")
          requests.append((record[0],record[1],record[2],record[3],requestLatency.total_seconds() * 1000.0))
          break
    else:
      requests.append((record[0],record[1],record[2],record[3],requestLatency.total_seconds() * 1000.0))
    #print("Requests added")

def is_record_in_sends(record,sendLatency):
  if len(sends) == 0:
    sends.append((record[0],record[1],record[2],record[3],sendLatency.total_seconds() * 1000.0))
    #print("Sends added")
  else:
    for item in sends:
      if item[0] == record[0] and item[2] == record[2]:  
        if item[3] <= record[3]:
          dupsS.append((record[0],record[1],record[2],record[3],sendLatency.total_seconds() * 1000.0))
          #print("DupsS added")
          break
        elif item[3] > record[3]:
          sends.remove(item)
          #print("Substitute")
          dupsS.append(item)
          sends.append((record[0],record[1],record[2],record[3],sendLatency.total_seconds() * 1000.0))
          break
    else:
      sends.append((record[0],record[1],record[2],record[3],sendLatency.total_seconds() * 1000.0))
    #print("Sends added")

def save_to_excel(liist,name):
  filename = name + ".xlsx"
  r1 = []
  r2 = []
  r3 = []
  r4 = []
  r5 = []
  for x in liist:
    r1.append(x[0])
    r2.append(x[1])
    r3.append(x[2])
    r4.append(x[3])
    r5.append(x[4])
  col1 = "Block ID"
  col2 = "Sender ID"
  col3 = "Receiver ID"
  col4 = "Timestamp"
  col5 = "Latency"
  data = pd.DataFrame({col1:r1,col2:r2,col3:r3,col4:r4,col5:r5})
  data.to_excel(filename, sheet_name=name, index=False)

if __name__ == "__main__":
  #mydb = pymysql.connect(
  #host="34.118.36.194",
  #user="root",
  #password="root",
  #database="logs"
  #)
  sqlEngine       = create_engine('mysql+pymysql://root:root@localhost/logs', pool_recycle=3600)
  dbConnection    = sqlEngine.connect()

  #mycursor = mydb.cursor()

  #mycursor.execute("SELECT * FROM test_logs")
  #threads = list()

  for i in (pd.read_sql('SELECT * FROM test_logs order by BlockID', dbConnection, chunksize=100000)):
    for x, y in itertools.product(i.values.tolist(), repeat=2):

  #myresult = pd.read_sql('SELECT * FROM test_logs order by BlockID', dbConnection).values.tolist()
  #for x in myresult:
  #  for y in myresult:  
      #if x[1] != y[1] and myresult.index(y) > myresult.index(x):
      #  break
      #elif x[1] != y[1] and myresult.index(y) < myresult.index(x):
      #  continue
      if x[1] == y[1] and x[2] == y[3] and x[3] == y[2] and x[6] != None and y[4] != None:
        requestLatency = y[4] - x[6]
        if (requestLatency.total_seconds() * 1000.0) > 0:
          #th = threading.Thread(target=is_record_in_requests, args=((x[1],x[2],x[3],y[4]),requestLatency ))
          #threads.append(th)
          #th.start()
          is_record_in_requests((x[1],x[2],x[3],y[4]),requestLatency)
      elif x[1] == y[1] and x[2] == y[2] and x[3] == y[3] and x[4] != None and y[5] != None:
        sendLatency = y[5] - x[4]
        if (sendLatency.total_seconds() * 1000.0) > 0:
          #th = threading.Thread(target=is_record_in_sends, args=((x[1],x[2],x[3],y[5]),sendLatency ))
          #threads.append(th)
          #th.start()
          is_record_in_sends((x[1],x[2],x[3],y[5]),sendLatency)
  #for index, thread in enumerate(threads):
  #  thread.join()
  print("-----Saving Requests-----")
  save_to_excel(requests,"requests")
  print("-----Saving Sends-----")
  save_to_excel(sends,"sends")
  print("-----Saving DupsR-----")
  save_to_excel(dupsR,"dupsR")
  print("-----Saving DupsS-----")
  save_to_excel(dupsS,"dupsS")



