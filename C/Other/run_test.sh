#!/bin/bash

result=$(../xjson < "../Test/1-in.json" | diff - "../Test/1-out.json")
if [ -z "$result" ]; then
  echo "Test passed."
else
  echo "Test failed. Diff: "
  echo "$result"
fi
