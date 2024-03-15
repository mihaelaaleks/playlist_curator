class Track:
    def __init__(self, 
                 track_name, 
                 track_id,
                 track_url,
                 track_popularity,
                 image,
                 artist_name,
                 album_id
                 ):
        self.name = track_name
        self.id = track_id
        self.image = image
        self.url = track_url
        self.popularity = track_popularity
        self.artist = artist_name
        self.album_id = album_id