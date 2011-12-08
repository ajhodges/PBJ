#!/bin/bash
#run dummy.py with a sharepath that corresponds to the name of the machine (passed in as an argument)

if [ -z "$1" ]; then
 echo "Please supply machine name."
 exit
fi

machine=$1
sharepath="tmp/$machine"

cd "$HOME/PBJ"

mkdir -p "$sharepath"
touch "$sharepath/$machine.txt"

python dummy.py $sharepath &
