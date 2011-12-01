#!/bin/bash

if [ -z "$1" ]; then
 echo "Please supply machine name."
 exit
fi

machine=$1
sharepath="tmp/$machine"

mkdir -p "$HOME/PBJ/$sharepath"
touch "$HOME/PBJ/$sharepath/$machine.txt"

python $HOME/PBJ/dummy.py $sharepath &
