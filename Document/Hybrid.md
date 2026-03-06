# Tại sao annotations này dùng tốt cho ViT?

Roboflow hỗ trợ export cho Transformer models: Roboflow có hướng dẫn cụ thể về labeling và export dataset cho Vision Transformer training (ví dụ: guide "How to label data for Vision Transformer training" trên Roboflow). Dataset của bạn (object detection format: COCO JSON, YOLO TXT, hoặc Pascal VOC) có thể export dễ dàng sang định dạng phù hợp cho ViT-based detectors như DETR, RT-DETR, hoặc ViT fine-tune cho detection.
Classes head/helmet/person lý tưởng:
Head và helmet là small/fine-grained objects → ViT mạnh ở global attention, giúp capture context tốt hơn (ví dụ: helmet overlap với head trong cảnh đông đúc, occlusion mưa như ảnh Ung Văn Khiêm của bạn).
Person làm context để associate rider với xe (dễ integrate post-processing logic infer no-helmet).
Nhiều paper 2025–2026 dùng dataset tương tự (hard-hat workers, helmet detection trên Roboflow Universe) để train ViT hoặc hybrid: Ví dụ, YOLOv10 + ViT/Swin Transformer backbone cho helmet monitoring trên construction/traffic, đạt mAP cao hơn baseline CNN (như Swin transformer đạt AP50 96.55% cho safety helmets trong surveillance images).

Dataset size 2240 ảnh: ViT gốc cần data lớn, nhưng với pretrained ViT (từ Hugging Face: google/vit-base-patch16-224) hoặc variants như DeiT/Swin-Tiny/MobileViT, fine-tune trên 2240 ảnh custom là khả thi (Roboflow có notebook train ViT classification trên custom data, dễ adapt sang detection). Paper 2025 dùng ViT cho helmet detection với dataset tương tự (Roboflow hard-hat hoặc custom traffic) đạt kết quả tốt.