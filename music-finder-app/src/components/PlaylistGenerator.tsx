import React, { useState } from 'react';

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

interface PlaylistGeneratorProps {
  selectedTracks: Track[];
  onGenerate: (options: PlaylistOptions) => void;
  isGenerating: boolean;
}

interface PlaylistOptions {
  duration_minutes: number;
  transition_style: 'smooth' | 'energetic' | 'minimal';
}

const PlaylistGenerator: React.FC<PlaylistGeneratorProps> = ({ 
  selectedTracks, 
  onGenerate,
  isGenerating
}) => {
  const [options, setOptions] = useState<PlaylistOptions>({
    duration_minutes: 60,
    transition_style: 'smooth'
  });

  const handleOptionChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setOptions(prev => ({
      ...prev,
      [name]: name === 'duration_minutes' ? parseInt(value) : value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onGenerate(options);
  };

  return (
    <div className="bg-gray-800/70 rounded-lg p-6 border border-gray-700">
      <h2 className="text-xl font-bold mb-4 text-white">Generate DJ Playlist</h2>
      
      <div className="mb-4">
        <p className="text-gray-300 mb-2">Selected Tracks: <span className="font-bold">{selectedTracks.length}</span></p>
        {selectedTracks.length === 0 && (
          <p className="text-sm text-red-400">Please select at least one track to generate a playlist</p>
        )}
      </div>
      
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="duration_minutes" className="block text-sm font-medium text-gray-300 mb-1">
            Playlist Duration (minutes)
          </label>
          <input
            type="range"
            id="duration_minutes"
            name="duration_minutes"
            min="30"
            max="180"
            step="10"
            value={options.duration_minutes}
            onChange={handleOptionChange}
            className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
          />
          <div className="flex justify-between text-xs text-gray-400 mt-1">
            <span>30m</span>
            <span>{options.duration_minutes}m</span>
            <span>180m</span>
          </div>
        </div>
        
        <div className="mb-6">
          <label htmlFor="transition_style" className="block text-sm font-medium text-gray-300 mb-1">
            Transition Style
          </label>
          <select
            id="transition_style"
            name="transition_style"
            value={options.transition_style}
            onChange={handleOptionChange}
            className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="smooth">Smooth</option>
            <option value="energetic">Energetic</option>
            <option value="minimal">Minimal</option>
          </select>
        </div>
        
        <button
          type="submit"
          disabled={selectedTracks.length === 0 || isGenerating}
          className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white py-3 rounded-md font-medium hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isGenerating ? (
            <div className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Generating Playlist...
            </div>
          ) : (
            'Generate DJ Playlist'
          )}
        </button>
      </form>
    </div>
  );
};

export default PlaylistGenerator; 