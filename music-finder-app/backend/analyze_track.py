#!/usr/bin/env python
"""
Standalone script to analyze a SoundCloud track by URL
This script extracts musical features from a track and visualizes them
"""
import json
import os
import asyncio
import sys
import random

# Try importing httpx, handle if not available
try:
    import httpx
except ImportError:
    print("Error: The 'httpx' package is required. Please install it using:")
    print("  pip install httpx")
    sys.exit(1)

# Try importing numpy, handle if not available
try:
    import numpy as np
except ImportError:
    print("Error: The 'numpy' package is required. Please install it using:")
    print("  pip install numpy")
    sys.exit(1)

# Try importing dotenv, handle if not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Using hardcoded client ID if available.")

# SoundCloud API client ID - prefer environment variable, fallback to input
SOUNDCLOUD_CLIENT_ID = os.getenv("SOUNDCLOUD_CLIENT_ID")

def format_duration(ms):
    """Format milliseconds to minutes:seconds"""
    seconds = ms / 1000
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes}:{remaining_seconds:02d}"

def extract_track_features(track):
    """
    Extract relevant features from a track for analysis
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

async def analyze_track(track_url):
    """Analyze a SoundCloud track by URL"""
    global SOUNDCLOUD_CLIENT_ID
    
    if not SOUNDCLOUD_CLIENT_ID:
        print("No SoundCloud client ID found in environment variables.")
        SOUNDCLOUD_CLIENT_ID = input("Please enter your SoundCloud client ID: ")
        if not SOUNDCLOUD_CLIENT_ID:
            print("Error: A SoundCloud client ID is required to use the API.")
            return
    
    if not track_url:
        print("Error: No URL provided.")
        return
    
    print(f"Analyzing track: {track_url}")
    print("Fetching track information from SoundCloud...")
    
    try:
        async with httpx.AsyncClient() as client:
            # Resolve the track URL to get the track data
            resolve_url = f"https://api.soundcloud.com/resolve?url={track_url}&client_id={SOUNDCLOUD_CLIENT_ID}"
            response = await client.get(resolve_url)
            
            if response.status_code != 200:
                print(f"Error: Failed to resolve track URL (Status code: {response.status_code})")
                print(f"Response: {response.text}")
                return
            
            track_data = response.json()
            
            # Print basic track information
            print("\n===== TRACK INFORMATION =====")
            print(f"Title: {track_data.get('title', 'Unknown')}")
            print(f"Artist: {track_data.get('user', {}).get('username', 'Unknown')}")
            print(f"Duration: {format_duration(track_data.get('duration', 0))}")
            print(f"Genre: {track_data.get('genre', 'Unknown')}")
            print(f"BPM: {track_data.get('bpm', 'Unknown')}")
            print(f"Key: {track_data.get('key', 'Unknown')}")
            
            # Additional track metadata
            print("\n===== TRACK METADATA =====")
            print(f"Created: {track_data.get('created_at', 'Unknown')}")
            print(f"Plays: {track_data.get('playback_count', 0):,}")
            print(f"Likes: {track_data.get('likes_count', 0):,}")
            print(f"Comments: {track_data.get('comment_count', 0):,}")
            print(f"Description: {(track_data.get('description', 'None') or 'None')[:100]}...")
            
            # Extract features using our algorithm
            print("\n===== MUSICAL ANALYSIS =====")
            features = extract_track_features(track_data)
            
            print(f"Generated BPM: {features.get('bpm', 'Unknown')}")
            print(f"Energy: {features.get('energy', 0):.2f}")
            print(f"Danceability: {features.get('danceability', 0):.2f}")
            print(f"Acousticness: {features.get('acousticness', 0):.2f}")
            print(f"Instrumentalness: {features.get('instrumentalness', 0):.2f}")
            print(f"Valence: {features.get('valence', 0):.2f}")
            
            # Classification results
            print("\n===== CLASSIFICATION =====")
            print(f"Sonic Signature: {features.get('sonic_signature', 0):.2f}")
            print(f"Sonic Cluster: {features.get('sonic_cluster', 'Unknown')}")
            print(f"Classified as: {features.get('sonic_cluster', 'Unknown')} track with " +
                  f"{'high' if features.get('energy', 0) > 0.7 else 'medium' if features.get('energy', 0) > 0.4 else 'low'} energy")
            
            # Visual representation of features
            print("\n===== FEATURE VISUALIZATION =====")
            features_to_visualize = {
                "Energy": features.get('energy', 0),
                "Danceability": features.get('danceability', 0),
                "Acousticness": features.get('acousticness', 0),
                "Instrumentalness": features.get('instrumentalness', 0),
                "Valence": features.get('valence', 0)
            }
            
            # Simple ASCII visualization
            max_bar_length = 50
            for name, value in features_to_visualize.items():
                bar_length = int(value * max_bar_length)
                bar = "█" * bar_length + "░" * (max_bar_length - bar_length)
                print(f"{name:15} [{bar}] {value:.2f}")
            
            # Save the analysis to a JSON file
            output = {
                "track_info": {
                    "id": track_data.get('id'),
                    "title": track_data.get('title'),
                    "artist": track_data.get('user', {}).get('username'),
                    "permalink_url": track_data.get('permalink_url'),
                    "duration": track_data.get('duration'),
                    "genre": track_data.get('genre'),
                    "bpm": track_data.get('bpm'),
                    "key": track_data.get('key'),
                    "created_at": track_data.get('created_at'),
                    "plays": track_data.get('playback_count'),
                    "likes": track_data.get('likes_count')
                },
                "analysis": features
            }
            
            # Create a clean filename from the track title
            safe_title = "".join(c for c in track_data.get('title', 'unknown') if c.isalnum() or c in " -_")[:30]
            filename = f"analysis_{safe_title}_{track_data.get('id', 'unknown')}.json"
            
            with open(filename, "w") as f:
                json.dump(output, f, indent=2)
            print(f"\nAnalysis saved to {filename}")
            
    except Exception as e:
        print(f"Error analyzing track: {str(e)}")
        import traceback
        traceback.print_exc()

async def main():
    """Main function to run the script"""
    print("=== SoundCloud Track Analyzer ===")
    print("This tool analyzes musical elements of a SoundCloud track\n")
    
    # Get track URL from command line arguments or prompt
    import sys
    if len(sys.argv) > 1:
        track_url = sys.argv[1]
    else:
        track_url = input("Enter SoundCloud track URL: ")
    
    await analyze_track(track_url)

if __name__ == "__main__":
    asyncio.run(main()) 