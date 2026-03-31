# COMMENTED OUT - Not needed for foundation (ML data splitting)
# import os
# import shutil
# import random
# import glob

# # Config
# BASE_DIR = "data/modanet_yolo"
# IMG_TRAIN = os.path.join(BASE_DIR, "images/train")
# IMG_VAL = os.path.join(BASE_DIR, "images/val")
# LABEL_TRAIN = os.path.join(BASE_DIR, "labels/train")
# LABEL_VAL = os.path.join(BASE_DIR, "labels/val")
# SPLIT_RATIO = 0.2  # 20% for validation

# def split_dataset():
#     # Ensure val dirs exist
#     os.makedirs(IMG_VAL, exist_ok=True)
#     os.makedirs(LABEL_VAL, exist_ok=True)

#     # Get all images in train
#     # Assuming jpg extension, checking both jpg and JPG
#     images = glob.glob(os.path.join(IMG_TRAIN, "*.jpg")) + glob.glob(os.path.join(IMG_TRAIN, "*.JPG"))
    
#     total_images = len(images)
#     if total_images == 0:
#         print("❌ No images found in images/train to split.")
#         return

#     # Shuffle
#     random.seed(42) # Reproducibility
#     random.shuffle(images)

#     # Calculate split index
#     val_count = int(total_images * SPLIT_RATIO)
#     val_images = images[:val_count]
    
#     print(f"Total Images: {total_images}")
#     print(f"Moving {val_count} images (20%) to validation set...")

#     moved_count = 0
#     for img_path in val_images:
#         basename = os.path.basename(img_path)
#         name_no_ext = os.path.splitext(basename)[0]
        
#         # Define paths
#         src_img = img_path
#         dst_img = os.path.join(IMG_VAL, basename)
        
#         src_label = os.path.join(LABEL_TRAIN, f"{name_no_ext}.txt")
#         dst_label = os.path.join(LABEL_VAL, f"{name_no_ext}.txt")
        
#         # Move Image
#         shutil.move(src_img, dst_img)
        
#         # Move Label (if exists)
#         if os.path.exists(src_label):
#             shutil.move(src_label, dst_label)
        
#         moved_count += 1
#         if moved_count % 1000 == 0:
#             print(f"Moved {moved_count}...")

#     print(f"✅ Successfully created validation set with {moved_count} images.")

# if __name__ == "__main__":
#     split_dataset()
