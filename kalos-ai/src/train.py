# COMMENTED OUT - Not needed for foundation (ML model training)
# import argparse
# from ultralytics import YOLO

# def train(epochs, device_name):
#     print(f"Starting training on {device_name}...")
    
#     # Load a model
#     model = YOLO("yolov8n.pt")  # build a new model from scratch or load pretrained

#     # Train the model
#     # data arg points to the yaml file in root
#     model.train(data="modanet.yaml", epochs=epochs, device=device_name)
    
#     print("Training complete.")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Train model")
#     parser.add_argument("--epochs", type=int, default=1, help="Number of epochs")
#     parser.add_argument("--device", type=str, default="cpu", help="Device (cpu or cuda)")
    
#     args = parser.parse_args()
    
#     train(args.epochs, args.device)
