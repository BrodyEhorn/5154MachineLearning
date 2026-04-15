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

## 5. Project Roadmap

### Step 1: Research & Design
- Conduct an in-depth review of the three core academic references listed in Section 4.
- Map out the full pipeline from raw image data to final classification output.
- Identify which ResNet34 layers will be frozen vs. fine-tuned during transfer learning.
- Define the exact class labels to be used: `open`, `closed`, and optionally `partial`.

### Step 2: Data Acquisition
- Write a scraping script (e.g., using `duckduckgo-search`) to collect carabiner images from the web.
- Manually review and label each image, placing them in `data/raw/open` and `data/raw/closed` directories.
- Remove duplicate, corrupt, or irrelevant images.
- Target a minimum of 150–200 images per class.

### Step 3: Development I — General Training
- Load the pre-trained ResNet34 weights from `torchvision.models`.
- Freeze all layers except the final classification head.
- Replace the fully connected layer with a two-class output head.
- Train for 5–10 epochs using Cross-Entropy loss and an AdamW optimizer.

### Step 4: Development II — Specialized Fine-Tuning
- Unfreeze the full model and reduce the learning rate significantly (e.g., by 10x).
- Apply data augmentation: random crops, horizontal/vertical flips, color jitter, and rotation.
- Continue training for an additional 10–15 epochs, saving the best checkpoint by validation accuracy.

### Step 5: Evaluation
- Run the model against a held-out test set (20% of total data).
- Report Accuracy, Precision, Recall, and F1 Score.
- Generate a confusion matrix and analyze false negatives specifically (open predicted as closed).
- Test on edge-case "Partially Open" images to probe decision boundaries.

### Step 6: Finalization
- Write the final project report documenting methodology, results, and limitations.
- Design presentation slides summarizing the problem, approach, and key findings.
- Package the model with a simple `streamlit` or `gradio` demo for live inference.

---

## 6. Implementation Instructions

To develop this machine learning project, follow these structured steps:

### Step 1: Environment & Directory Setup
* **Dependencies**: Initialize a Python environment. Core libraries should include `torch`, `torchvision`, `numpy`, `pandas`, `matplotlib`, `Pillow`, and optionally `scikit-learn` or `fastai`.
* **Scaffolding**: Create standard project directories (`/data`, `/src`, `/notebooks`, `/models`, `/scripts`).

### Step 2: Data Acquisition & Preprocessing
* **Image Scraping Script**: Write a script (e.g., using `duckduckgo-search` or `BeautifulSoup`) to scrape images of carabiners.
* **Data Structure**: Organize scraped images into classification folders: `data/raw/open` and `data/raw/closed`.
* **Cleaning**: Provide a utility to identify and remove corrupt or non-image files, and filter out irrelevant images.
* **Augmentation**: Implement data transformations (random cropping, rotations, flipping, and brightness/contrast adjustments) to mimic various real-world lighting conditions and carabiner orientations.

### Step 3: Model Training
* **Base Model Configuration**: Load a pre-trained **ResNet34** model structure. Ensure the initial convolution layers are frozen to leverage transfer learning.
* **Custom Head**: Replace the fully connected classification layer with a new one that targets two classes: Open and Closed.
* **Training Loop**: Set up the training loop using an appropriate loss function (like Cross-Entropy) and an optimizer (like AdamW). Use a learning rate finder to select optimal starting rates. Unfreeze the full model for fine-tuning after initial training of the custom head.

### Step 4: Evaluation & Validation
* **Metrics**: Calculate and report Accuracy, Precision, Recall, and the F1 Score.
* **Confusion Matrix**: Output a confusion matrix to identify false positives vs. false negatives. Note that failing to detect an open carabiner (predicting closed when open) is the most dangerous failure mode and should be minimized.
* **Edge Case Analysis**: Test the model on "Partially Open" states to evaluate its boundaries.

### Step 5: Interface / Deployment
* **Demo App**: Provide a simple web interface script (using `streamlit` or `gradio`) where users can upload an image of a carabiner and instantly see the model's prediction.