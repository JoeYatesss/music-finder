export interface Track {
  id: string;
  title: string;
  user: {
    username: string;
  };
  artwork_url: string;
  duration: number;
  permalink_url: string;
  genre?: string;
  bpm?: number;
}

export interface Playlist {
  name: string;
  tracks: Track[];
  duration_seconds: number;
  transition_style: string;
  track_count: number;
}

export interface PlaylistOptions {
  duration_minutes: number;
  transition_style: 'smooth' | 'energetic' | 'minimal';
} 