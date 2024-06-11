# Recommendation endpoint

The spotify API provides an endpoint for recommendations. This document serves to allow us to make notes on which of the attributes for recommendation are relevant and useful for the API being developed for curation.

## Spotify recommendation rules

### Seeds
- Users can specify target seeds
    - Seeds can be:
        - "seed_tracks" : Then these would be IDs of tracks to use for seeding.
        - "seed_artists": Then these would be IDs of artists to use for seeding.
        - "seed_genres" : Then these would be the names of genres to use for seeding.

- Rules:
    - Up to 5 of any combination of seeds is possible.
        - If someone does more than 5, we'll need an approach to do a nice aggregating between the chunks available.


### Attributes:

- accousticness
    - number, range 0-1
- danceability
    - number, range 0-1
- duration_ms
    - integer
- energy
    - number, range 0-1
- instrumentalness
    - number, range 0-1
- key
    - integer, range 0-11 (lol)
- liveness
    - number, range 0-1
- loudness
    - number
    - Question:
        - I wonder if this is in decibels. The docs don't say.
- mode
    - integer, 0/1
- popularity
    - integer, range 0-100
- speechiness
    - number, range 0-1
- tempo
    - number
    - Definition: How many BPM do we want
- time_signature
    - integer
    - Question:
        - Unclear what is meant by allowable values of the time signature.
- valence
    - number, range 0-1

## Curator

This section will select the attributes that the curator will support in an initial beta version.

### Supported attributes 

#### Supported in MVP

- accousticness
    - number, range 0-1
- danceability
    - number, range 0-1
- energy
    - number, range 0-1
- instrumentalness
    - number, range 0-1
- liveness
    - number, range 0-1
- popularity
    - integer, range 0-100      => also just do 0-1 and if "name == popularity" then multiply by 100.
- speechiness
    - number, range 0-1
    
#### Would like eventually supported

- duration_ms
    - integer
- tempo
    - number
    - Definition: How many BPM do we want
- loudness
    - number

### Not intended for support soon

These attributes are included to explicitly state which ones likely won't be parameters we will include in the curator release any time soon. Part of the reason is simply the complexity of needing to clarify to the user what these attributes mean. 

- key
    - integer, range 0-11 (lol)
- mode
    - integer, 0/1
- time_signature
    - integer
    - Question:
        - Unclear what is meant by allowable values of the time signature.
- valence
    - number, range 0-1
