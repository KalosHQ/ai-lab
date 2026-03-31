# COMMENTED OUT - Not needed for foundation (ML data conversion for training)
# import json
# import os
# import shutil
# from pathlib import Path

# # --- CONFIG ---
# # Base paths
# base_data_dir = "data/modanet_yolo"
# json_base_dir = f"{base_data_dir}/images/datasets/modanet/annotations"
# src_img_dir = f"{base_data_dir}/images/images/datasets/coco/images" # Where they are currently buried
# dst_img_base = f"{base_data_dir}/images"     # Target: images/train, images/val
# dst_label_base = f"{base_data_dir}/labels"   # Target: labels/train, labels/val

# # Splits to process
# splits = [
#     ("train", "modanet2018_instances_train.json"),
#     ("val", "modanet2018_instances_val.json")
# ]

# # MVP Mapping: ModaNet ID -> YOLO ID (5 Classes)
# # 1: bag, 3: shoes, 4: dress, 5: shoes, 6: top, 8: top, 9: bottom, 10: bottom, 11: top, 12: top, 13: shoes
# mapping = {
#     1: 4,  # bag
#     3: 3,  # footwear -> shoes
#     4: 2,  # dress
#     5: 3,  # hosiery -> shoes
#     6: 0,  # jacket -> top
#     8: 0,  # outer -> top
#     9: 1,  # pants -> bottom
#     10: 1, # skirt -> bottom
#     9: 1,  # pants -> bottom
#     10: 1, # skirt -> bottom
#     11: 0, # top
#     12: 0, # scarf -> top
#     13: 3  # boots -> shoes
# }

# def convert():
#     print(f"Starting conversion...")
    
#     # Ensure source images exist
#     if not os.path.exists(src_img_dir):
#         print(f"❌ Error: Source image directory not found: {src_img_dir}")
#         return

#     total_images_moved = 0
#     total_labels_written = 0

#     for split_name, json_file in splits:
#         json_path = os.path.join(json_base_dir, json_file)
#         print(f"\nProcessing {split_name} from {json_path}...")
        
#         if not os.path.exists(json_path):
#             print(f"⚠️ Warning: JSON not found: {json_path}. Skipping.")
#             continue

#         with open(json_path) as f:
#             data = json.load(f)

#         # Create target directories
#         target_img_dir = os.path.join(dst_img_base, split_name)
#         target_label_dir = os.path.join(dst_label_base, split_name)
#         os.makedirs(target_img_dir, exist_ok=True)
#         os.makedirs(target_label_dir, exist_ok=True)

#         # Index annotations by image_id
#         img_id_to_ann = {}
#         for ann in data['annotations']:
#             image_id = ann['image_id']
#             if image_id not in img_id_to_ann:
#                 img_id_to_ann[image_id] = []
#             img_id_to_ann[image_id].append(ann)

#         print(f"Found {len(data['images'])} images in JSON.")
        
#         count = 0
#         for img in data['images']:
#             fname = img['file_name']
#             img_id = img['id']
            
#             # 1. Move Image
#             src_path = os.path.join(src_img_dir, fname)
#             dst_path = os.path.join(target_img_dir, fname)
            
#             # Check if image exists in source (or already in dest)
#             if os.path.exists(src_path):
#                 shutil.move(src_path, dst_path)
#                 total_images_moved += 1
#             elif os.path.exists(dst_path):
#                # Already moved, skip copy
#                 pass
#             else:
#                 # Image missing completely
#                 # print(f"Missing image: {fname}") 
#                 continue 

#             # 2. Generate Label
#             # Only if we have annotations
#             if img_id in img_id_to_ann:
#                 base_name = os.path.splitext(fname)[0]
#                 label_path = os.path.join(target_label_dir, f"{base_name}.txt")
                
#                 # YOLO Normalization
#                 dw = 1. / img['width']
#                 dh = 1. / img['height']
                
#                 has_labels = False
#                 with open(label_path, 'w') as f: # 'w' to overwrite/create fresh
#                     for ann in img_id_to_ann[img_id]:
#                         if ann['category_id'] in mapping:
#                             yolo_id = mapping[ann['category_id']]
#                             x, y, w, h = ann['bbox'] # [x, y, w, h]
                            
#                             x_center = (x + w / 2) * dw
#                             y_center = (y + h / 2) * dh
#                             w_norm = w * dw
#                             h_norm = h * dh
                            
#                             f.write(f"{yolo_id} {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}\n")
#                             has_labels = True
                
#                 if has_labels:
#                     total_labels_written += 1
#                 else:
#                     # If empty file (no mapped classes), maybe delete it? 
#                     # Ultralytics handles empty files as background images.
#                     pass 
            
#             count += 1
#             if count % 1000 == 0:
#                 print(f"Processed {count} images...")

#     print(f"\n✅ Complete. Moved {total_images_moved} images. Generated {total_labels_written} label files.")

# if __name__ == "__main__":
#     convert()
