# SystemTrafficLaw
Traffic Violation Detection System using Instance Segmentation
Giới thiệu
Dự án xây dựng hệ thống giám sát giao thông thông minh sử dụng Computer Vision và Deep Learning nhằm tự động phát hiện hành vi vi phạm giao thông từ hình ảnh/video, xác định biển số phương tiện vi phạm và hỗ trợ khôi phục ảnh biển số mờ trong điều kiện thực tế tại Việt Nam.
Hệ thống tập trung vào các lỗi vi phạm phổ biến của xe máy, phù hợp với hạ tầng camera giao thông hiện nay.
Mục tiêu dự án
Mục tiêu tổng quát

Ứng dụng Instance Segmentation, Object Detection và OCR để xây dựng một pipeline hoàn chỉnh có khả năng:

Phát hiện hành vi vi phạm giao thông

Tự động trích xuất và nhận dạng biển số phương tiện

Nâng cao chất lượng ảnh biển số phục vụ nhận dạng
Mục tiêu cụ thể

Nhận diện chính xác các đối tượng giao thông trong môi trường phức tạp

Phát hiện các hành vi vi phạm giao thông phổ biến

Xây dựng logic xác định vi phạm dựa trên mối quan hệ không gian giữa các đối tượng

Nhận dạng biển số phương tiện vi phạm

Khôi phục ảnh biển số bị mờ bằng Generative AI

Xây dựng hệ thống có khả năng mở rộng cho bài toán thực tế

Các hành vi vi phạm được phát hiện

Không đội mũ bảo hiểm
Vượt đèn đỏ
Chở quá số người quy định (tống 3)
Dừng xe sai vạch (mở rộng)
Kiến trúc tổng thể hệ thống
Video / Image Input
        ↓
YOLO Instance Segmentation
        ↓
Rule-based Violation Detection
        ↓
License Plate Detection (YOLO)
        ↓
Crop License Plate
        ↓
Image Enhancement (GAN - nếu mờ)
        ↓
OCR License Plate
        ↓
Violation Result Output

Các mô hình sử dụng
🔹 Model 1 – Instance Segmentation

Mục đích: Phát hiện đối tượng và phân biệt từng instance riêng biệt

Công nghệ:

YOLO Seg (YOLOv8 / YOLO11 / YOLOv12)

Classes chính:

motorcycle

person

helmet

head

traffic_light_red

stop_line

🔹 Model 2 – License Plate Detection

Mục đích: Phát hiện vùng biển số phương tiện vi phạm

Công nghệ:

YOLO Object Detection

Class:

license_plate

🔹 Model 3 – Image Enhancement (Nâng cao – tùy chọn)

Mục đích: Khôi phục ảnh biển số mờ, nhiễu

Công nghệ:

Real-ESRGAN / DeblurGAN

🔹 Model 4 – OCR

Mục đích: Nhận dạng ký tự biển số

Công nghệ:

PaddleOCR / VietOCR

(Nâng cao: detect từng ký tự bằng YOLO + CNN)

⚙️ Công nghệ sử dụng
Thành phần	Công nghệ
Ngôn ngữ	Python
Deep Learning	PyTorch
Computer Vision	OpenCV
Model CV	YOLO Seg, YOLO Detection
Annotation	Roboflow
OCR	PaddleOCR / VietOCR
Image Enhancement	GAN (Real-ESRGAN)
Dataset	Image & Video giao thông Việt Nam
Gán nhãn dữ liệu (Annotation)

Công cụ: Roboflow

Loại nhãn:

Instance Segmentation cho đối tượng giao thông

Bounding Box cho biển số

Hỗ trợ:

Annotation Group

Gán nhãn tiếng Việt
 Output hệ thống

Hình ảnh/video có bounding box & mask

Thông tin:

Loại vi phạm

Biển số phương tiện
