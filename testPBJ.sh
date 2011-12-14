#!/bin/bash
#run dummy.py with a sharepath that corresponds to the name of the machine (passed in as an argument)

#if [ -z "$1" ]; then
# echo "Please supply machine name."
# exit
#fi

machine=node$PBS_NODENUM
sharepath="tmp/$machine"

cd "$HOME/PBJ"

mkdir -p "$sharepath"
touch "$sharepath/$machine.txt"

sleep $PBS_NODENUM

nohup python dummy.py $sharepath
