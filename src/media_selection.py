import os
from pathlib import Path
from typing import List, Dict, Optional, Any
from pydantic import BaseModel

class MediaItem(BaseModel):
    source_path: str
    artist_id: str
    media_type: str
    sampled_timestamps: Optional[List[str]] = None
    selection_reason: str

def get_media_type(filename: str) -> str:
    ext = filename.lower().split('.')[-1]
    if ext in ['jpg', 'jpeg', 'png', 'webp']:
        return 'image'
    elif ext in ['mp4', 'mov', 'avi']:
        return 'video'
    elif ext in ['mp3', 'wav', 'aac']:
        return 'audio'
    return 'unknown'

def select_media(media_files: List[str], artist_id: str) -> List[MediaItem]:
    selected = []
    
    # Sort files to ensure deterministic selection
    sorted_files = sorted(media_files)
    
    for f in sorted_files:
        mtype = get_media_type(f)
        if mtype == 'image':
            selected.append(MediaItem(
                source_path=f,
                artist_id=artist_id,
                media_type=mtype,
                sampled_timestamps=None,
                selection_reason="All portfolio images are selected for comprehensive review."
            ))
        elif mtype == 'video':
            selected.append(MediaItem(
                source_path=f,
                artist_id=artist_id,
                media_type=mtype,
                sampled_timestamps=["00:00:05", "00:00:15", "00:00:25"], # Deterministic sample representation
                selection_reason="Sampled early, mid, and late frames for pacing, transition, and style analysis."
            ))
        elif mtype == 'audio':
            selected.append(MediaItem(
                source_path=f,
                artist_id=artist_id,
                media_type=mtype,
                sampled_timestamps=["00:00:10", "00:00:30"], # Deterministic representation
                selection_reason="Sampled representative segments for genre, mood, and vocal characteristics."
            ))
            
    return selected
