import React from 'react';
import Image from 'next/image';

interface Track {
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

interface Playlist {
  name: string;
  tracks: Track[];
  duration_seconds: number;
  transition_style: string;
  track_count: number;
}

interface PlaylistDisplayProps {
  playlist: Playlist;
  onClose: () => void;
}

const PlaylistDisplay: React.FC<PlaylistDisplayProps> = ({ playlist, onClose }) => {
  // Format duration from seconds to hh:mm:ss
  const formatDuration = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        <div className="p-6 border-b border-gray-800 flex justify-between items-center">
          <h2 className="text-xl font-bold text-white">{playlist.name}</h2>
          <button 
            onClick={onClose}
            className="text-gray-400 hover:text-white"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div className="p-6">
          <div className="flex flex-wrap gap-4 mb-6">
            <div className="bg-gray-800 rounded-lg px-4 py-2 text-sm">
              <span className="text-gray-400">Tracks:</span> 
              <span className="ml-1 font-bold text-white">{playlist.track_count}</span>
            </div>
            <div className="bg-gray-800 rounded-lg px-4 py-2 text-sm">
              <span className="text-gray-400">Duration:</span> 
              <span className="ml-1 font-bold text-white">{formatDuration(playlist.duration_seconds)}</span>
            </div>
            <div className="bg-gray-800 rounded-lg px-4 py-2 text-sm">
              <span className="text-gray-400">Style:</span> 
              <span className="ml-1 font-bold text-white capitalize">{playlist.transition_style}</span>
            </div>
          </div>
        </div>
        
        <div className="overflow-y-auto flex-1 p-6 pt-0">
          <div className="space-y-1">
            {playlist.tracks.map((track, index) => (
              <div key={`${track.id}-${index}`} className="flex items-center p-3 rounded-lg hover:bg-gray-800/50 transition-colors">
                <div className="flex-shrink-0 w-8 text-center text-gray-500 font-mono">{index + 1}</div>
                <div className="flex-shrink-0 w-10 h-10 ml-2">
                  <Image
                    src={track.artwork_url || 'https://via.placeholder.com/40'}
                    alt={track.title}
                    width={40}
                    height={40}
                    className="rounded object-cover"
                  />
                </div>
                <div className="ml-3 flex-1 min-w-0">
                  <p className="text-sm font-medium text-white truncate">{track.title}</p>
                  <p className="text-xs text-gray-400 truncate">{track.user.username}</p>
                </div>
                <div className="flex-shrink-0 text-xs text-gray-400">
                  {formatDuration(track.duration / 1000)}
                </div>
                <a 
                  href={track.permalink_url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="ml-4 text-gray-400 hover:text-white"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                  </svg>
                </a>
              </div>
            ))}
          </div>
        </div>
        
        <div className="p-6 border-t border-gray-800">
          <div className="flex justify-between">
            <button 
              onClick={onClose}
              className="px-4 py-2 border border-gray-700 rounded-md text-gray-300 hover:bg-gray-800 transition-colors"
            >
              Close
            </button>
            <button className="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-md text-white hover:opacity-90 transition-opacity">
              Export Playlist
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlaylistDisplay; 