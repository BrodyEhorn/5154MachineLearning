# Project Overview: Carabiner State Recognition
**Author:** Brody Ehorn
**Academic Focus:** Machine Learning and Computer Image Recognition

---

## 1. Problem Statement
In safety-critical environments such as industrial job sites or rock climbing, the "seemingly correct" state of safety equipment can lead to fatal accidents due to human oversight. Specifically, a carabiner may appear closed at a cursory glance but remain unlocked or partially open.

The goal of this project is to develop a machine learning model capable of successfully distinguishing between two primary states of a carabiner: **Open** or **Closed**.

---

## 2. Motivation
The primary motivation stems from personal engagement in high-stakes hobbies such as indoor/outdoor climbing and slacklining/highlining. In these activities, gear misuse can be life-threatening.

Current safety protocols in high-risk scenarios (like highlining) recommend a "second set of eyes" to verify that every piece of gear is utilized correctly. This project aims to create a digital "double-check" system that could potentially save the lives of individuals venturing alone by identifying incorrectly secured gear.

---

## 3. Methodology & Technical Approach
The project will utilize **Transfer Learning** to achieve high accuracy with a custom dataset.

* **Model Architecture:** The project will employ **ResNet34**, a proven pre-trained image recognition model.
* **Adaptation:** The model will first be adapted to recognize carabiners as a general object class before being specifically trained to classify the "Open" vs. "Closed" states.
* **Data Collection:** Due to the lack of existing large-scale carabiner datasets, a custom dataset of a few hundred images will be collected from the internet.
* **Data Diversity:** The dataset will include carabiners in varying positions, covering Open, Closed, and Partially Open states.

---

## 4. Research & Literature Survey

### 4.1 Main Reference — Enhancing Computer Image Recognition (Huang et al., 2024)
The core research focuses on improving image recognition algorithms, particularly for challenging environments where traditional approaches struggle.

* **Challenges:** Traditional image recognition often struggles with busy backgrounds and fluctuating lighting.
* **Architecture:** The study focuses on improving the **ResNet34** model specifically for unstructured outdoor environments.
* **Technical Modification:** The standard fully connected layers are replaced with $1\times1$ convolutions.
* **Performance:** This approach achieved a peak recognition accuracy of 92.1%.
* **Repository:** Reference implementation available at `https://github.com/laringying88/EnhancingImage.git`.

**Application to this project:**
* **Distinction:** The use of regression methods is helpful for accurately distinguishing between the closed and open states of a carabiner.
* **Environment:** The model's ability to handle background noise is essential for the outdoor environments where carabiners are typically used.

### 4.2 Related Work 1 — Evaluation of Recognition Models (Gambino, 2023)
This study compared the accuracy of traditional machine learning against deep learning using a dataset of handwritten numbers. It provides detailed insights into training methods and project workflows.

* **Models Tested:** The evaluation included KNN, CNN, BPNN, and DBN.
* **Conclusion:** CNN and KNN were found to be the most accurate, which supports the choice of a CNN-based architecture like **ResNet34** for this project.

### 4.3 Related Work 2 — Fundamentals of Image Recognition (Baheti, 2022)
Image recognition is defined as a specific category within the broader field of computer vision. This reference offers a high-level abstraction of the image recognition process to make the implementation more approachable.

* **Four Pillars of Computer Vision:**
    1. Classification
    2. Detection
    3. Tagging
    4. Segmentation
* **Real-World Implementation Issues:** Effective models must account for several variables, including obstruction, viewpoint variation, and object variation.

---

## 5. Project Phases

---

### Phase 1: Environment Setup
**Goal:** Establish a reproducible, working development environment before any code is written.

- Install Python (3.10+) and create a virtual environment (`venv` or `conda`).
- Install core dependencies: `torch`, `torchvision`, `numpy`, `pandas`, `matplotlib`, `Pillow`, `scikit-learn`.
- Create the standard project directory structure:
  ```
  project/
  ├── data/
  │   ├── raw/
  │   │   ├── open/
  │   │   └── closed/
  │   └── processed/
  ├── models/
  ├── notebooks/
  ├── src/
  └── scripts/
  ```
- Set up a `requirements.txt` or `pyproject.toml` to lock dependency versions.
- Initialize a Git repository and connect to GitHub.

**Deliverable:** A clean project skeleton with all dependencies installed and a working Python environment.

---

### Phase 2: Research & Planning
**Goal:** Deeply understand the problem domain and design the full implementation pipeline before writing any ML code.

- Read and summarize all three academic references from Section 4.
- Map out the end-to-end pipeline: image scraping → preprocessing → training → evaluation → deployment.
- Decide on final class labels: `open`, `closed`, and optionally `partial`.
- Determine which ResNet34 layers to freeze vs. fine-tune.
- Document design decisions in a planning notebook or README section.

**Deliverable:** A written pipeline plan and annotated notes from each reference paper.

---

### Phase 3: Data Collection & Labeling
**Goal:** Build a quality, labeled image dataset large enough to train a reliable classifier.

- Write a scraping script using `duckduckgo-search` or similar to query images of carabiners.
- Download images and sort them manually into `data/raw/open/` and `data/raw/closed/`.
- Remove duplicates, corrupt files, and irrelevant images.
- Target at least **150–200 images per class** (300–400 total minimum).
- Document label definitions: what constitutes "open" vs. "closed" vs. "partial."

**Deliverable:** A labeled, cleaned dataset organized in the correct folder structure, ready for preprocessing.

---

### Phase 4: Data Preprocessing & Augmentation
**Goal:** Transform raw images into a format suitable for model input, and expand the dataset artificially to improve generalization.

- Resize all images to a consistent size (e.g., 224×224 for ResNet34 compatibility).
- Normalize pixel values using ImageNet mean and standard deviation.
- Split the dataset: **70% train / 10% validation / 20% test** — keep the test set completely held out.
- Apply augmentation to the training split only:
  - Random horizontal/vertical flips
  - Random rotation (up to 30°)
  - Color jitter (brightness, contrast, saturation)
  - Random cropping and resizing
- Use `torchvision.transforms` or `albumentations` for the pipeline.

**Deliverable:** A `DataLoader`-ready dataset with augmentation applied to training data only.

---

### Phase 5: Model Training — Transfer Learning (Frozen)
**Goal:** Train only the classification head on the new dataset, using ResNet34's pre-learned feature extraction.

- Load pre-trained ResNet34 weights from `torchvision.models`.
- Freeze all convolutional layers (set `requires_grad = False`).
- Replace the final fully connected layer with a new 2-class output head.
- Train for **5–10 epochs** using:
  - Loss: Cross-Entropy
  - Optimizer: AdamW
  - Learning Rate: ~1e-3
- Monitor training and validation loss/accuracy each epoch.
- Save the best checkpoint by validation accuracy.

**Deliverable:** A trained classification head checkpoint and logged training metrics.

---

### Phase 6: Model Fine-Tuning (Unfrozen)
**Goal:** Refine the full model end-to-end to specialize on carabiner classification.

- Load the best checkpoint from Phase 5.
- Unfreeze all model layers.
- Reduce the learning rate significantly (e.g., ~1e-4 or lower).
- Continue training for **10–15 additional epochs**.
- Use a learning rate scheduler (e.g., `CosineAnnealingLR`) to avoid overshooting.
- Save the best checkpoint by validation accuracy.

**Deliverable:** A fully fine-tuned model checkpoint that outperforms the frozen-head version.

---

### Phase 7: Evaluation & Analysis
**Goal:** Rigorously test the model's performance on unseen data, with special attention to safety-critical failure modes.

- Evaluate on the held-out **test set** (never seen during training or fine-tuning).
- Report the following metrics:
  - Accuracy
  - Precision, Recall, F1 Score (per class)
- Generate and analyze a **confusion matrix**.
  - Pay particular attention to false negatives: predicting *closed* when the carabiner is actually *open* is the most dangerous error.
- Test on "Partially Open" images to understand the model's decision boundary.
- Visualize attention maps or grad-CAM outputs to understand what the model focuses on.

**Deliverable:** A full evaluation report with metrics, confusion matrix, and failure mode analysis.

---

### Phase 8: Results Visualization & Presentation
**Goal:** Display model results clearly and produce all final presentation deliverables.

- Build a simple results dashboard (e.g., Jupyter notebook) that displays:
  - Training and validation loss/accuracy curves over epochs.
  - The confusion matrix from the test set evaluation.
  - Per-class Precision, Recall, and F1 Score.
  - A sample grid of correctly and incorrectly classified images from the test set.
- Write the final project report covering: methodology, dataset details, results, and limitations.
- Design presentation slides following the rubric in Section 6.

**Deliverable:** A results visualization notebook/dashboard, a final written report, and a presentation slide deck exported as PDF.

---

## 6. Presentation Requirements

The project will be presented as a **recorded video (5–10 minutes)**. Do not exceed 10 minutes.

### Submission Checklist
- [ ] Recorded video (sharable link)
- [ ] Slide deck exported as **PDF**
- [ ] Video link included on the **first page** of the PDF slides

### Required Slide Content
The presentation must cover the following topics in order:

1. **Problem & Challenges** — Define the carabiner classification problem and explain why it is difficult (background noise, orientation variation, subtle state differences, etc.).
2. **Motivation** — Explain the personal and safety-critical motivation for automating gear state detection.
3. **Existing Related Approaches** — Summarize the three papers from Section 4 and how they inform this project.
4. **Method** — Describe the approach being duplicated/adapted: ResNet34 transfer learning, dataset construction, training strategy.
5. **Results & Observations** — Present accuracy, precision/recall/F1, confusion matrix, and any notable patterns or failure modes observed.
6. **Conclusion & Future Work** — Summarize what was achieved and what could be improved or expanded (e.g., a larger dataset, live video inference, more fine-grained states).

> **Note:** If the project is incomplete by the deadline, present what has been completed and clearly state what results are expected but not yet obtained.