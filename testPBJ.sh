#!/bin/bash

if [ -z "$1" ]; then
 echo "Please supply machine name."
 exit
fi

machine=$1
sharepath="$HOME/PBJ/tmp/$machine"

mkdir -p $sharepath
touch "$HOME/PBJ/tmp/$machine/$machine.txt"
