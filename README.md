
# Multi-Class Cancer Classification Using Gene Expression

## Project Overview

This project develops a machine learning system for multi-class cancer classification using high-dimensional gene-expression data.

The objective is to classify biological samples into five cancer categories based on their gene-expression profiles. The final model uses a Linear Support Vector Machine (Linear SVM) combined with feature reduction, feature selection, and standardization.

## Cancer Classes

The model classifies samples into the following five cancer types:

- BRCA — Breast Invasive Carcinoma
- COAD — Colon Adenocarcinoma
- KIRC — Kidney Renal Clear Cell Carcinoma
- LUAD — Lung Adenocarcinoma
- PRAD — Prostate Adenocarcinoma

---

# Dataset

| Property | Value |
|---|---:|
| Total Samples | 801 |
| Original Gene Features | 20,531 |
| Cancer Classes | 5 |

## Class Distribution

| Cancer Type | Number of Samples |
|---|---:|
| BRCA | 300 |
| KIRC | 146 |
| LUAD | 141 |
| PRAD | 136 |
| COAD | 78 |

---

# Machine Learning Pipeline

The complete machine learning pipeline was designed to perform preprocessing, feature reduction, feature selection, scaling, and classification.

```text
Gene Expression Data
        ↓
VarianceThreshold
(Remove Constant Features)
        ↓
SelectKBest
(ANOVA F-Test Feature Selection)
        ↓
StandardScaler
        ↓
Linear Support Vector Machine
        ↓
Cancer Classification

Keeping preprocessing steps inside the Scikit-learn pipeline helps prevent data leakage during cross-validation and model evaluation.

Feature Reduction and Selection

Gene-expression datasets contain extremely high-dimensional data. The original dataset contained 20,531 gene-expression features, which is substantially larger than the number of samples.

Therefore, dimensionality reduction was performed in two stages.

Stage 1: Variance Threshold

Constant features that contained no useful variation were removed using VarianceThreshold.

Original Features: 20,531
Constant Features Removed: 277
Remaining Features: 20,254
Stage 2: Feature Selection

The ANOVA F-test was used through SelectKBest to identify the most informative genes for cancer classification.

Features Before Selection: 20,254
Final Selected Genes: 250
Feature Reduction Summary
Stage	Number of Features
Original Gene Features	20,531
After Variance Threshold	20,254
Final Selected Genes	250

This significantly reduced the dimensionality of the dataset while maintaining excellent classification performance.

Train-Test Split

The dataset was divided into training and testing datasets using a stratified train-test split.

Dataset	Samples
Training Set	640
Testing Set	161
Total	801

A duplicate check confirmed that there were no exact duplicate samples between the training and testing datasets.

Exact Train-Test Duplicate Samples: 0
Final Model

The final machine learning pipeline consists of:

Component	Method
Constant Feature Removal	VarianceThreshold
Feature Selection	SelectKBest
Selection Method	ANOVA F-Test
Selected Features	250 Genes
Feature Scaling	StandardScaler
Classification Algorithm	LinearSVC
Random State	42
Model Comparison

Multiple models were evaluated during the project.

Model	Test Accuracy
Logistic Regression	99.38%
250-Gene Linear SVM	100.00%

The 250-Gene Linear SVM was selected as the final model because it achieved the strongest performance while using a substantially reduced number of features.

Model Validation
Independent Test Set Performance

The final model was evaluated on an unseen test dataset.

Metric	Result
Test Samples	161
Correct Predictions	161
Incorrect Predictions	0
Test Accuracy	100.00%
Classification Report
Cancer Type	Precision	Recall	F1-Score	Support
BRCA	1.00	1.00	1.00	60
COAD	1.00	1.00	1.00	16
KIRC	1.00	1.00	1.00	30
LUAD	1.00	1.00	1.00	28
PRAD	1.00	1.00	1.00	27
Cross-Validation

The model was evaluated using stratified cross-validation.

Final Pipeline 5-Fold Cross-Validation
CV Scores:
[1.00000, 1.00000, 1.00000, 1.00000, 0.99375]

Mean CV Accuracy: 99.875%
Standard Deviation: 0.25%
Minimum Accuracy: 99.375%
Maximum Accuracy: 100.00%

The consistently high cross-validation scores indicate that the model performance is stable across different data partitions.

Selected Gene Analysis

The final model selected 250 informative genes from the original high-dimensional gene-expression dataset.

The complete list is available in:

metadata/Final_250_Selected_Genes.csv

Examples of highly influential genes based on Linear SVM coefficients include:

BRCA
gene_9652
gene_6836
gene_6876
gene_18746
COAD
gene_5830
gene_6487
gene_3523
gene_10098
KIRC
gene_12977
gene_12068
gene_18333
gene_8794
LUAD
gene_15899
gene_15633
gene_15894
gene_15591
PRAD
gene_13976
gene_12847
gene_753
gene_16358

Note: These feature identifiers represent columns in the dataset. Biological interpretation would require mapping these identifiers to official gene symbols and performing further biological validation.

PCA Visualization

Principal Component Analysis (PCA) was performed for exploratory visualization of the selected gene-expression features.

The first two principal components explained:

PC1: 39.84%
PC2: 16.48%
Total Explained Variance: 56.32%

The PCA visualization demonstrated strong separation between the five cancer classes, indicating that the selected gene-expression features contain meaningful discriminatory information.

Reproducibility

The final trained pipeline was saved using Joblib.

models/Final_250_Gene_Linear_SVM.pkl

The saved model was reloaded successfully and produced identical predictions.

Reloaded Predictions Identical: True
Reloaded Model Test Accuracy: 100%
Input Validation

The prediction system validates uploaded input data before classification.

Validation checks include:

Input must be a pandas DataFrame
Dataset must not be empty
Duplicate column detection
Required gene column validation
Missing gene detection
Numeric value validation
Missing value detection
Automatic gene column ordering

The input CSV may optionally contain a sample_id column.

Project Structure
Cancer-Gene-Expression-Classifier/
│
├── app/
│   ├── app.py
│   └── predictor.py
│
├── models/
│   └── Final_250_Gene_Linear_SVM.pkl
│
├── data/
│   └── sample_input_gene_expression.csv
│
├── metadata/
│   ├── Final_250_Selected_Genes.csv
│   ├── model_metadata.json
│   └── required_gene_columns.csv
│
├── requirements.txt
├── .gitignore
└── README.md
Application Features

The Streamlit application allows users to:

Upload gene-expression data in CSV format.
Validate the input structure.
Detect missing or invalid gene features.
Run multi-class cancer classification.
View predicted cancer categories.
Visualize predicted class distribution.
Download prediction results.
Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/Cancer-Gene-Expression-Classifier.git

Navigate to the project directory:

cd Cancer-Gene-Expression-Classifier

Install dependencies:

pip install -r requirements.txt

Run the Streamlit application:

streamlit run app/app.py
Limitations

Despite the excellent internal evaluation results, this project has important limitations:

The dataset contains only 801 samples.
Evaluation was performed using internal train-test splitting and cross-validation.
No independent external validation dataset was used.
Dataset feature identifiers have not been mapped to biological gene symbols.
High internal accuracy does not guarantee clinical performance.
The model has not undergone clinical validation.

Therefore, this model should be considered a machine learning research project rather than a clinical diagnostic system.

Future Improvements

Potential future improvements include:

External validation using independent cancer datasets.
Mapping dataset feature IDs to official gene symbols.
Biological pathway and biomarker analysis.
SHAP-based model interpretability.
Comparison with additional machine learning algorithms.
Hyperparameter optimization.
Deep learning model comparison.
Docker containerization.
Cloud deployment with automated testing.
Disclaimer

This project is intended strictly for research and educational purposes.

It is not a clinically validated diagnostic system and must not be used for medical diagnosis, treatment planning, or patient care.

Author

Waqar Hussain

BS Biotechnology | B.Ed (Leadership & Management)

Machine Learning | AI Engineering | Data Science
