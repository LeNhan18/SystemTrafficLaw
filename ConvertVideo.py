"""
DEPRECATED: This file has been moved to src/backend/utils/video_processor.py

For the new professional video processing functionality, use:
    from src.backend.utils import VideoProcessor
    
Or run the demo:
    python test_video_processor.py

Original functionality maintained below for reference:
"""

# ========== ORIGINAL CODE (DEPRECATED) ==========
# import cv2
# import os
# folder = r"D:\nl\DatasetViPhamGiaoThong-20260211T113245Z-3-001\DatasetViPhamGiaoThong"
# for file in os.listdir(folder):
#     if file.endswith((".avi",".mp4", ".mov")):
#         video_path = os.path.join(folder, file)
#         cap = cv2.VideoCapture(video_path)
#         fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
#         codec = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])
#
#         print(f"{file} → Codec: {codec}")
#         cap.release()

# ========== NEW RECOMMENDED USAGE ==========

# Import the new video processor
try:
    from src.backend.utils import VideoProcessor, setup_logger
    
    def main():
        """Use the new VideoProcessor class instead of raw OpenCV code"""
        processor = VideoProcessor()
        
        # Original video path
        video_path = r"D:\nl\DatasetViPhamGiaoThong-20260211T113245Z-3-001\DatasetViPhamGiaoThong\Traffic062.mp4"
        
        # Get comprehensive video info (replaces the original code)
        info = processor.get_video_info(video_path)
        
        if info['is_valid']:
            print("=== NEW ENHANCED OUTPUT ===")
            print(f"FPS: {info['fps']}")
            print(f"Resolution: {info['resolution'][0]} x {info['resolution'][1]}")
            print(f"Total Frames: {info['frame_count']}")
            print(f"Duration: {info['duration_seconds']} seconds")
            print(f"Codec: {info['codec']}")
            print(f"File Size: {info['file_size_mb']} MB")
            
            print("\n🚀 TIP: Use test_video_processor.py for more features!")
        else:
            print(f"Error: {info.get('error')}")
    
    if __name__ == "__main__":
        main()
        
except ImportError:
    # Fallback to original code if new structure not available
    print("⚠️  New video processor not available. Using original code...")
    
    import cv2
    import os

    video_path = r"D:\nl\DatasetViPhamGiaoThong-20260211T113245Z-3-001\DatasetViPhamGiaoThong\Traffic062.mp4"

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    print("FPS:", fps)
    print("Resolution:", int(width), "x", int(height))
    print("Total Frames:", int(frame_count))

    cap.release()