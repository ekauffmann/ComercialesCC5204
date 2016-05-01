#!/bin/bash

FRAMES=(10 20 30)
ZONES=(1 2 4)
BINS=(16 32 64)
TOLERANCE=(50 80)

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
python compare.py

for frame in "${FRAMES[@]}"
do
    for zone in "${ZONES[@]}"
    do
        for bin in "${BINS[@]}"
        do
            for tol in "${TOLERANCE[@]}"
            do
                echo $frame $zone $zone $bin $tol
                python match.py $frame $zone $zone $bin $tol
            done
        done
    done
done