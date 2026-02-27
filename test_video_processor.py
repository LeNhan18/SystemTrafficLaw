"""
Demo script showing how to use the new VideoProcessor
This replaces the old ConvertVideo.py with professional structure
"""

from src.backend.utils import VideoProcessor, setup_logger
import os

def main():
    # Setup logging
    logger = setup_logger("VideoDemo", "INFO")
    logger.info("Starting video processing demo...")
    
    # Initialize video processor
    processor = VideoProcessor()
    
    # Test with the original video path
    video_path = r"D:\nl\DatasetViPhamGiaoThong-20260211T113245Z-3-001\DatasetViPhamGiaoThong\Traffic062.mp4"
    
    if os.path.exists(video_path):
        print("=== TESTING SINGLE VIDEO ===")
        info = processor.get_video_info(video_path)
        
        if info['is_valid']:
            print(f"📹 File: {info['file_name']}")
            print(f"📐 Resolution: {info['resolution'][0]} x {info['resolution'][1]}")
            print(f"🎬 FPS: {info['fps']}")
            print(f"⏱️  Duration: {info['duration_seconds']} seconds")
            print(f"🎞️  Total Frames: {info['frame_count']}")
            print(f"📦 Codec: {info['codec']}")
            print(f"💾 Size: {info['file_size_mb']} MB")
            print(f"⚡ Recommended FPS for processing: {info['processing_recommended_fps']}")
        else:
            print(f"❌ Error: {info.get('error')}")
        
        # Test folder analysis  
        folder_path = os.path.dirname(video_path)
        if os.path.exists(folder_path):
            print("\n=== TESTING FOLDER ANALYSIS ===")
            videos = processor.analyze_video_folder(folder_path)
            print(f"Found {len(videos)} videos in folder")
            
            # Create summary
            video_paths = [v['file_path'] for v in videos if v.get('is_valid')]
            if video_paths:
                summary = processor.create_video_summary(video_paths)
                print("\n📊 DATASET SUMMARY:")
                print(f"• Total videos: {summary['total_videos']}")
                print(f"• Total duration: {summary['total_duration_minutes']} minutes")
                print(f"• Total size: {summary['total_size_mb']} MB")
                print(f"• Average FPS: {summary['avg_fps']}")
                print(f"• Most common resolution: {summary['resolution_stats']['most_common_resolution']}")
                print(f"• Estimated processing time: {summary['estimated_processing_time_minutes']} minutes")
        
    else:
        print("❗ Original video path not found. Testing with custom structure...")
        print("Place your videos in the storage/uploads/ directory for processing")
        
        # Show how to use with project structure
        project_root = os.path.dirname(os.path.abspath(__file__))
        uploads_dir = os.path.join(project_root, "storage", "uploads")
        
        print(f"📁 Check this directory for videos: {uploads_dir}")
        
        if os.path.exists(uploads_dir):
            videos = processor.analyze_video_folder(uploads_dir)
            if videos:
                print(f"Found {len(videos)} videos in uploads directory")
            else:
                print("No videos found in uploads directory")

    logger.info("Demo completed successfully!")

if __name__ == "__main__":
    main()