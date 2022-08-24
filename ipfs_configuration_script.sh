#!/bin/sh

ipfs init
ipfs bootstrap rm all
ipfs bootstrap add /ip4/10.172.0.2/tcp/4001/ipfs/12D3KooWRaWpo2C4CpDYSBJW2CxqG8DJFgmidSYiKUgrziBdY8jD

tmpfile=$(mktemp)
jq '.Addresses |= . + {"API": "/ip4/'$1'/tcp/5001" }' .ipfs/config > ${tmpfile}
cat ${tmpfile} > .ipfs/config
rm -f ${tmpfile}
tmpfile2=$(mktemp)
jq '.Internal |= . + {"Bitswap":{"TaskWorkerCount": null,"EngineBlockstoreWorkerCount": null,"EngineTaskWorkerCount": null,"MaxOutstandingBytesPerPeer": null,"ProviderSelectionMode": '$2',"ServerAddress": "'$3'","SessionAvgLatencyThreshold": '$4'} }' .ipfs/config > ${tmpfile2} 
cat ${tmpfile2} > .ipfs/config
rm -f ${tmpfile2}
