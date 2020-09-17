#!/bin/bash

for i in {1..10}
do
   if [ -f "../Test/${i}-in.json" ]; then
     echo "../Test/${i}-in.json already exists"
   else
     touch "../Test/${i}-in.json"
   fi
done


for i in {1..10}
do
   if [ -f "../Test/${i}-out.json" ]; then
     echo "../Test/${i}-out.json already exists"
   else
     touch "../Test/${i}-out.json"
   fi
done
