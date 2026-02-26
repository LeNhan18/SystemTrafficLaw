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