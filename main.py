from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv('.env')
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = "https://example.com/callback/"

user_pick = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
SITE_URL = f"https://www.billboard.com/charts/hot-100/{user_pick}/"
response = requests.get(SITE_URL)
billboard_page = response.text

soup = BeautifulSoup(billboard_page, "html.parser")

titles = soup.select(".o-chart-results-list__item .c-title")
# get all the song titles:
title_list = [title.text.strip() for title in titles]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=SPOTIFY_REDIRECT_URI,
                                               scope="playlist-modify-private",
                                               cache_path="token.txt",
                                               show_dialog=True))

user_id = sp.current_user()["id"]

song_uris = []
year = user_pick.split("-")[0]
for song in title_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"This {song} doesn't exist in Spotify")


playlist = sp.user_playlist_create(user=user_id, name=f"Top 100 {user_pick} Billboard", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)