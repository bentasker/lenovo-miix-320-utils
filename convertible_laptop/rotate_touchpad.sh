#!/bin/bash

coords="0 1 0 -1 0 1 0 0 1"
if [ "$1" = "portrait" ]
then
  coords="1 0 0 0 1 0 0 0 1"
fi

id=`xinput list | grep FTSC1000 | grep pointer | grep -o -P 'id=([0-9]+)' | grep -o -P '([0-9]+)'`

xinput set-prop $id "Coordinate Transformation Matrix" $coords



