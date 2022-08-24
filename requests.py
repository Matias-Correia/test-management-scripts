import pandas as pd

requests = pd.read_excel('requests.xlsx').values.tolist()
sends = pd.read_excel('sends.xlsx').values.tolist()

newRequests = []

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

for r in requests:
    for s in sends:
        if r[0] == s[0] and r[1] == s[2] and r[2] == s[1]:
            newRequests.append(r)
            break

save_to_excel(newRequests,"newRequests")