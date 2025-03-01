'use client';

import { useState } from 'react';
import Header from '../components/Header';
import SearchBar from '../components/SearchBar';
import TrackCard from '../components/TrackCard';
import PlaylistGenerator from '../components/PlaylistGenerator';
import PlaylistDisplay from '../components/PlaylistDisplay';
import { searchTracks, createPlaylist } from '../utils/api';
import { Track, Playlist, PlaylistOptions } from '../types';

export default function Home() {
  const [searchResults, setSearchResults] = useState<Track[]>([]);
  const [selectedTracks, setSelectedTracks] = useState<Track[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedPlaylist, setGeneratedPlaylist] = useState<Playlist | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (query: string) => {
    setError(null);
    setIsSearching(true);
    try {
      const results = await searchTracks(query);
      setSearchResults(results);
    } catch (err) {
      setError('Failed to search tracks. Please try again.');
      console.error(err);
    } finally {
      setIsSearching(false);
    }
  };

  const handleTrackSelect = (track: Track) => {
    setSelectedTracks(prev => {
      // If track is already selected, remove it
      if (prev.some(t => t.id === track.id)) {
        return prev.filter(t => t.id !== track.id);
      }
      // Otherwise add it
      return [...prev, track];
    });
  };

  const handleGeneratePlaylist = async (options: PlaylistOptions) => {
    setError(null);
    setIsGenerating(true);
    try {
      const playlist = await createPlaylist(selectedTracks, options);
      setGeneratedPlaylist(playlist);
    } catch (err) {
      setError('Failed to generate playlist. Please try again.');
      console.error(err);
    } finally {
      setIsGenerating(false);
    }
  };

  const closePlaylist = () => {
    setGeneratedPlaylist(null);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-1 container mx-auto px-4 py-8">
        <section className="mb-12 text-center">
          <h1 className="text-4xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
            Find Music & Create DJ Playlists
          </h1>
          <p className="text-gray-300 max-w-2xl mx-auto">
            Search for tracks on SoundCloud, select your favorites, and let our algorithm create the perfect DJ playlist with smooth transitions.
          </p>
        </section>
        
        <section className="mb-12">
          <SearchBar onSearch={handleSearch} isLoading={isSearching} />
        </section>
        
        {error && (
          <div className="mb-8 p-4 bg-red-900/30 border border-red-800 rounded-lg text-red-200">
            {error}
          </div>
        )}
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <h2 className="text-xl font-bold mb-4 text-white">Search Results</h2>
            
            {isSearching ? (
              <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
              </div>
            ) : searchResults.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {searchResults.map(track => (
                  <TrackCard 
                    key={track.id} 
                    track={track} 
                    onSelect={handleTrackSelect}
                    isSelected={selectedTracks.some(t => t.id === track.id)}
                  />
                ))}
              </div>
            ) : (
              <div className="bg-gray-800/50 rounded-lg p-8 text-center">
                <p className="text-gray-400">
                  Search for tracks to see results here
                </p>
              </div>
            )}
          </div>
          
          <div>
            <PlaylistGenerator 
              selectedTracks={selectedTracks}
              onGenerate={handleGeneratePlaylist}
              isGenerating={isGenerating}
            />
            
            {selectedTracks.length > 0 && (
              <div className="mt-6">
                <h3 className="text-lg font-medium mb-3 text-white">Selected Tracks</h3>
                <div className="space-y-2 max-h-96 overflow-y-auto pr-2">
                  {selectedTracks.map(track => (
                    <div 
                      key={track.id} 
                      className="flex items-center p-2 bg-gray-800/50 rounded-lg"
                    >
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-white truncate">{track.title}</p>
                        <p className="text-xs text-gray-400">{track.user.username}</p>
                      </div>
                      <button 
                        onClick={() => handleTrackSelect(track)}
                        className="ml-2 text-gray-400 hover:text-red-500"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
      
      <footer className="py-6 border-t border-gray-800">
        <div className="container mx-auto px-4 text-center text-gray-400 text-sm">
          <p>© {new Date().getFullYear()} MusicFinder DJ Edition. Powered by SoundCloud API.</p>
        </div>
      </footer>
      
      {generatedPlaylist && (
        <PlaylistDisplay playlist={generatedPlaylist} onClose={closePlaylist} />
      )}
    </div>
  );
}
