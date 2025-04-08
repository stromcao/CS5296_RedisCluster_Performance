#!/bin/bash
# get the current timestamp
timestamp=$(date +%s%N)
redis-cli SET sync_test $timestamp
echo "Master write time: $timestamp"
