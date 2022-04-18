import pandas as pd
import matplotlib.pyplot as plt

import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# PART ONE----------------- housekeeping aka merging json files into dataframe

# converting json files into a CSV with pandas varies depending on length of streaming history

df0 = pd.read_json('./history/StreamingHistory0.json')
df1 = pd.read_json('./history/StreamingHistory1.json')
df2 = pd.read_json('./history/StreamingHistory2.json')
df3 = pd.read_json('./history/StreamingHistory3.json')
df4 = pd.read_json('./history/StreamingHistory4.json')
df5 = pd.read_json('./history/StreamingHistory5.json')
df6 = pd.read_json('./history/StreamingHistory6.json')
df7 = pd.read_json('./history/StreamingHistory7.json')
df8 = pd.read_json('./history/StreamingHistory8.json')


# making one dataframe for all of the listening dataframes

df = pd.concat([df0, df1, df2, df3, df4, df5, df6, df7, df8])
df.to_csv('streamingHistory.csv', index=False)
result = pd.read_csv('streamingHistory.csv')


# nmake new dataframe with top 100 - track and artist
music_history = result.drop(['endTime', 'msPlayed'], axis=1)
sorted_music = music_history.value_counts().head(100)

tuple_list = sorted_music.index.tolist()
music_count = sorted_music.tolist()


listed_tracks = []
for index, pair in enumerate(tuple_list):
    listed_tracks.append(f"{pair[1]}")


# PART TWO --------------------------- creating graph of top 100 tracks

# customizing the graph
titlefont = {'fontname': 'Arial Rounded MT Bold'}
mainfont = {'fontname': 'Arial Narrow'}
green_color = '#1DB954'
black_color = '#191414'
# a graph of top 100 tracks and number of times listened to


plt.figure(facecolor="#C1E1C1")
plt.bar(listed_tracks, music_count, color=green_color)
plt.xticks(rotation='vertical', **mainfont, color=black_color)
plt.title('Top 100 Tracks', **titlefont, color=black_color, fontweight='bold')
plt.xlabel('Artist, Track', **titlefont, color=black_color, fontweight='bold')
plt.ylabel('Number of Times Played', **titlefont, color=black_color, fontweight='bold')

plt.subplots_adjust(left=0.1, right=0.9, bottom=0.4, top=0.9)
plt.show()






# PART THREE -------- creating playlist of top [enter_number e.g. 100] available tracks that you've listened to


# create list of dictionaries with song info (artistName and trackName)

top_tracks = []
for index, pair in enumerate(tuple_list):
    item = {
        'artistName': pair[0],
        'trackName': pair[1]
    }
    top_tracks.append(item)



# setting up to use spotify API

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = "https://example.com"
OAUTH_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-public",
        redirect_uri=REDIRECT_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

# creating new user
user_id = sp.current_user()["id"]


# get track uris
track_uris = []
for item in top_tracks:
    index = top_tracks.index(item)
    result = sp.search(q=f"track: {top_tracks[index]['trackName']} artist: {top_tracks[index]['artistName']}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        track_uris.append(uri)
    except IndexError:
        print(f"{top_tracks[index]['trackName']} is not available on Spotify. Skipped")



# make playlist
playlist = sp.user_playlist_create(user=user_id, name="Unoffically Undressed Test", public=True)


# adding tracks to playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=track_uris)





