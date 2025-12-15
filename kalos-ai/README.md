# Kalos AI

## Project Goal (Week 1)
Build a local clothing detection pipeline and establish a clear data schema for training.

## Structure
- `data/`: Raw and processed datasets (DeepFashion2, ModaNet)
- `models/`: YOLOv8 detection and segmentation models
- `notebooks/`: Experiments for detection, segmentation, and color extraction
- `src/`: Core logic for the pipeline

## Setup
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Verify GPU:
   ```python
   import torch
   torch.cuda.is_available()
   ```

## Tasks
- [ ] Data Collection & Mapping
- [ ] Wardrobe Schema Definition
- [ ] YOLOv8 Baseline Inference
- [ ] Fine-tuning
