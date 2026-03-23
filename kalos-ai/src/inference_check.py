from ultralytics import YOLO
import sys

def run_check():
    print("🚀 Starting Data Integrity Check...")
    print("Loading YOLOv8n model...")
    model = YOLO("yolov8n.pt")

    print("\n🧐 Validating dataset (1 batch only for speed)...")
    # val() will try to load images and labels from modanet.yaml
    # We set batches=1 to just check if it crashes on data loading
    try:
        # Note: 'checks' won't provide meaningful mAP on untrained model, 
        # but it WILL fail if images/labels are corrupt or missing.
        results = model.val(data="modanet.yaml", device="cpu", batch=4, imgsz=320, plots=False) 
        print("✅ Validation check passed! Data loaded successfully.")
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        sys.exit(1)

    print("\n💨 Running Inference on a sample image...")
    # Just grab an image from val
    import glob
    import os
    val_images = glob.glob("data/modanet_yolo/images/val/*.jpg")
    if val_images:
        test_img = val_images[0]
        print(f"Testing on: {test_img}")
        model.predict(test_img, show=False)
        print("✅ Inference check passed!")
    else:
        print("⚠️ No validation images found to test inference.")

if __name__ == "__main__":
    run_check()
