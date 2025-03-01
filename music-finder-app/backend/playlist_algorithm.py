import numpy as np
from typing import List, Dict, Any, Optional
import random
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def extract_track_features(track: Dict[Any, Any]) -> Dict[str, float]:
    """
    Extract relevant features from a track for playlist creation
    """
    features = {
        "duration": track.get("duration", 0) / 1000,  # Convert to seconds
        "bpm": track.get("bpm", 0),
        "playback_count": track.get("playback_count", 0),
        "likes_count": track.get("likes_count", 0),
        "genre": track.get("genre", ""),
        "created_at": track.get("created_at", ""),
        "key": track.get("key", ""),
        "energy": random.uniform(0, 1),  # Placeholder for energy (would come from audio analysis)
        "danceability": random.uniform(0, 1),  # Placeholder for danceability
    }
    
    # Add more sophisticated feature extraction here
    # In a real implementation, you might use audio analysis APIs or ML models
    
    return features

def calculate_transition_score(track1: Dict[str, float], track2: Dict[str, float], style: str) -> float:
    """
    Calculate a transition score between two tracks based on their features
    Higher score means better transition
    """
    # Base weights for different transition styles
    if style == "smooth":
        weights = {
            "bpm_diff": -0.5,
            "key_compatibility": 0.3,
            "energy_diff": -0.3,
            "danceability_diff": -0.2,
        }
    elif style == "energetic":
        weights = {
            "bpm_diff": -0.2,
            "key_compatibility": 0.1,
            "energy_diff": 0.3,  # Positive weight for energy changes
            "danceability_diff": 0.2,
        }
    else:  # minimal
        weights = {
            "bpm_diff": -0.7,
            "key_compatibility": 0.4,
            "energy_diff": -0.4,
            "danceability_diff": -0.3,
        }
    
    # Calculate differences
    bpm_diff = abs(track1.get("bpm", 0) - track2.get("bpm", 0))
    energy_diff = abs(track1.get("energy", 0) - track2.get("energy", 0))
    danceability_diff = abs(track1.get("danceability", 0) - track2.get("danceability", 0))
    
    # Simple key compatibility (placeholder - would be more sophisticated in real implementation)
    # In reality, this would use music theory to determine key compatibility
    key_compatibility = 1.0 if track1.get("key", "") == track2.get("key", "") else 0.5
    
    # Calculate weighted score
    score = (
        weights["bpm_diff"] * bpm_diff +
        weights["key_compatibility"] * key_compatibility +
        weights["energy_diff"] * energy_diff +
        weights["danceability_diff"] * danceability_diff
    )
    
    return score

def create_dj_playlist(
    seed_tracks: List[Dict[Any, Any]], 
    duration_minutes: int = 60,
    transition_style: str = "smooth"
) -> Dict[str, Any]:
    """
    Create a DJ playlist based on seed tracks
    
    Args:
        seed_tracks: List of track data from SoundCloud API
        duration_minutes: Target duration in minutes
        transition_style: Style of transitions (smooth, energetic, minimal)
        
    Returns:
        Dictionary with playlist information
    """
    # Extract features from seed tracks
    tracks_with_features = []
    for track in seed_tracks:
        features = extract_track_features(track)
        tracks_with_features.append({
            "track": track,
            "features": features
        })
    
    # Start with the first seed track
    playlist_tracks = [tracks_with_features[0]["track"]]
    current_duration = tracks_with_features[0]["features"]["duration"]
    target_duration_seconds = duration_minutes * 60
    
    # Create a pool of potential tracks (in a real app, this would come from SoundCloud API)
    # For now, we'll just use the seed tracks as our pool
    track_pool = tracks_with_features.copy()
    
    # Build the playlist
    while current_duration < target_duration_seconds and len(track_pool) > 1:
        last_track_features = extract_track_features(playlist_tracks[-1])
        
        # Calculate transition scores for all tracks in the pool
        transition_scores = []
        for track_data in track_pool:
            # Skip if the track is already in the playlist
            if track_data["track"]["id"] in [t["id"] for t in playlist_tracks]:
                continue
                
            score = calculate_transition_score(
                last_track_features, 
                track_data["features"],
                transition_style
            )
            transition_scores.append((track_data, score))
        
        # Sort by transition score (higher is better)
        transition_scores.sort(key=lambda x: x[1], reverse=True)
        
        # If we have no valid transitions, break
        if not transition_scores:
            break
            
        # Add the best track to the playlist
        best_track_data = transition_scores[0][0]
        playlist_tracks.append(best_track_data["track"])
        current_duration += best_track_data["features"]["duration"]
    
    # Create the final playlist object
    playlist = {
        "name": "DJ Mix - " + seed_tracks[0].get("title", "Custom Mix"),
        "tracks": playlist_tracks,
        "duration_seconds": current_duration,
        "transition_style": transition_style,
        "track_count": len(playlist_tracks)
    }
    
    return playlist

def analyze_playlist_energy(playlist: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze the energy flow of a playlist
    Returns data that can be used for visualization
    """
    tracks = playlist["tracks"]
    energy_profile = []
    
    for track in tracks:
        features = extract_track_features(track)
        energy_profile.append({
            "title": track.get("title", "Unknown"),
            "energy": features["energy"],
            "danceability": features["danceability"],
            "bpm": features["bpm"]
        })
    
    # Calculate energy flow statistics
    energy_values = [item["energy"] for item in energy_profile]
    energy_changes = [abs(energy_values[i] - energy_values[i-1]) for i in range(1, len(energy_values))]
    
    analysis = {
        "energy_profile": energy_profile,
        "avg_energy": np.mean(energy_values) if energy_values else 0,
        "energy_variance": np.var(energy_values) if energy_values else 0,
        "avg_energy_change": np.mean(energy_changes) if energy_changes else 0,
        "max_energy": max(energy_values) if energy_values else 0,
        "min_energy": min(energy_values) if energy_values else 0
    }
    
    return analysis 