#!/bin/bash

# Remove existing output files to ensure the pipeline creates them
rm -f ../data/carbon_dioxide.db ../data/surface_temperature.db

python3 project/code.py

# Check if the output files exist and are newly created
if [[ -f "../data/carbon_dioxide.db" && -f "../data/surface_temperature.db" ]]; then
    echo "Test passed: Output files exist."
    
    # Run the Python tests to check the contents of the files
    python3 test_pipeline.py

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
