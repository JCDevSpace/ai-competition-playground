#!/bin/bash

for i in {1..10}
do
  result=$(../xjson < "./${i}-in.json" | diff - "./${i}-out.json")
  if [ -z "$result" ]; then
  	echo "Test ${i} passed."
  else
  	echo "Test ${i} failed. Diff: "
  	echo "$result"
  fi
done
