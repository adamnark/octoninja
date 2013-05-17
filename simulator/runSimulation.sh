#!/bin/bash

for GPX in `ls gpx | grep *.gpx` ;  do
	py simulator.py $GPX ${GPX:0:1} &
done
