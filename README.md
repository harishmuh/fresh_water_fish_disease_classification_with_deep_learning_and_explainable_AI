# Freshwater Fish Disease Classification Using Deep Learning and Explainable AI

![Banner](https://github.com/harishmuh/fresh_water_fish_disease_classification_with_deep_learning_and_explainable_AI/blob/main/figures/banner/banner.png?raw=true)

A deep learning study investigating multiclass freshwater fish disease image classification using transfer learning and explainable AI. Three pretrained CNN architectures were evaluated under a controlled experimental framework:

* ResNet50
* DenseNet121
* EfficientNetB0

The study examines overall classification performance, class-level performance, confusion patterns, misclassified images, and Grad-CAM visualizations. The resulting ResNet50 model was integrated into **FishScan7**, a Streamlit application for interactive image classification and model visualization.

**Web demo app:** https://fishscan7.streamlit.app/

## Research Objectives

This project aims to:

1. Characterize the freshwater fish disease image dataset through exploratory data analysis.
2. Develop a controlled transfer learning pipeline using pretrained CNN architectures.
3. Compare ResNet50, DenseNet121, and EfficientNetB0 using multiple classification metrics.
4. Investigate model errors and visual activation patterns using misclassified images and Grad-CAM.

## Dataset

The study uses the Freshwater Fish Disease Aquaculture in South Asia dataset from [Biswas et al. (2024)](https://ieeexplore.ieee.org/abstract/document/10759657). The dataset was made available by the author at this [link](https://www.kaggle.com/datasets/subirbiswas19/freshwater-fish-disease-aquaculture-in-south-asia)

The version analyzed in this project contains:

| Property | Description |
|---|---|
| Total images | 2,450 |
| Classes | 7 |
| Original training set | 1,750 |
| Independent test set | 700 |
| Training images per class | 250 |
| Test images per class | 100 |
| Input image size | 224 × 224 pixels |

The original test set was kept separate from model training and validation.

## Experimental Approach

The study uses pre-trained ImageNet CNN architectures under a common transfer learning framework.

| Configuration | Setting |
|---|---|
| Architectures | ResNet50, DenseNet121, EfficientNetB0 |
| Pretrained weights | ImageNet |
| Input size | 224 × 224 |
| Batch size | 32 |
| Maximum epochs | 20 |
| Optimizer | Adam |
| Learning rate | 1 × 10⁻⁴ |
| Loss | Sparse categorical crossentropy |
| Backbone | Frozen |
| Classification task | 7 class multiclass classification |

The original training data were divided into stratified training and validation subsets using an 80:20 split. The original test set remained independent for final evaluation.


## Results

The three architectures were evaluated on the same independent test set.

| Model | Accuracy | Macro F1 |
|---|---:|---:|
| ResNet50 | 96.86% | 96.85% |
| EfficientNetB0 | 93.14% | 93.13% |
| DenseNet121 | 85.43% | 85.35% |

ResNet50 produced the strongest performance under the frozen backbone configuration used in this study and was therefore selected as the model integrated into FishScan7.


## Explainable AI

Grad-CAM was used to visualize image regions that contributed strongly to the model predictions. The same test images were evaluated across ResNet50, DenseNet121, and EfficientNetB0 to compare their activation patterns. The analysis includes:

* correctly classified examples from each disease category
* comparison of activation patterns across architectures
* selected misclassified examples
* qualitative examination of model attention

Grad CAM is interpreted as a visualization of model activation and not as evidence of a biological disease location or causal mechanism.

## FishScan7 Web Application

The ResNet50 model selected from the comparative experiments was integrated into FishScan7, a Streamlit application for interactive freshwater fish disease image classification.

FishScan7 provides:

* sample image selection
* image upload
* predicted class
* model confidence
* class probabilities
* Grad-CAM visualization
* disease category information
* potential treatment information

### Live Application

https://fishscan7.streamlit.app/


## Repository Structure

```text
├── assets/
│   └── logo/
├── figures/
│   └── banner/
├── images/
│   └── samples/
├── model/
│   └── resnet50_fish_disease.keras
├── notebooks/
│   └── freshwater_fish_disease_classification.ipynb
├── app.py
├── config.py
├── disease_info.py
├── image_utils.py
├── model_utils.py
├── requirements.txt
├── ui.py
└── README.md
```

## Research Notebook

The complete experimental workflow is available in the research notebook → [Open research notebook](https://colab.research.google.com/drive/11NoGDAn1FLC3D3Arhtk4nJ9ArxbHK_Yb?usp=sharing)

The notebook covers:

* Dataset characterization
* Exploratory data analysis
* Train, validation, and test preparation
* Image preprocessing
* ResNet50 training
* DenseNet121 training
* EfficientNetB0 training
* Comparative evaluation
* Confusion matrix analysis
* Misclassified image analysis
* Grad-CAM explainability
* Discussion
* Limitations
* Future work

## Limitations

Several limitations should be considered when interpreting the results:

* The study uses a single public dataset, so performance may depend on its image quality, diversity, and label quality.
* The disease categories represent dataset labels and should not automatically be interpreted as laboratory-confirmed diagnoses.
* The pretrained CNN backbones were frozen, so the experiments represent a transfer learning baseline rather than a fully fine-tuned model.
* The model was evaluated on the dataset's independent test set and has not yet been externally validated on images from different farms, populations, or imaging conditions.
* Grad-CAM provides qualitative information about model activation and does not establish biological causality or confirm the true location of disease.

## Future Work

Potential improvements to this work include:

* Fine-tuning the ResNet50 backbone
* More systematic data augmentation
* Aspect ratio preserving image preprocessing
* Improved disease label validation
* Group based dataset splitting where source information is available
* External validation on independent datasets
* Disease localization using object detection or segmentation
* Larger scale explainability analysis
* Multi-label classification for images containing multiple pathological conditions
