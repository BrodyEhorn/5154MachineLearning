# Carabiner State Recognition

## Phase 2: Research & Planning

### 1. Literature Survey & Reference Summaries

**4.1 Main Reference — Enhancing Computer Image Recognition (Huang et al., 2024)**
- **Focus:** Improving image recognition in challenging environments (busy backgrounds, fluctuating lighting).
- **Core Strategy:** Modifying the ResNet34 architecture by replacing standard fully connected layers with $1\times1$ convolutions.
- **Results:** The approach achieved a peak recognition accuracy of 92.1% in unstructured outdoor environments.
- **Application to our Project:** This indicates ResNet34 is highly suitable as a foundational model. More specifically, the model's resilience to background noise perfectly maps onto outdoor carabiner use-cases where backgrounds are rarely uniform.

**4.2 Related Work 1 — Evaluation of Recognition Models (Gambino, 2023)**
- **Focus:** Benchmarking traditional machine learning (e.g., KNN) against deep learning (e.g., CNN).
- **Results:** Convolutional Neural Networks (CNN) and K-Nearest Neighbors (KNN) provided the most accurate classification.
- **Application to our Project:** Reinforces the decision to utilize a CNN-based architecture, justifying the specific use of ResNet34 over simpler non-deep-learning ML approaches for image-based classification.

**4.3 Related Work 2 — Fundamentals of Image Recognition (Baheti, 2022)**
- **Focus:** A high-level abstraction of the four pillars of computer vision (Classification, Detection, Tagging, Segmentation).
- **Key Challenges:** Successful implementations must account for real-world nuances like obstruction, viewpoint variations, and object scale.
- **Application to our Project:** Our project falls squarely under **Classification**. We must ensure that our dataset intentionally includes varying viewpoints, lighting conditions, and potential obstructions (like rope or hands) to build safely applicable model generalizations.

---

### 2. End-to-End Implementation Pipeline
1. **Image Scraping & Collection:** Use a programmatic approach (e.g., `duckduckgo-search` library) to query and download internet images of carabiners.
2. **Data Cleaning & Labeling:** Manually scrutinize images to filter out irrelevant or low-quality data. Organize the remaining images into target folders (`data/raw/open`, `data/raw/closed`).
3. **Preprocessing & Augmentation:** 
   - Resize images to 224x224 (ResNet34 standard).
   - Normalize tensor colors using standard ImageNet mean and deviation.
   - Apply data augmentations (flips, rotations, color jitters) to the training split to simulate real-world environmental variation.
4. **Transfer Learning (Frozen Head):** Freeze the ResNet34 convolutional network, instantiate a custom classification head for 2 classes, and initially train just the new head.
5. **Fine-Tuning (Unfrozen):** Unfreeze the entire model pipeline and train for additional epochs at a distinctly lower learning rate to optimize the full-feature extraction specifically for carabiners.
6. **Evaluation:** Evaluate comprehensively against a held-out test set using accuracy, precision, recall, and a confusion matrix. 

---

### 3. Final Class Labels Strategy
- `closed`: The carabiner is properly closed, and the gate/lock is fully secured.
- `open`: The gate is physically open, or the lock is not secured (partially open).

*Design Decision:* For safety analysis, any "partially open" carabiner poses the identical critical risk as a fully "open" one. Therefore, to maximize the safety constraints of the model, we will stick to a **binary classification mapping** (`closed` vs `open`), folding any partial states strictly into the `open` class to prevent false confidence.

---

### 4. Transfer Learning (ResNet34) Layer Strategy
- **Base Model Generation:** Load pre-trained ResNet34 (`torchvision.models`).
- **Phase 1 Training (Frozen):**
  - **Freeze:** All base Cov2D blocks and layers (`requires_grad = False`).
  - **Train:** The newly appended output layer that maps the final tensor features to `out_features=2`.
- **Phase 2 Training (Fine-Tuning):**
  - **Unfreeze:** Set `requires_grad = True` for all parameters.
  - **Train:** Train the entire network end-to-end using a scaled-down learning rate scheduler (e.g., `CosineAnnealingLR`) to incrementally adapt the ImageNet kernels for carabiner structures without catastrophically forgetting their base edge-detection prowess.
