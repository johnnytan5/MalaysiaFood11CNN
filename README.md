# Malaysia Food CNN Classifier

WID3011 Deep Learning — Individual Assignment
CNN-Based Image Classifier for Malaysian Product Recognition

---

## Overview

A deep learning project comparing a custom CNN built from scratch against a fine-tuned ResNet-50 on a self-collected 15-class Malaysian food dataset. Includes data preparation with class-imbalance handling, architecture analysis, transfer learning comparison, and misclassification reflection.

---

## Dataset

- **15 Malaysian food categories** (ais_kacang, asam_pedas, ayam_masak_merah, bak_kut_teh, curry_laksa, hokkien_mee, kuih_seri_muka, mee_rebus, murtabak, nasi_dagang, nasi_kerabu, otak_otak, pau, popiah, roti_tisu)
- **3,139 images total** (154–255 per class, mild imbalance ~1.65×)
- Self-collected via Bing Image Search using `icrawler`
- Handled with `WeightedRandomSampler` for balanced training batches

---

## Project Structure

```
.
├── assignment.ipynb       # Main notebook (Parts A–D)
├── scrape.py              # Dataset collection script
├── requirements.txt       # Python dependencies
├── result/                # All generated visualizations
│   ├── class_distribution.png
│   ├── augmentation_examples.png
│   ├── sample_grid.png
│   ├── cnn_learning_curves.png
│   ├── cnn_confusion_matrix.png
│   ├── resnet_confusion_matrix.png
│   ├── comparison_learning_curves.png
│   └── misclassified_samples.png
└── README.md
```

---

## Notebook Sections

| Part | Section | Content |
|---|---|---|
| **A** | Dataset Preparation | Class distribution, imbalance strategy, train/val/test split (70/15/15), augmentation pipeline, sample grid |
| **B** | CNN Architecture Design | Custom CNN (4 conv blocks), parameter count, layer shapes, receptive field analysis, training, learning curves |
| **C** | Transfer Learning | Fine-tune ResNet-50 (2-phase), comparison table, side-by-side learning curves |
| **D** | Analysis & Reflection | Misclassification analysis (1 per class), proposed data improvement, Malaysian SME business application |

---

## How to Run

### 1. Clone and set up environment

```bash
git clone https://github.com/johnnytan5/MalaysiaFood11CNN.git
cd MalaysiaFood11CNN

# Create conda environment (recommended for Apple Silicon)
conda create -n deeplearning python=3.11 -y
conda activate deeplearning

# Install dependencies
pip install -r requirements.txt
```

### 2. Collect dataset

The dataset is not included in this repo due to size. Run the scraper:

```bash
python scrape.py
```

This will download 15 food categories to `data/raw/` via Bing Image Search.

### 3. Run the notebook

```bash
# Register kernel (optional)
python -m ipykernel install --user --name deeplearning --display-name "Deep Learning"

# Launch Jupyter
jupyter notebook assignment.ipynb
```

Run all cells sequentially. The notebook auto-detects device:
- **MPS** (Apple Silicon Mac)
- **CUDA** (NVIDIA GPU, Colab/RunPod/Lightning AI)
- **CPU** (fallback)

### 4. Run on Google Colab

Set `USE_GOOGLE_DRIVE = True` in the first cell, then upload the dataset zip to your Drive and update `DATASET_DIR`.

---

## Results Summary

| Metric | Custom CNN | ResNet-50 (Fine-tuned) |
|---|---|---|
| Test Accuracy | 50.42% | **91.74%** |
| Training Time | 18.5 min | 41.8 min |
| Parameters | 26.1M | 23.5M |
| Convergence | ~29 epochs | ~15 epochs |

ResNet-50 with transfer learning significantly outperforms the custom CNN, demonstrating the value of pretrained ImageNet features for low-data domains.

---

## Key Techniques

- **Data augmentation:** Resize, RandomHorizontalFlip, RandomRotation, ColorJitter, RandomResizedCrop
- **Class imbalance handling:** WeightedRandomSampler
- **Regularisation:** BatchNorm, Dropout (0.5)
- **Transfer learning:** Two-phase fine-tuning (FC head → layer3/4 unfreeze)
- **Evaluation:** Confusion matrix, per-class F1, misclassification analysis

---

## Author

**Tan Hao Wen**
3rd Year Artificial Intelligence Student
University of Malaya

WID3011 — Semester Break Assignment
