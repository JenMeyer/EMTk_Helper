#!/usr/bin/env bash

for EMOTION in joy love sadness anger surprise fear
do
	emtk emotions classify -i $1 -p -d sc -e $EMOTION
done
