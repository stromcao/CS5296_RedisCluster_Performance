#!/bin/bash
# until get the key value
while true; do
    # get the sync_test value
    value=$(redis-cli GET sync_test)
    if [ "$value" != "" ]; then
        # record current time
        current=$(date +%s%N)
        # calculate the delay
        delay=$(( (current - value) / 1000000 ))
        echo "Replication delay: $delay ms"
        break
    fi
    # pause 0.01sec and retry
    sleep 0.01
done
