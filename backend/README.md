# Purpose
This is the backend of the project authored by Arunan Gnanasekaran, Trym Gudvangen, and Sebastian Bugge for the hackathon Startcode 2022. The backend makes predictions of the final score of a football minute by minute.

# Setup
## Requirements
The application requires a python version of 3.10 or greater.

## Installation
To install the reqired dependencies follow these steps:
1. Create and activate a fresh python virual enviornment (`virtualenv .venv && source .venv/bin/activate`)
2. Install the dependencies in the requirements.txt file (`pip install -r requirements.txt`)
3. Enjoy and relax

## Preparations
For the backend to work, a trained model is needed. For this to work, one would need to use raw data from the matches. In our case, matches were supplied by Sportradar directly. For the application to run, the matches need to be compliant with the format of the xml files supplied by Sportradar.

Once the data has been collected, put all xml files in a folder in the `matches` directory. A model can be trained on it by changeing the working directory to `sportradar_ml` and running the `forest_reg.py` file. Make sure the folder specified in the main section matches the folder you created with the matches.

## How to run?
Once everything is set up, the backend can be launched using uvicorn by executing the command `python -m uvicorn api.main:app` in the backend root directory.
