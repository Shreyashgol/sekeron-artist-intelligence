import subprocess
import json
import base64
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def get_video_duration(video_path: str) -> float:
    try:
        cmd = [
            'ffprobe', '-v', 'error', '-show_entries',
            'format=duration', '-of',
            'default=noprint_wrappers=1:nokey=1', video_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        logger.error(f"Failed to get video duration for {video_path}: {e}")
        return 0.0

def extract_representative_frames(video_path: str, num_frames: int = 3) -> List[Dict[str, str]]:
    """
    Extracts num_frames from the video deterministically spaced out.
    Returns a list of dicts with 'timestamp' and 'base64_image'.
    """
    duration = get_video_duration(video_path)
    if duration <= 0:
        return []

    # Calculate timestamps to sample (avoiding very beginning and very end if possible)
    # e.g., for 3 frames, we might take them at 25%, 50%, and 75% of the video duration.
    if num_frames == 1:
        timestamps = [duration / 2]
    else:
        timestamps = [duration * (i + 1) / (num_frames + 1) for i in range(num_frames)]

    frames = []
    for ts in timestamps:
        try:
            cmd = [
                'ffmpeg', '-ss', str(ts), '-i', video_path,
                '-vframes', '1', '-f', 'image2pipe', '-vcodec', 'mjpeg', '-loglevel', 'error', '-'
            ]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            b64_img = base64.b64encode(result.stdout).decode('utf-8')
            
            # Format timestamp as MM:SS
            m, s = divmod(int(ts), 60)
            formatted_ts = f"{m:02d}:{s:02d}"
            
            frames.append({
                "timestamp": formatted_ts,
                "base64_image": b64_img
            })
        except Exception as e:
            logger.error(f"Failed to extract frame at {ts} from {video_path}: {e}")

    return frames
