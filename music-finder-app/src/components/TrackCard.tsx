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

interface TrackCardProps {
  track: Track;
  onSelect: (track: Track) => void;
  isSelected: boolean;
}

const TrackCard: React.FC<TrackCardProps> = ({ track, onSelect, isSelected }) => {
  // Format duration from milliseconds to mm:ss
  const formatDuration = (ms: number) => {
    const totalSeconds = Math.floor(ms / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  // Use a default image if artwork_url is not available
  const artworkUrl = track.artwork_url || 'https://via.placeholder.com/100';

  return (
    <div 
      className={`
        relative p-4 rounded-lg transition-all duration-200 cursor-pointer
        ${isSelected 
          ? 'bg-gradient-to-r from-purple-900/50 to-pink-900/50 border border-purple-500' 
          : 'bg-gray-800/50 hover:bg-gray-800 border border-gray-700'}
      `}
      onClick={() => onSelect(track)}
    >
      <div className="flex items-center space-x-3">
        <div className="relative w-16 h-16 flex-shrink-0">
          <Image
            src={artworkUrl}
            alt={track.title}
            width={64}
            height={64}
            className="rounded-md object-cover"
          />
          {isSelected && (
            <div className="absolute inset-0 bg-purple-500/30 rounded-md flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
          )}
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="text-sm font-medium text-white truncate">{track.title}</h3>
          <p className="text-xs text-gray-400">{track.user.username}</p>
          <div className="flex items-center mt-1 space-x-2 text-xs text-gray-400">
            <span>{formatDuration(track.duration)}</span>
            {track.genre && <span>• {track.genre}</span>}
            {track.bpm && <span>• {track.bpm} BPM</span>}
          </div>
        </div>
      </div>
      <a 
        href={track.permalink_url} 
        target="_blank" 
        rel="noopener noreferrer"
        className="absolute bottom-2 right-2 text-xs text-gray-400 hover:text-white"
        onClick={(e) => e.stopPropagation()}
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
        </svg>
      </a>
    </div>
  );
};

export default TrackCard; 