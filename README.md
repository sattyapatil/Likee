# LikeMe

## Clone and Installation

### Clone Rapository

1. `git clone https://github.com/sattyapatil/Likee.git`
2. Then go to the main application folder `cd ./Likee`

### Installation

1. First create virtual env and activate it.
  1. `sudo apt install python3-virtualenv`
  2. `virtualenv -p python3 venv`
  3. `source ./venv/bin/activate`
2. Install all required packages `pip3 install -r requirements.txt`

## Test application
1. Then run this command `pytest`

## Run application
1. Then run this command `uvicorn Application.app:app --reload`

## User Guide

1. After starting application go to the [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
2. We can see all the api documentation here
3. We can test all api endpoints from here
