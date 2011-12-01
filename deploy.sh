#!/bin/bash 

if [ -z "$1" ]; then
 echo "Please supply username."
 exit
fi

USER=$1
MACHINECOUNT=0
machines=( )

#24 dragons
COUNTER=1
while [  $COUNTER -lt 25 ]; do
 machines[$MACHINECOUNT]=dragon$COUNTER
 let COUNTER=COUNTER+1
 let MACHINECOUNT=MACHINECOUNT+1
done

#27 frogs
COUNTER=1
while [  $COUNTER -lt 28 ]; do
 machines[$MACHINECOUNT]=frog$COUNTER
 let COUNTER=COUNTER+1 
 let MACHINECOUNT=MACHINECOUNT+1
done

#22 geckos
COUNTER=1
while [  $COUNTER -lt 23 ]; do
 machines[$MACHINECOUNT]=gecko$COUNTER
 let COUNTER=COUNTER+1 
 let MACHINECOUNT=MACHINECOUNT+1
done

for machine in "${machines[@]}";
do
 ssh -o "StrictHostKeyChecking no" $USER@$machine.cs.clemson.edu 'nohup bash -s' < testPBJ.sh $machine &
done
