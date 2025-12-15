import argparse
import time
import torch

def train(epochs, device_name):
    print(f"Starting training on {device_name}...")
    
    if torch.cuda.is_available():
        if device_name == 'cuda':
            print(f"Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("CUDA available but using CPU as requested/default.")
    else:
        print("CUDA not available. Using CPU.")

    device = torch.device(device_name if torch.cuda.is_available() else "cpu")
    print(f"Device set to: {device}")

    # Simulated training loop
    for epoch in range(1, epochs + 1):
        print(f"Epoch {epoch}/{epochs}")
        # Simulate work
        time.sleep(0.5) 
        
    print("Training complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train model")
    parser.add_argument("--epochs", type=int, default=1, help="Number of epochs")
    parser.add_argument("--device", type=str, default="cpu", help="Device (cpu or cuda)")
    
    args = parser.parse_args()
    
    train(args.epochs, args.device)
