#!/bin/bash

for i in {1..13}
do
  result=$(../xjson < "../Test/${i}-in.json" | diff - "../Test/${i}-out.json")
  if [ -z "$result" ]; then
  	echo "Test ${i} passed."
  else
  	echo "Test ${i} failed. Diff: "
  	echo "$result"
  fi
done
