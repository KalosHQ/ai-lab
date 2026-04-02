import os
import gdown

MODELS = {
    "models/smplx/SMPLX_NEUTRAL.npz": "1-c9G-hKXEdspheiqqw6sg8F94Y9QDEwD",
    "models/smplx/SMPLX_MALE.npz": "1BTKP8OB0PbXBh2Po7E1s7WXY2Ty-lnNr",
    "models/smplx/SMPLX_FEMALE.npz": "1oo2VFrbnszyhzYDeVkXTwMmsXejd-ps4",
}

def download_models():
    for path, file_id in MODELS.items():
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            print(f"Downloading {path}...")
            gdown.download(f"https://drive.google.com/uc?id={file_id}", path, quiet=False)
            print(f"✅ {path} downloaded.")