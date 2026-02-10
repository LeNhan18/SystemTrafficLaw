# SystemTrafficLaw
# Traffic Violation Detection System using Deep Learning

## Giới thiệu

Dự án này xây dựng hệ thống phát hiện hành vi vi phạm giao thông dựa trên Computer Vision, Deep Learning và Tracking. 

Hệ thống có khả năng:
- Phát hiện và theo dõi phương tiện giao thông 
- Phát hiện hành vi vượt đèn đỏ 
- Phát hiện không đội mũ bảo hiểm 
- Phát hiện chở quá số người quy định
- Tự động phát hiện khôi phục nhận diện biển số 
- Tự động chụp ảnh phương tiện vi phạm

Hệ thống được thiết kế theo kiến trúc nhiều mô hình (multi-model pipeline), phản ánh đúng quy trình của camera giao thông thông minh trong thực tế.

## Mục tiêu dự án

- Ứng dụng YOLO + Tracking + Segmentation vào bài toán giao thông
- Kết hợp nhiều mô hình AI cho các nhiệm vụ khác nhau
- Xây dựng pipeline xử lý hoàn chỉnh từ video → vi phạm → biển số
- Phục vụ mục đích nghiên cứu – học tập – demo hệ thống giám sát giao thông

## Kiến trúc tổng thể hệ thống

```
Camera / Video
      ↓
Model 1: Vehicle Detection + Tracking
      ↓
Phát hiện hành vi vi phạm (logic)
      ↓
Trigger Capture (chỉ khi vi phạm)
      ↓
Model 2: Helmet & People Detection
      ↓
Model 3: License Plate Detection
      ↓
Super Resolution / Deblur (nếu cần)
      ↓
OCR – Nhận dạng biển số
      ↓
Lưu DB & Xuất báo cáo vi phạm
```

## Các mô hình trong hệ thống

### Model 1 – Vehicle Detection & Tracking

**Nhiệm vụ**
- Phát hiện phương tiện và người tham gia giao thông
- Theo dõi đối tượng qua nhiều frame
- Phục vụ phát hiện hành vi vượt đèn đỏ

**Công nghệ**
- YOLOv8 (Detection hoặc Segmentation)
- DeepSORT / ByteTrack

**Class label**
- motorbike
- car
- person
- traffic_light (hoặc red_light / green_light)

**Output**
- Bounding box / mask
- Track ID
- Quỹ đạo di chuyển

### Model 2 – Helmet & Overloading Detection

**Nhiệm vụ**
- Phát hiện người đội mũ / không đội mũ
- Phát hiện hành vi chở quá số người

**Dữ liệu**
- Ảnh crop từ output Model 1 (xe máy + người)

**Class label**
- person
- helmet
- head (hoặc no_helmet)

**Logic vi phạm**

*Không đội mũ:*
- ≥ 3 frame liên tiếp không có helmet → vi phạm

*Chở quá số người:*
- 1 motorbike + số person > 2 → vi phạm

### Model 3 – License Plate Detection & Recognition

**Nhiệm vụ**
- Phát hiện biển số xe
- Khôi phục biển số bị mờ
- Nhận dạng ký tự biển số

**Pipeline**
```
YOLO detect plate
→ Crop plate
→ Super Resolution / Deblur (nếu mờ)
→ OCR (PaddleOCR / EasyOCR)
```

**Class label**
- license_plate

## Xử lý & tổ chức dữ liệu

### 1. Dữ liệu thô
- Video giao thông từ camera
- Trích xuất frame theo FPS phù hợp

### 2. Tiền xử lý
- Loại bỏ ảnh quá mờ (Laplacian variance)
- Resize ảnh về kích thước chuẩn
- Augmentation: flip, blur, noise

### 3. Annotation

**Lưu ý:** Các model dùng chung dữ liệu ảnh/video, **KHÔNG** dùng chung label

```
raw_images/
labels_model1/
labels_model2/
labels_model3/
```

## Chiến lược huấn luyện (Training Strategy)

### Fine-tuning
- Sử dụng pretrained YOLOv8
- Freeze backbone giai đoạn đầu
- Fine-tune head theo từng bài toán
- Batch size & learning rate điều chỉnh theo GPU

### Loss function
- YOLO default loss (box + cls + dfl)
- Mask loss (nếu dùng segmentation)

## Đánh giá mô hình (Evaluation Metrics)

### Detection / Segmentation
- Precision
- Recall
- mAP@0.5
- mAP@0.5:0.95
- IoU

### Tracking
- MOTA
- ID Switch
- FPS

### OCR
- Character Accuracy
- Plate-level Accuracy

## Cơ chế phát hiện & ghi nhận vi phạm

- Hệ thống chỉ chụp ảnh khi có vi phạm
- Mỗi lỗi là module độc lập
- Một phương tiện có thể vi phạm nhiều lỗi cùng lúc

**Ví dụ:**
```
Không vượt đèn đỏ ❌
Nhưng:
Không đội mũ bảo hiểm ✅
→ Vẫn ghi nhận vi phạm
```

## Kết quả đầu ra

- Ảnh phương tiện vi phạm
- Biển số đã nhận dạng
- Thời gian & loại vi phạm
- Dữ liệu sẵn sàng hiển thị dashboard hoặc báo cáo

## Hướng phát triển

- Nhận diện đi ngược chiều
- Nhận diện đi sai làn
- Tối ưu realtime (TensorRT)
- Kết nối hệ thống IoT / Smart City

## Công nghệ sử dụng

- Python
- YOLOv8
- OpenCV
- DeepSORT / ByteTrack
- PaddleOCR / EasyOCR
- ESRGAN / Real-ESRGAN
