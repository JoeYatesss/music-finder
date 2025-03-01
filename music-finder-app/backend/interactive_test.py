#!/usr/bin/env python
"""
Interactive testing script for the Music Finder DJ Playlist Algorithm
This script allows you to test the algorithm with different parameters
"""
import json
import os
import random
import httpx
from playlist_algorithm import (
    extract_track_features,
    calculate_key_compatibility,
    calculate_transition_score,
    create_dj_playlist,
    analyze_playlist_energy
)

# Load environment variables for API access
from dotenv import load_dotenv
load_dotenv()

# SoundCloud API client ID
SOUNDCLOUD_CLIENT_ID = os.getenv("SOUNDCLOUD_CLIENT_ID")

# Load sample tracks
def load_sample_tracks():
    """Load sample tracks from JSON file if it exists, otherwise create new ones"""
    if os.path.exists("sample_tracks.json"):
        with open("sample_tracks.json", "r") as f:
            return json.load(f)
    else:
        # Create sample tracks with a diverse range of properties
        tracks = create_diverse_tracks(20)
        with open("sample_tracks.json", "w") as f:
            json.dump(tracks, f, indent=2)
        return tracks

def create_diverse_tracks(count=20):
    """Create a diverse set of sample tracks"""
    genres = ["House", "Techno", "Deep House", "Progressive", "Ambient", 
              "Downtempo", "Drum & Bass", "Minimal", "Tech House", "Electronica"]
    
    keys = ["C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "F",
            "Am", "Em", "Bm", "F#m", "C#m", "G#m", "D#m", "A#m", "Fm", "Cm", "Gm", "Dm"]
    
    tracks = []
    for i in range(count):
        # Create varying BPMs in different ranges
        bpm_range = random.choice([
            (80, 100),    # Downtempo/Ambient
            (118, 130),   # House/Deep House
            (125, 135),   # Techno
            (170, 180)    # Drum & Bass
        ])
        
        bpm = random.randint(bpm_range[0], bpm_range[1])
        
        # Duration between 3 and 9 minutes
        duration = random.randint(180, 540) * 1000
        
        track = {
            "id": f"track_{i+1}",
            "title": f"{random.choice(['Deep', 'Smooth', 'Dark', 'Light', 'Groovy', 'Melodic', 'Hypnotic', 'Dreamy'])} {random.choice(genres)} {i+1}",
            "user": {"username": f"Producer_{i+1}"},
            "duration": duration,
            "permalink_url": f"https://soundcloud.com/example/track_{i+1}",
            "artwork_url": f"https://example.com/artwork_{i+1}.jpg",
            "genre": random.choice(genres),
            "bpm": bpm,
            "key": random.choice(keys)
        }
        tracks.append(track)
    
    return tracks

def format_duration(ms):
    """Format milliseconds to minutes:seconds"""
    seconds = ms / 1000
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes}:{remaining_seconds:02d}"

def print_track_info(track, index=None, show_features=False):
    """Print formatted track information"""
    prefix = f"{index}. " if index is not None else ""
    print(f"{prefix}{track['title']} by {track['user']['username']}")
    print(f"   Duration: {format_duration(track['duration'])}, BPM: {track.get('bpm', 'Unknown')}, Key: {track.get('key', 'Unknown')}")
    print(f"   Genre: {track.get('genre', 'Unknown')}")
    
    if show_features:
        features = extract_track_features(track)
        print(f"   Sonic Cluster: {features['sonic_cluster']}")
        print(f"   Energy: {features['energy']:.2f}, Danceability: {features['danceability']:.2f}")
        print(f"   Sonic Signature: {features['sonic_signature']:.2f}")
    
    print("")

def select_tracks(tracks, message="Select tracks (comma-separated numbers, e.g. 1,3,5):"):
    """Let the user select tracks from a list"""
    while True:
        selection = input(message + " ")
        try:
            indices = [int(i.strip()) - 1 for i in selection.split(",")]
            selected_tracks = [tracks[i] for i in indices if 0 <= i < len(tracks)]
            if not selected_tracks:
                print("No valid tracks selected. Please try again.")
                continue
            return selected_tracks
        except (ValueError, IndexError):
            print("Invalid selection. Please enter comma-separated numbers.")

def select_option(options, prompt):
    """Let the user select an option from a list"""
    print(prompt)
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
    
    while True:
        try:
            choice = int(input("Enter your choice (number): "))
            if 1 <= choice <= len(options):
                return options[choice-1]
            print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print("Please enter a valid number")

def get_int_input(prompt, min_val=None, max_val=None, default=None):
    """Get an integer input from the user with validation"""
    default_str = f" (default: {default})" if default is not None else ""
    while True:
        try:
            value_str = input(f"{prompt}{default_str}: ")
            if value_str == "" and default is not None:
                return default
            
            value = int(value_str)
            if min_val is not None and value < min_val:
                print(f"Value must be at least {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Value must be at most {max_val}")
                continue
            return value
        except ValueError:
            print("Please enter a valid number")

def test_key_compatibility_interactive():
    """Test key compatibility interactively"""
    print("\n===== KEY COMPATIBILITY TEST =====")
    
    # List of common keys
    keys = ["C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "F",
            "Am", "Em", "Bm", "F#m", "C#m", "G#m", "D#m", "A#m", "Fm", "Cm", "Gm", "Dm"]
    
    print("Available keys:")
    for i, key in enumerate(keys):
        print(f"{i+1}. {key}", end="\t")
        if (i + 1) % 6 == 0:
            print()
    print()
    
    while True:
        try:
            key1_idx = int(input("Select first key (number, 0 to exit): "))
            if key1_idx == 0:
                return
            
            key1 = keys[key1_idx - 1]
            
            print("\nCompatibility with other keys:")
            for i, key2 in enumerate(keys):
                score = calculate_key_compatibility(key1, key2)
                compatibility = "Perfect" if score >= 0.9 else "Good" if score >= 0.7 else "Fair" if score >= 0.5 else "Poor"
                print(f"{i+1}. {key2}: {score:.2f} ({compatibility})")
            
            print()
        except (ValueError, IndexError):
            print("Invalid selection.")

def run_algorithm_test():
    """Run an interactive test of the playlist algorithm"""
    print("\n===== PLAYLIST ALGORITHM TEST =====")
    
    # Load sample tracks
    tracks = load_sample_tracks()
    
    # Show available tracks
    print("Available tracks:")
    for i, track in enumerate(tracks):
        print_track_info(track, i+1)
    
    # Select seed tracks
    seed_tracks = select_tracks(tracks, "Select seed tracks (comma-separated numbers):")
    
    # Print selected seed tracks
    print("\nSelected seed tracks:")
    for i, track in enumerate(seed_tracks):
        print_track_info(track, i+1, show_features=True)
    
    # Select transition style
    style = select_option(["smooth", "energetic", "minimal"], "Select transition style:")
    
    # Set playlist duration
    duration = get_int_input("Enter target playlist duration in minutes", min_val=5, max_val=180, default=30)
    
    # Generate the playlist
    print("\nGenerating playlist...")
    playlist = create_dj_playlist(
        seed_tracks=seed_tracks,
        duration_minutes=duration,
        transition_style=style
    )
    
    # Add energy analysis
    energy_analysis = analyze_playlist_energy(playlist)
    playlist["energy_analysis"] = energy_analysis
    
    # Print playlist details
    print("\nGenerated Playlist:")
    print(f"Name: {playlist['name']}")
    print(f"Duration: {playlist['duration_seconds'] // 60} minutes {playlist['duration_seconds'] % 60} seconds")
    print(f"Tracks: {playlist['track_count']}")
    print(f"Style: {playlist['transition_style']}")
    print(f"Average Energy: {energy_analysis['avg_energy']:.2f}")
    
    # Print tracks in the playlist
    print("\nTracks in playlist:")
    for i, track in enumerate(playlist['tracks']):
        profile = energy_analysis['energy_profile'][i] if i < len(energy_analysis['energy_profile']) else None
        
        print_track_info(track, i+1)
        
        if profile:
            print(f"   Energy: {profile['energy']:.2f}, Danceability: {profile['danceability']:.2f}")
            print(f"   Sonic Cluster: {profile['sonic_cluster']}")
        
        # Show transition info if not the last track
        if i < len(playlist['tracks']) - 1 and i+1 < len(energy_analysis['energy_profile']):
            next_profile = energy_analysis['energy_profile'][i+1]
            print(f"   → Transition to: {playlist['tracks'][i+1]['title']}")
            
            # BPM change
            bpm_change = next_profile['bpm'] - profile['bpm']
            bpm_change_str = f"+{bpm_change:.1f}" if bpm_change > 0 else f"{bpm_change:.1f}"
            print(f"      BPM: {profile['bpm']:.1f} → {next_profile['bpm']:.1f} ({bpm_change_str})")
            
            # Energy change
            energy_change = next_profile['energy'] - profile['energy']
            energy_change_str = f"+{energy_change:.2f}" if energy_change > 0 else f"{energy_change:.2f}"
            print(f"      Energy: {profile['energy']:.2f} → {next_profile['energy']:.2f} ({energy_change_str})")
            
            # Key change
            print(f"      Key: {profile['key']} → {next_profile['key']}")
            print(f"      Key Compatibility: {calculate_key_compatibility(profile['key'], next_profile['key']):.2f}")
            
        print("")
    
    # Save playlist to a JSON file
    filename = f"test_{style}_playlist.json"
    with open(filename, "w") as f:
        json.dump(playlist, f, indent=2)
    print(f"Playlist saved to {filename}")

async def analyze_soundcloud_track():
    """Analyze a track from SoundCloud by URL"""
    print("\n===== SOUNDCLOUD TRACK ANALYSIS =====")
    
    if not SOUNDCLOUD_CLIENT_ID:
        print("Error: SOUNDCLOUD_CLIENT_ID environment variable is not set.")
        print("Please create a .env file with your SoundCloud API client ID.")
        return
    
    track_url = input("Enter SoundCloud track URL: ")
    if not track_url:
        print("No URL provided.")
        return
    
    print("\nFetching track information from SoundCloud...")
    try:
        async with httpx.AsyncClient() as client:
            # Resolve the track URL to get the track ID
            resolve_url = f"https://api.soundcloud.com/resolve?url={track_url}&client_id={SOUNDCLOUD_CLIENT_ID}"
            response = await client.get(resolve_url)
            
            if response.status_code != 200:
                print(f"Error: Failed to resolve track URL (Status code: {response.status_code})")
                return
            
            track_data = response.json()
            
            print("\n===== TRACK INFORMATION =====")
            print(f"Title: {track_data.get('title', 'Unknown')}")
            print(f"Artist: {track_data.get('user', {}).get('username', 'Unknown')}")
            print(f"Duration: {format_duration(track_data.get('duration', 0))}")
            print(f"Genre: {track_data.get('genre', 'Unknown')}")
            print(f"BPM: {track_data.get('bpm', 'Unknown')}")
            print(f"Key: {track_data.get('key', 'Unknown')}")
            print(f"Created: {track_data.get('created_at', 'Unknown')}")
            print(f"Plays: {track_data.get('playback_count', 0)}")
            print(f"Likes: {track_data.get('likes_count', 0)}")
            
            # Extract features using our algorithm
            print("\n===== TRACK ANALYSIS =====")
            features = extract_track_features(track_data)
            
            print(f"Generated BPM: {features.get('bpm', 'Unknown')}")
            print(f"Energy: {features.get('energy', 0):.2f}")
            print(f"Danceability: {features.get('danceability', 0):.2f}")
            print(f"Acousticness: {features.get('acousticness', 0):.2f}")
            print(f"Instrumentalness: {features.get('instrumentalness', 0):.2f}")
            print(f"Valence: {features.get('valence', 0):.2f}")
            print(f"Sonic Signature: {features.get('sonic_signature', 0):.2f}")
            print(f"Sonic Cluster: {features.get('sonic_cluster', 'Unknown')}")
            
            # Save the analysis to a JSON file
            output = {
                "track_info": track_data,
                "analysis": features
            }
            
            filename = f"track_analysis_{track_data.get('id', 'unknown')}.json"
            with open(filename, "w") as f:
                json.dump(output, f, indent=2)
            print(f"\nAnalysis saved to {filename}")
            
            # Ask if the user wants to create a playlist based on this track
            create_playlist_choice = input("\nWould you like to create a playlist based on this track? (y/n): ")
            if create_playlist_choice.lower() == 'y':
                # Create a playlist with just this track as the seed
                style = select_option(["smooth", "energetic", "minimal"], "Select transition style:")
                duration = get_int_input("Enter target playlist duration in minutes", min_val=5, max_val=180, default=30)
                
                print("\nGenerating playlist...")
                playlist = create_dj_playlist(
                    seed_tracks=[track_data],
                    duration_minutes=duration,
                    transition_style=style
                )
                
                # Add energy analysis
                energy_analysis = analyze_playlist_energy(playlist)
                playlist["energy_analysis"] = energy_analysis
                
                # Save playlist to a JSON file
                playlist_filename = f"playlist_from_{track_data.get('id', 'unknown')}_{style}.json"
                with open(playlist_filename, "w") as f:
                    json.dump(playlist, f, indent=2)
                print(f"Playlist saved to {playlist_filename}")
            
    except Exception as e:
        print(f"Error analyzing track: {str(e)}")

def main_menu():
    """Display the main menu"""
    menu_options = [
        "Test key compatibility",
        "Run playlist algorithm test",
        "Analyze SoundCloud track by URL",
        "Exit"
    ]
    
    while True:
        print("\n===== MUSIC FINDER ALGORITHM TESTING =====")
        for i, option in enumerate(menu_options):
            print(f"{i+1}. {option}")
        
        try:
            choice = int(input("\nSelect an option: "))
            
            if choice == 1:
                test_key_compatibility_interactive()
            elif choice == 2:
                run_algorithm_test()
            elif choice == 3:
                import asyncio
                asyncio.run(analyze_soundcloud_track())
            elif choice == 4:
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    print("=== Music Finder DJ Playlist Algorithm Interactive Test ===")
    main_menu() 