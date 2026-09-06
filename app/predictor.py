
from pathlib import Path
import pandas as pd
import joblib


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "Final_250_Gene_Linear_SVM.pkl"
GENES_PATH = BASE_DIR / "metadata" / "required_gene_columns.csv"


def load_resources():
    """Load the trained model and required gene list."""

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    if not GENES_PATH.exists():
        raise FileNotFoundError(
            f"Required gene list not found: {GENES_PATH}"
        )

    model = joblib.load(MODEL_PATH)

    required_genes = pd.read_csv(
        GENES_PATH
    )["Gene"].tolist()

    return model, required_genes


def validate_input(data, required_genes):
    """
    Validate uploaded gene-expression data and return
    correctly ordered gene features.
    """

    if not isinstance(data, pd.DataFrame):
        raise TypeError(
            "Input must be a pandas DataFrame."
        )

    if data.empty:
        raise ValueError(
            "Input dataset is empty."
        )

    # Check duplicate column names
    duplicate_columns = data.columns[
        data.columns.duplicated()
    ].tolist()

    if duplicate_columns:
        raise ValueError(
            f"Duplicate column names detected. "
            f"Examples: {duplicate_columns[:5]}"
        )

    # Remove optional sample ID
    gene_data = data.drop(
        columns=["sample_id"],
        errors="ignore"
    )

    # Check missing required genes
    missing_genes = sorted(
        set(required_genes) - set(gene_data.columns)
    )

    if missing_genes:
        raise ValueError(
            f"Missing {len(missing_genes)} required "
            f"gene columns. Examples: {missing_genes[:5]}"
        )

    # Keep required genes in exact training order
    gene_data = gene_data[
        required_genes
    ].copy()

    # Ensure all values are numeric
    try:
        gene_data = gene_data.apply(
            pd.to_numeric,
            errors="raise"
        )
    except Exception as exc:
        raise ValueError(
            "All gene-expression values must be numeric."
        ) from exc

    # Check missing values
    if gene_data.isnull().any().any():
        raise ValueError(
            "Input contains missing gene-expression values."
        )

    return gene_data


def predict_cancer(data):
    """
    Predict cancer class for one or multiple samples.

    Parameters
    ----------
    data : pandas.DataFrame
        Input data containing all required gene-expression
        features and an optional sample_id column.

    Returns
    -------
    pandas.DataFrame
        Sample IDs (if available) and predicted cancer classes.
    """

    model, required_genes = load_resources()

    validated_data = validate_input(
        data,
        required_genes
    )

    predictions = model.predict(
        validated_data
    )

    results = pd.DataFrame({
        "Predicted_Cancer_Type": predictions
    })

    # Preserve sample IDs
    if "sample_id" in data.columns:
        results.insert(
            0,
            "sample_id",
            data["sample_id"].values
        )

    return results
