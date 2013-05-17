#!/bin/bash

for GPX in `ls gpx | grep gpx` ;  do
	echo simulator.py $GPX ${GPX:0:1}
	python simulator.py gpx/$GPX ${GPX:0:1} &
done
