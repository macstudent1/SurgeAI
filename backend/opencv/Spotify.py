import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import time  # For checking token expiration
import json


scope = "user-library-read"
client_id = "5d5f1dcb76c346448c29ac3cb09eaa58"
client_secret = "ef58d49ea1fd476d969064a09eff6944"
redirect_uri = "http://localhost:8080"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id="5d5f1dcb76c346448c29ac3cb09eaa58",
    client_secret="ef58d49ea1fd476d969064a09eff6944",
    redirect_uri="http://localhost:8080"))

'''results= sp.current_user_saved_tracks(limit=1)
print(results)
print( results["items"][0]["track"]["artists"][0]["id"])'''

import requests
access_token = "BQB0HcCPebRS6ed8n6n5Z1PGCTsz-_2uUaa4r96n2iCtpW5mf2q46shkYEm3QQ1T_502UGWbI26xY7OvFQG0OnDmnHpVwmmTNzsgZCLz4KVKbYnKJaAZGlwYEa4bkPTbIXjRkzO55WSH3e4axF-HVCruw4BjjJavskq4sMV-RO7HT1w0r7H335nAFf296HadF1PGop_0NjwTyFu2rT_0IGM16ffmArI-F5dNcYJtXtWbS4uFtGkBLQ"
refresh_token = "AQANCEUoBvP_ldIzhagUWaY4DGRiQL19kQAICdyc97edy20EsKrPzLepg09CYsqSBsf2FSjmtCv395gbW-1nFuFZL_PGHx8FzPI1lasa-OBhAL8o8xWWJ7yqghc3NfAEzSA"
expires_at = time.time() + 3600  # Set expiration to one hour from now

# Function to refresh the access token
def load_tokens():
    try:
        with open('.cache', 'r') as f:
            data = json.load(f)
            return data["access_token"], data["refresh_token"], data["expires_at"]
    except FileNotFoundError:
        return None, None, None

# Function to save new tokens to cache
def save_tokens(access_token, refresh_token, expires_at):
    with open('.cache', 'w') as f:
        json.dump({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at
        }, f)

def refresh_access_token():
    global access_token, expires_at
    refresh_url = "https://accounts.spotify.com/api/token"
    auth = (client_id, client_secret)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    # Make the request to refresh the access token
    response = requests.post(refresh_url, headers=headers, data=data, auth=auth)
    print(response.json())

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        expires_in = token_data["expires_in"]
        expires_at = time.time() + expires_in  # Update expiration time
        print("Token refreshed successfully!")
        save_tokens(access_token, refresh_token, expires_at)  # Save to cache
    else:
        print("Error refreshing token:", response.status_code, response.text)


# Call the function to refresh token if necessary
def check_and_refresh_token():
    global access_token, refresh_token, expires_at
    if time.time() >= expires_at:  # Token expired
        print("Token expired, refreshing...")
        refresh_access_token()
    else:
        print("Token is still valid.")

# Load the tokens from cache file
access_token, refresh_token, expires_at = load_tokens()

if access_token and refresh_token and expires_at:
    check_and_refresh_token()  # Ensure we have a valid token before proceeding
else:
    print("No tokens found, please authenticate again.")

# Example API call to get saved tracks
results = sp.current_user_saved_tracks(limit=1)
'''print(results)'''
artist_id = []
artist_url = []
response = []
artist_data = []
results = sp.current_user_saved_tracks(limit=10)['items']
RecommendedSongs=[]
for i in range(len(results)) : 
    artist_data.append(results[i]["track"]["artists"][0]["id"])
    artist_id.append(results[i]["track"]["artists"][0]["id"])
    response = sp.artist(artist_id[i])
    print(response['genres'])
    




#Song Reccomendations
#UserID, Song Name, Song URL, Album Photo, Artist Name, Artist URL, Genre

