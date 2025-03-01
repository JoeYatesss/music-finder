#!/usr/bin/env python
"""
Test script for the Music Finder DJ Playlist Algorithm
"""
import json
from playlist_algorithm import (
    extract_track_features, 
    calculate_key_compatibility, 
    calculate_transition_score, 
    create_dj_playlist,
    analyze_playlist_energy
)

# Mock track data for testing
def create_mock_tracks(count=5):
    """Create mock track data for testing"""
    tracks = []
    genres = ["electronic", "house", "techno", "ambient", "downtempo"]
    keys = ["C", "G", "D", "A", "E", "B", "F#", "C#", "Am", "Em", "Bm"]
    
    for i in range(count):
        track = {
            "id": f"track_{i}",
            "title": f"Test Track {i}",
            "user": {
                "username": f"test_user_{i}"
            },
            "duration": 180000 + (i * 30000),  # duration in ms
            "permalink_url": f"https://soundcloud.com/test/track_{i}",
            "artwork_url": f"https://example.com/artwork_{i}.jpg",
        }
        
        # Add optional properties to some tracks
        if i % 2 == 0:
            track["genre"] = genres[i % len(genres)]
        if i % 3 == 0:
            track["bpm"] = 120 + (i * 5)
        if i % 4 == 0:
            track["key"] = keys[i % len(keys)]
            
        tracks.append(track)
    
    return tracks

def test_feature_extraction():
    """Test the feature extraction function"""
    print("\n=== Testing Feature Extraction ===")
    
    # Create a mock track
    track = create_mock_tracks(1)[0]
    print(f"Mock Track: {json.dumps(track, indent=2)}")
    
    # Extract features
    features = extract_track_features(track)
    print(f"\nExtracted Features: {json.dumps(features, indent=2)}")
    
    # Verify all expected features are present
    expected_features = ["bpm", "key", "energy", "danceability", "sonic_signature", "sonic_cluster"]
    for feature in expected_features:
        assert feature in features, f"Missing feature: {feature}"
    
    print("✅ Feature extraction test passed")

def test_key_compatibility():
    """Test the key compatibility function"""
    print("\n=== Testing Key Compatibility ===")
    
    test_cases = [
        ("C", "C", 1.0, "Same key"),
        ("C", "G", 0.8, "Perfect fifth"),
        ("A", "E", 0.8, "Perfect fifth"),
        ("C", "F", 0.8, "Perfect fourth"),
        ("C", "D", 0.3, "Unrelated key"),
        ("", "C", 0.5, "Empty key"),
        ("C", "", 0.5, "Empty key"),
        ("Am", "C", 0.8, "Relative major/minor"),
    ]
    
    for key1, key2, expected, description in test_cases:
        score = calculate_key_compatibility(key1, key2)
        result = "✅ Passed" if abs(score - expected) < 0.01 else "❌ Failed"
        print(f"{result} - {description}: {key1} to {key2} = {score} (expected {expected})")

def test_transition_scoring():
    """Test the transition scoring function"""
    print("\n=== Testing Transition Scoring ===")
    
    # Create mock track features
    track1 = {
        "bpm": 120,
        "key": "C",
        "energy": 0.7,
        "sonic_cluster": "groovy"
    }
    
    # Test different transition styles
    styles = ["smooth", "energetic", "minimal"]
    
    for style in styles:
        print(f"\nTesting '{style}' transition style:")
        
        # Similar track - should have high score
        track2_similar = {
            "bpm": 122,
            "key": "G",
            "energy": 0.75,
            "sonic_cluster": "groovy"
        }
        
        # Different track - should have lower score
        track2_different = {
            "bpm": 140,
            "key": "D#",
            "energy": 0.3,
            "sonic_cluster": "ambient"
        }
        
        score_similar = calculate_transition_score(track1, track2_similar, style)
        score_different = calculate_transition_score(track1, track2_different, style)
        
        print(f"Similar tracks score: {score_similar:.2f}")
        print(f"Different tracks score: {score_different:.2f}")
        
        # Similar tracks should score higher than different tracks
        assert score_similar > score_different, f"Similar track should score higher for {style} style"
    
    print("✅ Transition scoring test passed")

def test_playlist_creation():
    """Test the playlist creation function"""
    print("\n=== Testing Playlist Creation ===")
    
    # Create mock tracks
    tracks = create_mock_tracks(8)
    print(f"Created {len(tracks)} mock tracks")
    
    # Test different transition styles
    for style in ["smooth", "energetic", "minimal"]:
        playlist = create_dj_playlist(tracks, duration_minutes=10, transition_style=style)
        
        print(f"\nPlaylist with '{style}' style:")
        print(f"- Name: {playlist['name']}")
        print(f"- Track count: {playlist['track_count']}")
        print(f"- Duration: {playlist['duration_seconds'] / 60:.1f} minutes")
        print(f"- Transition style: {playlist['transition_style']}")
        
        # Verify playlist structure
        assert "name" in playlist
        assert "tracks" in playlist
        assert "duration_seconds" in playlist
        assert "transition_style" in playlist
        assert "track_count" in playlist
        
        # Verify playlist contains tracks
        assert len(playlist["tracks"]) > 0
        assert playlist["track_count"] == len(playlist["tracks"])
        
        # Analyze energy profile
        energy_analysis = analyze_playlist_energy(playlist)
        print(f"\nEnergy Analysis:")
        print(f"- Average energy: {energy_analysis['avg_energy']:.2f}")
        print(f"- Energy variance: {energy_analysis['energy_variance']:.2f}")
        print(f"- Average energy change: {energy_analysis['avg_energy_change']:.2f}")
        
        # Print the first 3 tracks in the playlist
        print("\nFirst 3 tracks:")
        for i, track in enumerate(playlist["tracks"][:3]):
            print(f"{i+1}. {track['title']} (ID: {track['id']})")
    
    print("\n✅ Playlist creation test passed")

if __name__ == "__main__":
    print("Testing DJ Playlist Algorithm")
    test_feature_extraction()
    test_key_compatibility()
    test_transition_scoring()
    test_playlist_creation()
    print("\n🎵 All tests passed! The playlist algorithm is working correctly.") 