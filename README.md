# Playlist Curator
Welcome to the Playlist Curator repository, a place to analyze, curate and tweak your Spotify playlists!

## Description
Here're some of the project's best features:

   - Playlist Curator
   - Dashboard with playlist analytics

TBD 

Other things to include:

    Technology stack: Indicate the technological nature of the software, including primary programming language(s) and whether the software is intended as standalone or as a module in a framework or other ecosystem.
    Status: Alpha, Beta, 1.1, etc. It's OK to write a sentence, too. The goal is to let interested people know where this project is at. This is also a good place to link to the CHANGELOG.
    Links to production or demo instances
    Describe what sets this apart from related-projects. Linking to another doc or page is OK if this can't be expressed in a sentence or two.


## Dependencies
Please see the project `toml` file for a list of Python package dependencies. Additionally this project makes use of the Spotify API via the `Spotipy` library. For more information on how that can be setup please visit the official [Spotipy documentation](https://spotipy.readthedocs.io/en/2.22.1/).

## Installation
`source env/bin/activate`

Install the required packages to run the project from the provided `requirements.txt` file: 
Install the required packages to run the project from the provided `pyproject.toml` file: 

`python3 -m pip install -r requirements.txt`
`python3 -m pip install -e .[dev]`

For troubleshooting visit the official Python docs on how to set up a [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

## How to run
### Backend
Assuming fastapi is installed, then simply running the `app/main.py` will work. That script will start the uvicorn server and connect the routes the fastapi app.

### Frontend
Ensure npm & node.js are installed. Navigate to the `ui/` directory: 
    - `npm install` - to install project dependencies
    - `npm run dev`

## Configuration
Following the structure of the `compose.yaml`, the frontend is dependent on the backend. Ensure spotify client id, secret and redirect URI are available to the project as environment variables. You can acquire those from the Spotify Dashboard for developers. 

## Usage
Ensure you have docker installed. Navigate to the root of the project and `docker compose up`. See Docker documentation for further troubleshooting, should you have issues. 

## How to test the software
Tests for basic functionality of the `curator service` can be found in the `root/curator_service/tests` directory.

## Known issues
Long way to go still. 

## Getting help
Instruct users how to get help with this software; this might include links to an issue tracker, wiki, mailing list, etc.

Example
If you have questions, concerns, bug reports, etc, please file an issue in this repository's Issue Tracker.

## Contributing guide
For information and how to set up a development environment, see the Installation steps above.

This project follows the Github Flow workflow with tags and releases for published versions of our components; when working on the codebase create descriptive branch names (e.g. feature/cool_feature_x, hotfix/flux_capacitor, issue/123, etc.).

When your changes are complete then create a Pull Request ensuring that your branch is up-to-date with the source branch and that code changes are covered by tests and that the full test suite passes.

## Open source licensing info
    TERMS
    LICENSE
    CFPB Source Code Policy

## Credits and references
    Projects that inspired you
    Related projects
    Books, papers, talks, or other sources that have meaningful impact or influence on this project


## Goal structure

```
\curator_service
    \tests
    \app
    Dockerfile
\ui
    \tests
    \src
    Dockerfile
LICENSE
README.md
pyproject.toml
compose.yaml
```