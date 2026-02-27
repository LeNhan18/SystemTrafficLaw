"""
Video Processing Utilities for Traffic Law System
Handles video analysis, frame extraction, and preprocessing
"""

import cv2
import os
import numpy as np
from typing import Dict, List, Tuple, Optional, Generator
from pathlib import Path
import logging


class VideoProcessor:
    """Professional video processing class for traffic violation detection"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._get_default_config()
        self.logger = logging.getLogger(__name__)
        
    def _get_default_config(self) -> Dict:
        """Default configuration for video processing"""
        return {
            'supported_formats': ['.mp4', '.avi', '.mov', '.mkv', '.wmv'],
            'target_fps': 15,  # FPS for processing (reduce for performance)
            'max_resolution': (1920, 1080),  # Max resolution for processing
            'blur_threshold': 100.0,  # Laplacian variance threshold for blur detection
            'quality_check': True,
            'auto_resize': True
        }
    
    def get_video_info(self, video_path: str) -> Dict:
        """
        Get comprehensive video information
        Enhanced version of original ConvertVideo.py functionality
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
            
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
        
        try:
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
            
            # Get codec information
            codec = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])
            
            # Calculate duration
            duration = frame_count / fps if fps > 0 else 0
            
            # File information
            file_size = os.path.getsize(video_path)
            file_name = os.path.basename(video_path)
            
            video_info = {
                'file_name': file_name,
                'file_path': video_path,
                'file_size_mb': round(file_size / (1024 * 1024), 2),
                'fps': fps,
                'resolution': (width, height),
                'frame_count': frame_count,
                'duration_seconds': round(duration, 2),
                'codec': codec,
                'fourcc': fourcc,
                'is_valid': True,
                'processing_recommended_fps': min(fps, self.config['target_fps'])
            }
            
            self.logger.info(f"Video info extracted: {file_name} - {width}x{height} @ {fps}fps")
            return video_info
            
        except Exception as e:
            self.logger.error(f"Error getting video info: {str(e)}")
            return {'is_valid': False, 'error': str(e)}
        finally:
            cap.release()
    
    def analyze_video_folder(self, folder_path: str) -> List[Dict]:
        """
        Enhanced version of the commented code in ConvertVideo.py
        Analyze all videos in a folder and return comprehensive information
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")
        
        video_files = []
        supported_formats = tuple(self.config['supported_formats'])
        
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith(supported_formats):
                video_path = os.path.join(folder_path, file_name)
                video_info = self.get_video_info(video_path)
                video_files.append(video_info)
        
        self.logger.info(f"Found {len(video_files)} video files in {folder_path}")
        return video_files
    
    def extract_frames(self, video_path: str, output_dir: str, 
                      frame_interval: Optional[int] = None,
                      start_second: float = 0, 
                      end_second: Optional[float] = None) -> List[str]:
        """
        Extract frames from video for ML processing
        Returns list of saved frame paths
        """
        os.makedirs(output_dir, exist_ok=True)
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Calculate frame extraction parameters
        if frame_interval is None:
            frame_interval = max(1, int(fps / self.config['target_fps']))
        
        start_frame = int(start_second * fps)
        end_frame = int(end_second * fps) if end_second else total_frames
        
        saved_frames = []
        frame_count = 0
        
        try:
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            
            while True:
                ret, frame = cap.read()
                if not ret or frame_count >= end_frame:
                    break
                
                current_frame = start_frame + frame_count
                
                # Extract frame at specified intervals
                if frame_count % frame_interval == 0:
                    # Quality check
                    if self.config['quality_check'] and self._is_blurry(frame):
                        self.logger.debug(f"Skipping blurry frame {current_frame}")
                        frame_count += 1
                        continue
                    
                    # Auto resize if needed
                    if self.config['auto_resize']:
                        frame = self._resize_frame(frame)
                    
                    # Save frame
                    frame_filename = f"frame_{current_frame:06d}.jpg"
                    frame_path = os.path.join(output_dir, frame_filename)
                    
                    cv2.imwrite(frame_path, frame)
                    saved_frames.append(frame_path)
                    
                    self.logger.debug(f"Saved frame: {frame_filename}")
                
                frame_count += 1
            
            self.logger.info(f"Extracted {len(saved_frames)} frames from {os.path.basename(video_path)}")
            return saved_frames
            
        finally:
            cap.release()
    
    def _is_blurry(self, frame: np.ndarray) -> bool:
        """Check if frame is too blurry using Laplacian variance"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        variance = cv2.Laplacian(gray, cv2.CV_64F).var()
        return variance < self.config['blur_threshold']
    
    def _resize_frame(self, frame: np.ndarray) -> np.ndarray:
        """Resize frame to target resolution while maintaining aspect ratio"""
        height, width = frame.shape[:2]
        max_width, max_height = self.config['max_resolution']
        
        if width <= max_width and height <= max_height:
            return frame
        
        # Calculate scaling factor
        scale = min(max_width / width, max_height / height)
        
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        return cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    def create_video_summary(self, video_paths: List[str]) -> Dict:
        """Create summary statistics for multiple videos"""
        if not video_paths:
            return {}
        
        summaries = [self.get_video_info(path) for path in video_paths]
        valid_videos = [s for s in summaries if s.get('is_valid')]
        
        if not valid_videos:
            return {'error': 'No valid videos found'}
        
        total_duration = sum(v['duration_seconds'] for v in valid_videos)
        total_frames = sum(v['frame_count'] for v in valid_videos)
        total_size_mb = sum(v['file_size_mb'] for v in valid_videos)
        
        resolutions = [v['resolution'] for v in valid_videos]
        fps_values = [v['fps'] for v in valid_videos]
        
        return {
            'total_videos': len(valid_videos),
            'total_duration_minutes': round(total_duration / 60, 2),
            'total_frames': total_frames,
            'total_size_mb': round(total_size_mb, 2),
            'avg_fps': round(np.mean(fps_values), 2),
            'resolution_stats': {
                'unique_resolutions': list(set(resolutions)),
                'most_common_resolution': max(set(resolutions), key=resolutions.count)
            },
            'estimated_processing_time_minutes': round(total_duration / 60 * 0.5, 2)  # Rough estimate
        }


def main():
    """Test function - replica of original ConvertVideo.py behavior"""
    processor = VideoProcessor()
    
    # Test with specific video (from original code)
    video_path = r"D:\nl\DatasetViPhamGiaoThong-20260211T113245Z-3-001\DatasetViPhamGiaoThong\Traffic062.mp4"
    
    if os.path.exists(video_path):
        info = processor.get_video_info(video_path)
        print("=== VIDEO INFO ===")
        print(f"FPS: {info['fps']}")
        print(f"Resolution: {info['resolution'][0]} x {info['resolution'][1]}")
        print(f"Total Frames: {info['frame_count']}")
        print(f"Duration: {info['duration_seconds']} seconds")
        print(f"Codec: {info['codec']}")
    else:
        print("Video file not found - testing with sample data structure")


if __name__ == "__main__":
    main()