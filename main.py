import random
from flask import Flask, render_template, request, redirect, url_for
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import flask_bootstrap
from keys import *

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENTID,
                                               client_secret=CLIENTSECRET,
                                               redirect_uri=SIU,
                                               scope=SCOPE))

app = Flask(__name__)
flask_bootstrap.Bootstrap(app)


def user_playlist_tracks_full(playlist_id=playlist_id, fields=None, market=None):
    # first run through also retrieves total no of songs in library
    response = sp.user_playlist_tracks(sp.current_user(), playlist_id, fields=fields, limit=100, market=market)
    results = response["items"]

    # subsequently runs until it hits the user-defined limit or has read all songs in the library
    while len(results) < response["total"]:
        response = sp.user_playlist_tracks(
            sp.current_user(), playlist_id, fields=fields, limit=100, offset=len(results), market=market
        )
        results.extend(response["items"])
        p = []
        for k in results:
            p.append({"name": k['track']['name'], "id": k['track']['id']})
        return p


def play_song(song_id):
    device_id = sp.devices()['devices'][0]['id']
    sp.start_playback(device_id=device_id, uris=["spotify:track:" + song_id])


app.jinja_env.globals.update(play_song=play_song)





@app.route('/')
def index():
    p = user_playlist_tracks_full()
    o = len(p)
    u = random.randint(0, o)
    i = p[u]
    return render_template('index.html', song=i)

@app.route("/cmd")
def cmd():
    x = request.args
    ids = x['id']
    play_song(ids)
    return redirect('/')

app.run(host='127.0.0.1', port=8080)
