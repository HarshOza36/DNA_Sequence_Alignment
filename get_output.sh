#!/bin/bash
# Using this final to run and create output files for us

for i in {1..15..1}
do
  python basic_3.py "datapoints/in"$i".txt" "out_"$i".txt"
done


for i in {1..15..1}
do
  python efficient_3.py "datapoints/in"$i".txt" "out_dnc_"$i".txt"
done