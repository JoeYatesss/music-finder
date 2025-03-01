import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="w-full py-6 px-4 sm:px-6 lg:px-8 border-b border-gray-800">
      <div className="flex justify-between items-center">
        <div className="flex items-center">
          <div className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
            MusicFinder
          </div>
          <span className="ml-2 text-xs bg-gradient-to-r from-purple-500 to-pink-500 px-2 py-1 rounded-full text-white">
            DJ Edition
          </span>
        </div>
        <nav className="hidden md:flex space-x-6">
          <a href="#" className="text-gray-300 hover:text-white transition-colors">
            Home
          </a>
          <a href="#about" className="text-gray-300 hover:text-white transition-colors">
            About
          </a>
          <a href="#how-it-works" className="text-gray-300 hover:text-white transition-colors">
            How It Works
          </a>
        </nav>
        <div className="flex items-center space-x-4">
          <button className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-2 rounded-md hover:opacity-90 transition-opacity">
            Get Started
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header; 