from typing import List, Dict, Tuple
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import json
from pydantic import BaseModel

# Emotion to genre/musical attributes mapping
EMOTION_MAPPING = {
    "happy": {
        "genres": ["pop", "dance", "disco", "happy", "funk"],
        "attributes": {
            "valence": 0.7,
            "energy": 0.7,
            "tempo": 120
        }
    },
    "sad": {
        "genres": ["sad", "blues", "acoustic", "piano", "classical"],
        "attributes": {
            "valence": 0.3,
            "energy": 0.4,
            "tempo": 90
        }
    },
    "angry": {
        "genres": ["metal", "rock", "punk", "hardcore"],
        "attributes": {
            "valence": 0.4,
            "energy": 0.8,
            "tempo": 140
        }
    },
    "neutral": {
        "genres": ["indie", "alternative", "ambient", "folk"],
        "attributes": {
            "valence": 0.5,
            "energy": 0.5,
            "tempo": 110
        }
    },
    "fear": {
        "genres": ["dark-ambient", "atmospheric", "instrumental"],
        "attributes": {
            "valence": 0.3,
            "energy": 0.4,
            "tempo": 95
        }
    }
}

class SpotifyConfig:
    def __init__(self):
        self.client_id = "5d5f1dcb76c346448c29ac3cb09eaa58"
        self.client_secret = "ef58d49ea1fd476d969064a09eff6944"
        self.redirect_uri = "http://localhost:8080"
        self.scope = "user-library-read playlist-modify-public user-top-read"
        self.sp = None

    def initialize_spotify(self):
        if not self.sp:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                scope=self.scope,
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri
            ))
        return self.sp

class SpotifyService:
    def __init__(self):
        self.spotify_config = SpotifyConfig()

    def get_track_with_genres(self, track_item: Dict) -> Dict:
        """
        Get track information along with its artist's genres.
        
        Args:
            track_item: Track item from Spotify API
            
        Returns:
            Dict: Track information with genres
        """
        sp = self.spotify_config.initialize_spotify()
        
        artist_id = track_item["track"]["artists"][0]["id"]
        artist_info = sp.artist(artist_id)
        
        return {
            'id': track_item["track"]["id"],
            'name': track_item["track"]["name"],
            'artist': track_item["track"]["artists"][0]["name"],
            'artist_id': artist_id,
            'preview_url': track_item["track"]["preview_url"],
            'external_url': track_item["track"]["external_urls"]["spotify"],
            'genres': artist_info['genres']
        }

    def match_genres_to_emotion(self, genres: List[str], emotion: str) -> float:
        """
        Calculate how well a list of genres matches an emotion.
        
        Args:
            genres: List of track/artist genres
            emotion: Target emotion
            
        Returns:
            float: Match score between 0 and 1
        """
        emotion_genres = set(EMOTION_MAPPING[emotion.lower()]["genres"])
        
        # Create a set of emotion-related keywords
        emotion_keywords = set()
        for genre in emotion_genres:
            emotion_keywords.update(genre.split('-'))
        
        # Count matching genres
        matching_count = 0
        for genre in genres:
            if any(keyword in genre for keyword in emotion_keywords):
                matching_count += 1
        
        # Return score between 0 and 1
        return matching_count / max(len(genres), 1) if genres else 0

    def get_recommendations_by_emotion(self, emotion: str) -> Dict:
        """
        Get track recommendations based on emotion by filtering user's saved tracks.
        
        Args:
            emotion: The detected emotion (happy, sad, angry, neutral, fear)
        
        Returns:
            Dict: Recommended tracks and metadata
        """
        if emotion.lower() not in EMOTION_MAPPING:
            raise ValueError(
                f"Invalid emotion. Must be one of: {', '.join(EMOTION_MAPPING.keys())}"
            )
        
        sp = self.spotify_config.initialize_spotify()
        
        # Get all saved tracks (increase limit as needed)
        results = sp.current_user_saved_tracks(limit=50)['items']
        
        # Get detailed track information with genres
        tracks_with_genres = []
        for item in results:
            track_info = self.get_track_with_genres(item)
            
            # Calculate emotion match score
            emotion_score = self.match_genres_to_emotion(track_info['genres'], emotion)
            track_info['emotion_score'] = emotion_score
            
            tracks_with_genres.append(track_info)
        
        # Sort tracks by emotion match score
        sorted_tracks = sorted(
            tracks_with_genres,
            key=lambda x: x['emotion_score'],
            reverse=True
        )
        
        # Get top 10 matching tracks
        recommended_tracks = sorted_tracks[:10]
        
        return {
            "tracks": recommended_tracks,
            "emotion": emotion,
            "total_tracks_analyzed": len(tracks_with_genres)
        }