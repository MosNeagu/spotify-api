import json
import requests
from secret import SPOTIFY_ID, SPOTIFY_TOKEN


# for every playlist, generate a new similar new one

# 1. get all playlists
# 2. get all songs from a playlist
# 3. create a list of similar songs
# 4. create a new playlist and add the new songs


# todo: fix empty playlist bug

class SpotifyTasks:

    def __init__(self):
        self.user_id = SPOTIFY_ID
        self.user_token = SPOTIFY_TOKEN
        self.artists_list = []

    def similar_songs(self, song):
        artist_id = song["track"]["album"]["artists"][0]["id"]

        # find similar artists
        end_point = "https://api.spotify.com/v1/artists/{id}/related-artists".format(id=artist_id)
        response = requests.get(
            end_point,
            headers={
                "Authorization": "Bearer {}".format(self.user_token)
            }
        )
        chosen_artist = "!"
        similar_artists = response.json()
        for artist in similar_artists["artists"]:
            if artist["id"] not in self.artists_list:
                self.artists_list.append(artist["id"])
                chosen_artist = artist["id"]
                break

        print(song["track"]["album"]["artists"][0]["name"])
        if chosen_artist == "!":
            print("aici")
            print(song["track"]["album"]["artists"][0]["name"])
            return

        end_point = "https://api.spotify.com/v1/artists/{id}/top-tracks?market={market}".format(id=chosen_artist,
                                                                                                market="RO")
        response = requests.get(
            end_point,
            headers={
                "Authorization": "Bearer {}".format(self.user_token)
            }
        )
        songs = response.json()
        # returns the id of a new song to be added in the playlist
        return songs["tracks"][0]["uri"]

    def create_playlist(self, name, songs):
        end_point = "https://api.spotify.com/v1/users/{user_id}/playlists".format(user_id=self.user_id)
        request_query = json.dumps({
            "name": name,
            "public": False,
        })

        response = requests.post(
            end_point,
            data=request_query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.user_token)
            }
        )
        new_playlist = response.json()
        new_playlist = new_playlist["id"]

        # created new playlist, now add the songs to it
        end_point = "https://api.spotify.com/v1/playlists/{playlist_id}/tracks".format(playlist_id=new_playlist)
        # print(songs)

        request_query = json.dumps({
            "uris": songs
        })

        response = requests.post(
            end_point,
            data=request_query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.user_token)
            }
        )
        response = response.json()

    def analyze_playlist(self, playlist):
        new_playlist = 'Based on ' + playlist["name"]

        # get every song
        end_point = "https://api.spotify.com/v1/playlists/{playlist_id}/tracks".format(playlist_id=playlist["id"])
        response = requests.get(
            end_point,
            headers={
                "Authorization": "Bearer {}".format(self.user_token)
            }
        )
        songs_list = []
        songs = response.json()
        # send every song to be analyzed
        for i in songs["items"]:
            songs_list.append(self.similar_songs(i))

        self.create_playlist(new_playlist, songs_list)

    def get_playlists(self):
        end_point = "https://api.spotify.com/v1/me/playlists"
        response = requests.get(
            end_point,
            headers={
                "Authorization": "Bearer {}".format(self.user_token)
            }
        )
        playlists = response.json()
        for i in playlists["items"]:
            self.analyze_playlist(i)
            self.artists_list = []
        # every playlist has an ID


eu = SpotifyTasks()
eu.get_playlists()
