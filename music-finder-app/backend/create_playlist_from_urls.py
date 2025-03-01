#!/usr/bin/env python
"""
Script to create a DJ playlist from multiple SoundCloud track URLs
This script allows you to input multiple SoundCloud track URLs and generate a playlist
"""
import json
import os
import asyncio
import httpx
from dotenv import load_dotenv
from playlist_algorithm import create_dj_playlist, analyze_playlist_energy

# Load environment variables
load_dotenv()

# SoundCloud API client ID
SOUNDCLOUD_CLIENT_ID = os.getenv("SOUNDCLOUD_CLIENT_ID")

def format_duration(ms):
    """Format milliseconds to minutes:seconds"""
    seconds = ms / 1000
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes}:{remaining_seconds:02d}"

def print_track_info(track):
    """Print formatted track information"""
    print(f"{track.get('title', 'Unknown')} by {track.get('user', {}).get('username', 'Unknown')}")
    print(f"  Duration: {format_duration(track.get('duration', 0))}")
    print(f"  Genre: {track.get('genre', 'Unknown')}")
    print(f"  BPM: {track.get('bpm', 'Unknown')}")
    print(f"  Key: {track.get('key', 'Unknown')}")
    print("")

async def fetch_track(client, track_url):
    """Fetch track data from SoundCloud"""
    print(f"Fetching track: {track_url}")
    try:
        # Resolve the track URL to get the track data
        resolve_url = f"https://api.soundcloud.com/resolve?url={track_url}&client_id={SOUNDCLOUD_CLIENT_ID}"
        response = await client.get(resolve_url)
        
        if response.status_code != 200:
            print(f"Error: Failed to resolve track URL (Status code: {response.status_code})")
            return None
        
        track_data = response.json()
        print(f"✅ Found: {track_data.get('title', 'Unknown')} by {track_data.get('user', {}).get('username', 'Unknown')}")
        return track_data
    
    except Exception as e:
        print(f"Error fetching track: {str(e)}")
        return None

async def create_playlist():
    """Create a playlist from SoundCloud track URLs"""
    if not SOUNDCLOUD_CLIENT_ID:
        print("Error: SOUNDCLOUD_CLIENT_ID environment variable is not set.")
        print("Please create a .env file with your SoundCloud API client ID.")
        return
    
    print("=== Create DJ Playlist from SoundCloud Tracks ===")
    print("Enter SoundCloud track URLs (one per line, leave blank when done):")
    
    track_urls = []
    while True:
        url = input(f"Track {len(track_urls) + 1} URL (or press enter to finish): ")
        if not url:
            if len(track_urls) > 0:
                break
            else:
                print("Please enter at least one track URL.")
                continue
        track_urls.append(url)
    
    # Fetch all tracks
    print(f"\nFetching {len(track_urls)} tracks from SoundCloud...")
    
    async with httpx.AsyncClient() as client:
        tasks = [fetch_track(client, url) for url in track_urls]
        track_results = await asyncio.gather(*tasks)
        
        # Filter out None results (failed fetches)
        tracks = [track for track in track_results if track is not None]
        
        if not tracks:
            print("No valid tracks found. Exiting.")
            return
        
        print(f"\nSuccessfully fetched {len(tracks)} tracks:")
        for i, track in enumerate(tracks):
            print(f"{i+1}. ", end="")
            print_track_info(track)
        
        # Select transition style
        print("\nSelect transition style:")
        styles = ["smooth", "energetic", "minimal"]
        for i, style in enumerate(styles):
            print(f"{i+1}. {style}")
        
        while True:
            try:
                style_choice = int(input("Enter style number (1-3): "))
                if 1 <= style_choice <= 3:
                    style = styles[style_choice - 1]
                    break
                print("Please enter a number between 1 and 3")
            except ValueError:
                print("Please enter a valid number")
        
        # Set playlist duration
        while True:
            try:
                duration = int(input("\nEnter target playlist duration in minutes (10-180): "))
                if 10 <= duration <= 180:
                    break
                print("Duration must be between 10 and 180 minutes")
            except ValueError:
                print("Please enter a valid number")
        
        # Generate the playlist
        print(f"\nGenerating {style} playlist with target duration of {duration} minutes...")
        
        playlist = create_dj_playlist(
            seed_tracks=tracks,
            duration_minutes=duration,
            transition_style=style
        )
        
        # Add energy analysis
        energy_analysis = analyze_playlist_energy(playlist)
        playlist["energy_analysis"] = energy_analysis
        
        # Print playlist summary
        print("\n===== PLAYLIST SUMMARY =====")
        print(f"Name: {playlist['name']}")
        print(f"Duration: {playlist['duration_seconds'] // 60} minutes {playlist['duration_seconds'] % 60} seconds")
        print(f"Tracks: {playlist['track_count']}")
        print(f"Style: {playlist['transition_style']}")
        print(f"Average Energy: {energy_analysis['avg_energy']:.2f}")
        
        # Print tracks in the playlist
        print("\nTracks in playlist:")
        for i, track in enumerate(playlist['tracks']):
            print(f"{i+1}. {track['title']} by {track['user']['username']}")
            
            if i < len(playlist['tracks']) - 1:
                # If we have energy profiles, show transition details
                if 'energy_analysis' in playlist and i < len(energy_analysis['energy_profile']):
                    curr_profile = energy_analysis['energy_profile'][i]
                    next_profile = energy_analysis['energy_profile'][i+1]
                    
                    print(f"   → Transition to: {playlist['tracks'][i+1]['title']}")
                    print(f"     BPM: {curr_profile['bpm']:.1f} → {next_profile['bpm']:.1f}")
                    print(f"     Key: {curr_profile['key']} → {next_profile['key']}")
                    print(f"     Compatibility: {calculate_key_compatibility(curr_profile['key'], next_profile['key']):.2f}")
        
        # Save playlist to a JSON file
        playlist_name = "".join(c for c in playlist['name'] if c.isalnum() or c in " -_")[:30]
        filename = f"playlist_{playlist_name}_{style}.json"
        with open(filename, "w") as f:
            json.dump(playlist, f, indent=2)
        print(f"\nPlaylist saved to {filename}")

# Add key compatibility function for displaying transition details
def calculate_key_compatibility(key1, key2):
    """Simple wrapper around the imported function"""
    from playlist_algorithm import calculate_key_compatibility as calc_compat
    return calc_compat(key1, key2)

if __name__ == "__main__":
    asyncio.run(create_playlist()) 