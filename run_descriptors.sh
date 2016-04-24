#!/bin/bash

FRAMES=(10 15 30)
ZONES=(1 2 4)
BINS=(32 64)

for frame in "${FRAMES[@]}"
do
    for zone in "${ZONES[@]}"
    do
        for bin in "${BINS[@]}"
        do
            echo $frame $zone $zone $bin
            python describe.py $frame $zone $zone $bin
        done
    done
done
