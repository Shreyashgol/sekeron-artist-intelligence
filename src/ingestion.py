import os
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any
from pydantic import BaseModel
from src.media_selection import select_media, MediaItem

class ArtistProfileRecord(BaseModel):
    artist_id: str
    inferred_category: str
    profile_text: str
    media: List[MediaItem]
    missing_profile: bool = False
    corrupt_data: bool = False

def extract_docx_text(filepath: str) -> str:
    try:
        with zipfile.ZipFile(filepath) as z:
            xml_content = z.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            text = []
            for node in tree.iter():
                if node.tag.endswith('}t') and node.text:
                    text.append(node.text)
            return ' '.join(text).strip()
    except Exception:
        return ""

def scan_data_directory(data_dir: str = "data") -> List[ArtistProfileRecord]:
    profiles = []
    base_path = Path(data_dir) / "artist_profiles"
    
    if not base_path.exists():
        return profiles

    # Discover categories dynamically
    categories = [d for d in base_path.iterdir() if d.is_dir()]
    
    for category_path in categories:
        category_name = category_path.name
        
        # Enumerate artists inside category
        artist_dirs = [d for d in category_path.iterdir() if d.is_dir()]
        
        for artist_dir in artist_dirs:
            artist_id_raw = artist_dir.name.split('_')[0]
            
            # Find profile.docx
            profile_text = ""
            missing_profile = True
            
            # Use glob to find any .docx
            docx_files = list(artist_dir.rglob("*.docx"))
            if docx_files:
                profile_text = extract_docx_text(str(docx_files[0]))
                missing_profile = False
                
            # Find media
            media_files = []
            media_dir = artist_dir / "media"
            if media_dir.exists():
                media_files = [str(f.relative_to(Path(data_dir))) for f in media_dir.rglob("*") if f.is_file() and not f.name.startswith('.')]
            else:
                # Some folders might have media nested differently like Work/
                media_files = [str(f.relative_to(Path(data_dir))) for f in artist_dir.rglob("*") if f.is_file() and not f.name.startswith('.') and f.suffix.lower() != '.docx']
                
            selected_media = select_media(media_files, artist_id=artist_id_raw)
            
            # Basic corruption detection
            corrupt = missing_profile or len(selected_media) == 0
            
            profiles.append(ArtistProfileRecord(
                artist_id=artist_id_raw,
                inferred_category=category_name,
                profile_text=profile_text,
                media=selected_media,
                missing_profile=missing_profile,
                corrupt_data=corrupt
            ))
            
    return profiles

if __name__ == "__main__":
    records = scan_data_directory()
    print(f"Discovered {len(records)} artists.")
    for r in records:
        print(f"{r.artist_id} ({r.inferred_category}) - Media: {len(r.media)} - Corrupt: {r.corrupt_data}")

