# Music Finder - DJ Playlist Creator

A Next.js application that uses the SoundCloud API to find new music and create DJ playlists based on your tracks. The application features a Python backend with a custom algorithm for creating playlists with smooth transitions.

## Features

- Search for tracks on SoundCloud
- Select tracks to use as seeds for playlist generation
- Generate DJ playlists with different transition styles (smooth, energetic, minimal)
- Customize playlist duration
- Server-side processing for optimal performance

## Tech Stack

- **Frontend**:
  - Next.js 14
  - TypeScript
  - React
  - Tailwind CSS

- **Backend**:
  - Python
  - FastAPI
  - scikit-learn (for playlist algorithm)
  - pandas & numpy (for data processing)

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- SoundCloud API client ID (you'll need to register as a developer with SoundCloud)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/music-finder.git
   cd music-finder
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Set up Python environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   cd backend
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the `backend` directory:
   ```
   SOUNDCLOUD_CLIENT_ID=your_soundcloud_client_id_here
   ```

### Running the Application

You can use the development script to start both the frontend and backend:

```bash
chmod +x dev.sh  # Make the script executable (Unix/macOS only)
./dev.sh
```

Or start them separately:

1. Start the backend:
   ```bash
   cd backend
   source ../venv/bin/activate  # On Windows: ..\venv\Scripts\activate
   uvicorn main:app --reload --port 8000
   ```

2. Start the frontend:
   ```bash
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## How It Works

1. **Track Search**: Users search for tracks on SoundCloud using the search bar.
2. **Track Selection**: Users select tracks they like to use as seeds for playlist generation.
3. **Playlist Generation**: The backend algorithm analyzes the selected tracks and creates a playlist with smooth transitions.
4. **Playlist Display**: The generated playlist is displayed with track information and transition details.

## Playlist Algorithm

The playlist algorithm uses several factors to create optimal track transitions:

- BPM (Beats Per Minute) matching
- Key compatibility
- Energy level transitions
- Danceability matching

Different transition styles prioritize different aspects:
- **Smooth**: Minimizes BPM and energy differences
- **Energetic**: Creates more dynamic energy changes
- **Minimal**: Focuses on subtle, minimal transitions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- SoundCloud API for providing access to music data
- Next.js team for the amazing framework
- FastAPI for the efficient Python backend
