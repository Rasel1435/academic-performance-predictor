#!/bin/bash

# Check if an environment is already active 
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Using currently active environment: $VIRTUAL_ENV"
    uvicorn src.web.api:app --reload
else
    # If not active, try to find and activate the local one
    VENV_DIR="mySCS-linux"
    if [ -d "$VENV_DIR" ]; then
        echo "Activating local environment..."
        source $VENV_DIR/bin/activate
        uvicorn src.web.api:app --reload
    else
        echo "Error: Virtual environment not found and none is active."
        echo "Please activate your environment manually or fix VENV_DIR in this script."
        exit 1
    fi
fi

# ./run.sh