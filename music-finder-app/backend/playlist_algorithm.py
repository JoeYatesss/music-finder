import numpy as np
from typing import List, Dict, Any, Optional
import random
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def extract_track_features(track: Dict[Any, Any]) -> Dict[str, float]:
    """
    Extract relevant features from a track for playlist creation
    Focusing on musical elements and ignoring popularity metrics
    """
    # Get BPM from track metadata or estimate it if not available
    bpm = track.get("bpm", 0)
    if bpm == 0:
        # In a real implementation, we would use audio analysis to estimate BPM
        bpm = random.randint(90, 140)  # Placeholder with reasonable range
    
    # Extract or generate musical features
    features = {
        "bpm": bpm,
        "key": track.get("key", ""),
        # In a real implementation, these would come from audio analysis
        "energy": random.uniform(0, 1),  # Placeholder for energy level
        "danceability": random.uniform(0, 1),  # Placeholder for danceability
        "acousticness": random.uniform(0, 1),  # Placeholder for acoustic quality
        "instrumentalness": random.uniform(0, 1),  # Placeholder for instrumental vs vocal
        "valence": random.uniform(0, 1),  # Placeholder for musical positiveness
    }
    
    # Create a sonic signature for the track (would be derived from audio analysis)
    # This helps group tracks with similar sound qualities
    features["sonic_signature"] = (
        features["energy"] * 0.3 + 
        features["danceability"] * 0.3 + 
        features["acousticness"] * 0.2 + 
        features["instrumentalness"] * 0.1 + 
        features["valence"] * 0.1
    )
    
    # Classify into pseudo-genre clusters based on sonic signature
    # In a real implementation, this would use machine learning
    if features["sonic_signature"] < 0.3:
        features["sonic_cluster"] = "ambient"
    elif features["sonic_signature"] < 0.5:
        features["sonic_cluster"] = "downtempo"
    elif features["sonic_signature"] < 0.7:
        features["sonic_cluster"] = "groovy"
    else:
        features["sonic_cluster"] = "energetic"
    
    return features

def calculate_key_compatibility(key1: str, key2: str) -> float:
    """
    Calculate musical key compatibility based on the circle of fifths
    Higher score means better harmonic transition
    
    In a real implementation, this would include full circle of fifths
    and relative major/minor relationships
    """
    if not key1 or not key2:
        return 0.5  # Unknown keys get medium compatibility
    
    if key1 == key2:
        return 1.0  # Perfect match
    
    # Simple circle of fifths relationship (highly simplified)
    # In a real implementation, this would be a complete mapping
    circle_of_fifths = {
        "C": ["G", "F", "Am"],
        "G": ["D", "C", "Em"],
        "D": ["A", "G", "Bm"],
        "A": ["E", "D", "F#m"],
        "E": ["B", "A", "C#m"],
        "B": ["F#", "E", "G#m"],
        "F#": ["C#", "B", "D#m"],
        "C#": ["G#", "F#", "A#m"],
        "G#": ["D#", "C#", "Fm"],
        "D#": ["A#", "G#", "Cm"],
        "A#": ["F", "D#", "Gm"],
        "F": ["C", "A#", "Dm"],
        # Add minor keys and their relationships
        "Am": ["Em", "Dm", "C"],
        "Em": ["Bm", "Am", "G"],
        # ... and so on
    }
    
    # Check if keys are adjacent on the circle of fifths
    if key2 in circle_of_fifths.get(key1, []):
        return 0.8  # Good compatibility
    
    return 0.3  # Poor compatibility

def calculate_transition_score(track1: Dict[str, float], track2: Dict[str, float], style: str) -> float:
    """
    Calculate a transition score between two tracks based on their features
    Higher score means better transition
    """
    # Base weights for different transition styles
    if style == "smooth":
        weights = {
            "bpm_diff": -1.2,  # Higher weight on BPM for smooth transitions
            "key_compatibility": 1.5,  # Higher weight on key compatibility
            "energy_diff": -0.7,
            "sonic_cluster": 0.8,  # Similar sonic qualities
        }
    elif style == "energetic":
        weights = {
            "bpm_diff": -0.5,  # Less penalty for BPM differences
            "key_compatibility": 0.8,
            "energy_diff": 0.6,  # Positive weight for energy changes (encourages contrast)
            "sonic_cluster": 0.4,
        }
    else:  # minimal
        weights = {
            "bpm_diff": -1.5,  # Strongest penalty for BPM differences
            "key_compatibility": 1.2,
            "energy_diff": -1.0,  # Strong penalty for energy differences
            "sonic_cluster": 1.0,  # Very important to keep sonic quality consistent
        }
    
    # Calculate differences and compatibility scores
    bpm_diff = abs(track1.get("bpm", 0) - track2.get("bpm", 0))
    energy_diff = abs(track1.get("energy", 0) - track2.get("energy", 0))
    
    # Calculate key compatibility using musical theory
    key_compatibility = calculate_key_compatibility(
        track1.get("key", ""), 
        track2.get("key", "")
    )
    
    # Sonic cluster compatibility (1.0 if same cluster, 0.5 if different)
    sonic_cluster_score = 1.0 if track1.get("sonic_cluster") == track2.get("sonic_cluster") else 0.5
    
    # Normalize BPM difference (0-50 range is typical for DJ transitions)
    normalized_bpm_diff = min(bpm_diff / 50.0, 1.0)
    
    # Calculate weighted score
    score = (
        weights["bpm_diff"] * normalized_bpm_diff +
        weights["key_compatibility"] * key_compatibility +
        weights["energy_diff"] * energy_diff +
        weights["sonic_cluster"] * sonic_cluster_score
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
    current_duration = tracks_with_features[0]["track"].get("duration", 0) / 1000  # Convert to seconds
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
        current_duration += best_track_data["track"].get("duration", 0) / 1000
    
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
            "bpm": features["bpm"],
            "key": features.get("key", "Unknown"),
            "sonic_cluster": features.get("sonic_cluster", "Unknown")
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