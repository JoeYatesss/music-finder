import { Track, Playlist, PlaylistOptions } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

export async function searchTracks(query: string): Promise<Track[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/search?query=${encodeURIComponent(query)}`);
    
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error searching tracks:', error);
    throw error;
  }
}

export async function getTrackInfo(trackUrl: string): Promise<Track> {
  try {
    const response = await fetch(`${API_BASE_URL}/track-info`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ track_url: trackUrl }),
    });
    
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error getting track info:', error);
    throw error;
  }
}

export async function createPlaylist(
  seedTracks: Track[], 
  options: PlaylistOptions
): Promise<Playlist> {
  try {
    const response = await fetch(`${API_BASE_URL}/create-playlist`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        seed_tracks: seedTracks.map(track => track.permalink_url),
        duration_minutes: options.duration_minutes,
        transition_style: options.transition_style,
      }),
    });
    
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error creating playlist:', error);
    throw error;
  }
} 