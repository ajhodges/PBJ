#!/bin/bash 

if [ -z "$1" ]; then
 echo "Please supply username."
 exit
fi

USER=$1
MACHINECOUNT=0
machines=( )

#10 dragons
COUNTER=1
while [  $COUNTER -lt 12 ]; do
 machines[$MACHINECOUNT]=dragon$COUNTER
 let COUNTER=COUNTER+1
 let MACHINECOUNT=MACHINECOUNT+1
done

for machine in "${machines[@]}";
do
 ssh -o "StrictHostKeyChecking no" -o "ConnectTimeout=2" $USER@$machine.cs.clemson.edu "cd PBJ ; nohup ./testPBJ.sh $machine && exit" &
 sleep 5
done
