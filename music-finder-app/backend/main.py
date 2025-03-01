from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import httpx
import os
from dotenv import load_dotenv
import json
from playlist_algorithm import create_dj_playlist

# Load environment variables
load_dotenv()

app = FastAPI(title="Music Finder API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SoundCloud API client ID (you'll need to get this from SoundCloud)
SOUNDCLOUD_CLIENT_ID = os.getenv("SOUNDCLOUD_CLIENT_ID")
if not SOUNDCLOUD_CLIENT_ID:
    raise ValueError("SOUNDCLOUD_CLIENT_ID environment variable is not set")

class TrackRequest(BaseModel):
    track_url: str

class PlaylistRequest(BaseModel):
    seed_tracks: List[str]
    duration_minutes: Optional[int] = 60
    transition_style: Optional[str] = "smooth"  # smooth, energetic, minimal

@app.get("/")
async def root():
    return {"message": "Music Finder API is running"}

@app.post("/api/track-info")
async def get_track_info(request: TrackRequest):
    """Get information about a track from SoundCloud"""
    try:
        async with httpx.AsyncClient() as client:
            # Resolve the track URL to get the track ID
            resolve_url = f"https://api.soundcloud.com/resolve?url={request.track_url}&client_id={SOUNDCLOUD_CLIENT_ID}"
            response = await client.get(resolve_url)
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to resolve track URL")
            
            track_data = response.json()
            return track_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching track info: {str(e)}")

@app.post("/api/search")
async def search_tracks(query: str):
    """Search for tracks on SoundCloud"""
    try:
        async with httpx.AsyncClient() as client:
            search_url = f"https://api.soundcloud.com/tracks?q={query}&client_id={SOUNDCLOUD_CLIENT_ID}&limit=20"
            response = await client.get(search_url)
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to search tracks")
            
            tracks = response.json()
            return tracks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching tracks: {str(e)}")

@app.post("/api/create-playlist")
async def generate_playlist(request: PlaylistRequest):
    """Generate a DJ playlist based on seed tracks"""
    try:
        # Get track details for each seed track
        track_details = []
        async with httpx.AsyncClient() as client:
            for track_url in request.seed_tracks:
                resolve_url = f"https://api.soundcloud.com/resolve?url={track_url}&client_id={SOUNDCLOUD_CLIENT_ID}"
                response = await client.get(resolve_url)
                
                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail=f"Failed to resolve track URL: {track_url}")
                
                track_data = response.json()
                track_details.append(track_data)
        
        # Generate playlist using our algorithm
        playlist = create_dj_playlist(
            track_details, 
            duration_minutes=request.duration_minutes,
            transition_style=request.transition_style
        )
        
        return playlist
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating playlist: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 