# Spotify Analyzer Tool

To get started set up a virtual python environment in the root folder of the project: 

`python3 -m venv env`

Activate the environment: 

`source env/bin/activate`

Install the required packages to run the project from the provided `requirements.txt` file: 

`python3 -m pip install -r requirements.txt`

For troubleshooting visit the official Python docs on how to set up a [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

# Setting up Spotipy

This project makes use of the Spotipy library. To set up making requests with the library the following environment variables will need to be included in the environments `activate` file.

Open the `activate` file using any IDE or text editor and add the following lines under `export PATH`: 

```
SPOTIPY_CLIENT_ID="ID"
SPOTIPY_CLIENT_SECRET="SECRET"
SPOTIPY_REDIRECT_URI="http://localhost:8888/callback"

export SPOTIPY_CLIENT_ID
export SPOTIPY_CLIENT_SECRET
export SPOTIPY_REDIRECT_URI
```

Replace the ID and SECRET variables with the assigned from the Spotify API dashboard. 
Ensure that the redirect URI is the same. 
