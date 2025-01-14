#!/bin/bash

# Simple loop to create CPU and memory load
for i in {1..999999}; do
    # Create memory load by storing command output in array
    # Add declare -a to properly initialize the array
    declare -a array
    array+=( $(seq 1 1000) )
    
    # Create CPU load with heavy calculations
    for j in {1..1000}; do
        echo "scale=5000; 4*a(1)" | bc -l >/dev/null
    done
    
    # Print progress every 100 iterations
    if [ $((i % 100)) -eq 0 ]; then
        # Add flush to ensure output is displayed
        echo "Completed $i iterations"
        # Force flush the output buffer
        exec 1>&1
    fi
    
    # Clear array to prevent memory overflow
    unset array
done

# Ensure final message is displayed
echo "Process complete"
exec 1>&1
