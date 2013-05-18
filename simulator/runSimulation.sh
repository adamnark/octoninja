#!/bin/bash

DIR=$1
#echo $DIR
for GPX in `ls $1 | grep gpx` ;  do
	echo "simulator.py $DIR/$GPX ${GPX:0:1}"
	python simulator.py $DIR/$GPX ${GPX:0:1} &
done
