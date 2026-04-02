import os
import gdown

MODELS = {
    "models/smplx/SMPLX_NEUTRAL.npz": "1-c9G-hKXEdspheiqqw6sg8F94Y9QDEwD",
    "models/smplx/SMPLX_MALE.npz": "1BTKP8OB0PbXBh2Po7E1s7WXY2Ty-lnNr",
    "models/smplx/SMPLX_FEMALE.npz": "1oo2VFrbnszyhzYDeVkXTwMmsXejd-ps4",
}

def download_models():
    """Download SMPL-X models from Google Drive if they don't exist.
    
    Returns:
        bool: True if all models are available (either already existed or downloaded),
              False if any models are missing.
    """
    all_available = True
    for path, file_id in MODELS.items():
        if not os.path.exists(path):
            all_available = False
            os.makedirs(os.path.dirname(path), exist_ok=True)
            print(f"Downloading {path}...")
            try:
                gdown.download(f"https://drive.google.com/uc?id={file_id}", path, quiet=False)
                print(f"✅ {path} downloaded.")
            except Exception as e:
                print(f"⚠️ Failed to download {path}: {e}")
                print("   You can manually download from: https://drive.google.com/uc?id={file_id}")
                print("   Or get models from: https://smpl-x.is.tue.mpg.de/")
    return all_available
