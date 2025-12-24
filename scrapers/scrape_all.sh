#!/bin/bash

for file in *.py; do
    [ -e "$file" ] || continue

    if [ "$file" != "run_all.py" ]; then
        echo "Running $file..."
        python "$file"
    fi
done