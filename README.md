# Kalos AI Lab

Experimental lab for building a clothing detection and segmentation pipeline for Kalos. This repository contains the training logic, experiments, and data processing scripts required to fine-tune YOLOv8 models on fashion datasets (DeepFashion2, ModaNet).

## Features
- **Clothing Detection**: YOLOv8 pipeline to identify clothing items.
- **Segmentation**: Pixel-level segmentation for wardrobe analysis.
- **Hybrid Workflow**: Develop locally (CPU), train on Google Colab (GPU).

## Project Structure
- `src/`: core training and utility scripts.
- `notebooks/`: Jupyter notebooks for experiments and Colab training.
- `models/`: Checkpoints and exported models (gitignored).
- `data/`: Datasets (gitignored).

## Setup

### Prerequisites
- Python 3.8+
- [Optional] CUDA-enabled GPU for local training

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/kalos-app/ai-lab.git
   cd ai-lab/kalos-ai
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Local Development (CPU)
Run the training script locally to verify logic before pushing to Colab.
```bash
python src/train.py --epochs 1 --device cpu
```

### Remote Training (Google Colab)
1. Commit and push your changes to GitHub.
2. Open `notebooks/colab_train.ipynb` in Google Colab.
3. Run the notebook cells to pull the latest code and start training on a T4/A100 GPU.
   ```python
   !python src/train.py --epochs 100 --device cuda
   ```
