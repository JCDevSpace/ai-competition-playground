#!/bin/bash

for i in {1..10}
do
   if [ -f "./${i}-in.json" ]; then
     echo "./${i}-in.json already exists"
   else
     touch "./${i}-in.json"
   fi
done


for i in {1..10}
do
   if [ -f "./${i}-out.json" ]; then
     echo "./${i}-out.json already exists"
   else
     touch "./${i}-out.json"
   fi
done