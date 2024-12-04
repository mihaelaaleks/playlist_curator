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
Please see the project `toml` file for a list of Python package dependencies. This project interacts with the Spotify API via the `Spotipy` library. For more information on how that can be setup, refer to the official [Spotipy documentation](https://spotipy.readthedocs.io/en/2.24.0/).

> Note: The curator requires Spotify API credentials as environment variables. For further information on setting this up refer to the Spotipy library documentation. 

## Installation
### Python
Ensure you have a virtual python environment created and active in the root of the project. For more information on how that can be setup, refer to this [documentation page](https://docs.python.org/3/library/venv.html).

Install the required packages to run the project from the provided `requirements.txt` file: 
Install the required packages to run the project from the provided `pyproject.toml` file: 

`python3 -m pip install -r requirements.txt`
`python3 -m pip install -e .[dev]`

For troubleshooting visit the official Python docs on how to set up a [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

### Vue.js
Ensure you have `Node.js` and `npm` installed. 

1. Navigate to the frontend service directory `root/frontend_service`. 
2. Install dependencies via `npm install`. 


## Getting Started

### Backend
Assuming the required dependencies are met, start the FastAPI through `backend_service/main.py`. That script will start the uvicorn server and connect the routes the fastapi app.

### Frontend
- To start local development server: `npm run dev`
- Create production build: `npm run build`
- Preview production build: `npm run preview`

> Note: If you encounter `'vite' is not recognized` error, ensure you've installed dependencies by running `npm install` first. 
> Note: The frontend service won't display any data unless the backend service is running. 

## Configuration
If the software is configurable, describe it in detail, either here or in other documentation to which you link.

## Usage
Show users how to use the software. Be specific. Use appropriate formatting when showing code snippets.

## How to test the software
If the software includes automated tests, detail how to run those tests.

## Known issues
Document any known significant shortcomings with the software.

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
\backend_service
    .env
    pyproject.toml # maybe this is in backend service?
    \tests
    \data
\frontend_service
    \tests
    \data
LICENSE
README.md
```