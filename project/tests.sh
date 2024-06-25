#!/bin/bash

# Get the absolute path of the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="$SCRIPT_DIR/../data"

# Remove existing output files to ensure the pipeline creates them
rm -f "$DATA_DIR/carbon_dioxide.db" "$DATA_DIR/data/surface_temperature.db"

python3 "$SCRIPT_DIR/code.py"

# Check if the output files exist and are newly created
if [[ -f "$DATA_DIR/carbon_dioxide.db" && -f "$DATA_DIR/surface_temperature.db" ]]; then
    echo "Test passed: Output files exist."
    
    # Run the Python tests to check the contents of the files
    python3 "$SCRIPT_DIR/test_pipeline.py"

    if [[ $? -eq 0 ]]; then
        echo "Test passed: Output files are valid."
        exit 0
    else
        echo "Test failed: Output files are invalid."
        exit 1
    fi
else
    echo "Test failed: Output files do not exist."
    exit 1
fi
