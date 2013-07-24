#!/bin/bash

if [ -d $1 ] ; then
	DIR=$1
else
	DIR=gpx
fi

#DIR=$1
echo "DIR = $DIR"
for GPX in `ls $1 | grep gpx` ;  do
	echo "simulator.py $DIR/$GPX ${GPX:0:1}"
	python simulator.py $DIR/$GPX ${GPX:0:1} &
done
