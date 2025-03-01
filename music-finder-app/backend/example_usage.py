#!/usr/bin/env python
"""
Example usage of the Music Finder DJ Playlist Algorithm
This script demonstrates how to use the algorithm with example tracks
"""
import json
from playlist_algorithm import create_dj_playlist, analyze_playlist_energy

# Sample tracks (in a real app, these would come from SoundCloud API)
sample_tracks = [
    {
        "id": "track_1",
        "title": "Deep House Groove",
        "user": {"username": "DJ Producer"},
        "duration": 240000,  # 4 minutes in milliseconds
        "permalink_url": "https://soundcloud.com/example/deep-house",
        "artwork_url": "https://example.com/artwork1.jpg",
        "genre": "Deep House",
        "bpm": 124,
        "key": "Am"
    },
    {
        "id": "track_2",
        "title": "Tech House Beat",
        "user": {"username": "TechDJ"},
        "duration": 300000,  # 5 minutes
        "permalink_url": "https://soundcloud.com/example/tech-house",
        "artwork_url": "https://example.com/artwork2.jpg",
        "genre": "Tech House",
        "bpm": 126,
        "key": "G"
    },
    {
        "id": "track_3",
        "title": "Progressive Journey",
        "user": {"username": "ProgressiveMaster"},
        "duration": 420000,  # 7 minutes
        "permalink_url": "https://soundcloud.com/example/progressive",
        "artwork_url": "https://example.com/artwork3.jpg",
        "genre": "Progressive House",
        "bpm": 128,
        "key": "C"
    },
    {
        "id": "track_4",
        "title": "Melodic Techno",
        "user": {"username": "MelodicMind"},
        "duration": 360000,  # 6 minutes
        "permalink_url": "https://soundcloud.com/example/melodic-techno",
        "artwork_url": "https://example.com/artwork4.jpg",
        "genre": "Melodic Techno",
        "bpm": 125,
        "key": "D"
    },
    {
        "id": "track_5",
        "title": "Ambient Chillout",
        "user": {"username": "ChillMaster"},
        "duration": 280000,  # 4.67 minutes
        "permalink_url": "https://soundcloud.com/example/ambient",
        "artwork_url": "https://example.com/artwork5.jpg",
        "genre": "Ambient",
        "bpm": 100,
        "key": "E"
    },
    {
        "id": "track_6",
        "title": "Downtempo Vibes",
        "user": {"username": "DowntempoDJ"},
        "duration": 320000,  # 5.33 minutes
        "permalink_url": "https://soundcloud.com/example/downtempo",
        "artwork_url": "https://example.com/artwork6.jpg",
        "genre": "Downtempo",
        "bpm": 90,
        "key": "Bm"
    },
    {
        "id": "track_7",
        "title": "Drum & Bass Energy",
        "user": {"username": "DNBproducer"},
        "duration": 260000,  # 4.33 minutes
        "permalink_url": "https://soundcloud.com/example/dnb",
        "artwork_url": "https://example.com/artwork7.jpg",
        "genre": "Drum & Bass",
        "bpm": 174,
        "key": "F"
    },
    {
        "id": "track_8",
        "title": "Minimal Textures",
        "user": {"username": "MinimalMaster"},
        "duration": 380000,  # 6.33 minutes
        "permalink_url": "https://soundcloud.com/example/minimal",
        "artwork_url": "https://example.com/artwork8.jpg",
        "genre": "Minimal",
        "bpm": 122,
        "key": "G"
    }
]

def format_duration(ms):
    """Format milliseconds to minutes:seconds"""
    seconds = ms / 1000
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes}:{remaining_seconds:02d}"

def print_track_info(track, index=None):
    """Print formatted track information"""
    prefix = f"{index}. " if index is not None else ""
    print(f"{prefix}{track['title']} by {track['user']['username']}")
    print(f"   Duration: {format_duration(track['duration'])}, BPM: {track.get('bpm', 'Unknown')}, Key: {track.get('key', 'Unknown')}")
    print(f"   Genre: {track.get('genre', 'Unknown')}")
    print("")

def main():
    """Run the example"""
    print("\n===== MUSIC FINDER DJ PLAYLIST EXAMPLE =====\n")
    
    # Print available tracks
    print("Available tracks:")
    for i, track in enumerate(sample_tracks):
        print_track_info(track, i+1)
    
    # Create playlists with different styles
    styles = ["smooth", "energetic", "minimal"]
    
    for style in styles:
        print(f"\n===== CREATING '{style.upper()}' PLAYLIST =====")
        
        # Seed tracks (in a real app, these would be selected by the user)
        # We'll use the first 3 tracks as seeds
        seed_tracks = sample_tracks[:3]
        print("\nSeed tracks:")
        for i, track in enumerate(seed_tracks):
            print_track_info(track, i+1)
        
        # Generate the playlist
        playlist = create_dj_playlist(
            seed_tracks=seed_tracks,
            duration_minutes=30,  # 30 minute target duration
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
                
            print("")
        
        # Save playlist to a JSON file for reference
        filename = f"example_{style}_playlist.json"
        with open(filename, "w") as f:
            json.dump(playlist, f, indent=2)
        print(f"Playlist saved to {filename}")

if __name__ == "__main__":
    main() 