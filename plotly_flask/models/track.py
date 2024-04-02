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
        
# from dataclasses import dataclass

# @dataclass
# class Track:
#     id: str
#     name: str
#     image: str = None
#     url: str = None
#     popularity: int
#     artist_id: str
#     artist_name: str
#     playlist_id: str

    
#     @classmethod
#     def from_dict(cls, track:dict):
#         return cls(track["track_id"],
#                    track["track_name"]
#                    )