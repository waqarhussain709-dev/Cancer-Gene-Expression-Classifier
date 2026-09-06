import sys
from pathlib import Path
import pandas as pd
import streamlit as st
APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
sys.path.insert(0, str(APP_DIR))
from predictor import (predict_cancer, load_resources, validate_input)
st.set_page_config(page_title="Cancer Gene Expression Classifier", page_icon=":dna:", layout="wide", initial_sidebar_state="expanded")
st.sidebar.title("Model Information")
st.sidebar.markdown("""**Algorithm:** Linear Support Vector Machine
**Feature_Selection:** ANNOVA F-test (SelectKBest)
**Selected Features:** 250 genes
Cancer Classes:** 5
- BRCA
- COAD
- KIRC
- LUAD
- PRAD""")
st.sidebar.divider()
st.sidebar.warning("""**Research Use Only**
This model is an experimental machine learning project and must not be used for clinical diagnosis or medical decision-making.""")
st.tile(":dna: Cancer Gene Expression Classifier")
st.markdown("""Upload a CSV file containing gene-expression values to classify sample into one of five cancer categories.""")
with st.expander("Cancer Classes Supported"):
    st.markdown("""
    | Code | Cancer Type |
    |------|-------------|
    | BRCA | Breast Invasive Carcinoma |
    | COAD | Colon Adenocarcinoma |
    | KIRC | Kidney Renal Clear Cell Carcinoma |
    | LUAD | Lung Adenocarcinoma |
    | PRAD | Prostate Adenocarcinoma |
    """)

st.warning("""
⚠️ **Research and Educational Use Only**

This application is an experimental machine learning research project.
It has not undergone clinical validation and must not be used for
medical diagnosis, treatment decisions, or patient care.
""")
try:
    model, required_genes = load_resources()
except Exception as e:
    st.error(f"Unable to load model resources: {e}")
    st.stop()
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Required Input Genes", f"{len(required_genes):,}")
with col2:
    st.metric("Selected Features", "250")

with col3:
    st.metric("Cancer Classes", "5")

st.divider()
st.header("Upload Gene Expression Data")
upload_file = st.file_uploader("Upload CSV File", type=["csv"], help=("The file must contain all required gene-expression"
"columns. An optional sample_id column is supported."))

if upload_file is not None:
    try:
        input_data = pd.read_csv(upload_file)
        st.success(f"File loaded successfully - "
        f"{input_data.shape[0]} sample(s), "
        f"{input_data.shape[1]:,} columns")

        with st.expander("Preview Uploaded Data"):
            st.dataframe(input_data.head(), use_container_width=True)


        try:

            validated_data = validate_input(
                input_data,
                required_genes
            )

            st.success(
                f"✓ Input validation successful — "
                f"{validated_data.shape[1]:,} required "
                f"gene features detected."
            )

            input_valid = True

        except Exception as validation_error:

            st.error(
                f"Input validation failed: "
                f"{validation_error}"
            )

            input_valid = False

        if input_valid:

            if st.button(
                "Run Cancer Classification",
                type="primary",
                use_container_width=True
            ):

                with st.spinner(
                    "Running cancer classification model..."
                ):

                    results = predict_cancer(
                        input_data
                    )



                st.success(
                    "Classification completed successfully."
                )

                st.header("Prediction Results")

                st.dataframe(
                    results,
                    use_container_width=True
                )



                st.subheader(
                    "Predicted Class Distribution"
                )

                class_counts = (
                    results[
                        "Predicted_Cancer_Type"
                    ]
                    .value_counts()
                )

                st.bar_chart(
                    class_counts
                )



                csv_results = results.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    label="Download Prediction Results",
                    data=csv_results,
                    file_name=(
                        "cancer_classification_results.csv"
                    ),
                    mime="text/csv",
                    use_container_width=True
                )


    except Exception as e:

        st.error(
            f"Unable to process uploaded file: {e}"
        )



st.divider()

st.caption("""
Developed as a machine learning research project for multi-class cancer
classification using high-dimensional gene-expression data.
Research and educational use only.
""")
