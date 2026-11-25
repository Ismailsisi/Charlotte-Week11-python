
"""Week 11 Class 3 student lab: implement a leakage-safe feature pipeline.
Run: python preprocess_iris.py --input iris_preprocessing_case_PUBLIC_DERIVED.csv --output-dir outputs
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder


NUMERIC = [
    "sepal_length_cm",
    "sepal_width_cm",
    "petal_length_cm",
    "petal_width_cm"
]

CATEGORICAL = ["collection_site", "instrument_type"]
LABEL = "species"


def build_preprocessor():
    """Return a ColumnTransformer with numeric imputation+scaling and category imputation+one-hot.
    Make unseen categories transformable without an exception.
    """

    numeric_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("numeric", numeric_pipeline, NUMERIC),
        ("categorical", categorical_pipeline, CATEGORICAL)
    ])

    return preprocessor


def prepare_dataset(input_csv):
    """Load CSV, split features/target before fitting, then return (transformer, train_df, test_df, report_dict).
    Split must be deterministic: test_size=0.2, random_state=42, stratify=species.
    Output DataFrames must have matching columns, numeric finite values, and no species/sample_id.
    Report keys: source_rows, training_rows, test_rows, transformed_features, missing_source_cells.
    """

    # Load the dataset
    df = pd.read_csv(input_csv)

    # Count missing cells in the original dataset
    missing_source_cells = int(df.isna().sum().sum())

    # Separate predictors (X) and target (y)
    X = df[NUMERIC + CATEGORICAL]
    y = df[LABEL]

    # Split before fitting any preprocessing transformations
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Build the preprocessing pipeline
    transformer = build_preprocessor()

    # Fit only on training data
    X_train_transformed = transformer.fit_transform(X_train)

    # Transform test data using the already fitted training pipeline
    X_test_transformed = transformer.transform(X_test)

    # Get the transformed feature names
    feature_names = transformer.get_feature_names_out()

    # Convert transformed arrays into DataFrames
    train_df = pd.DataFrame(
        X_train_transformed,
        columns=feature_names,
        index=X_train.index
    )

    test_df = pd.DataFrame(
        X_test_transformed,
        columns=feature_names,
        index=X_test.index
    )

    # Verify that transformed values are finite
    if not np.isfinite(train_df.to_numpy()).all():
        raise ValueError("Training features contain non-finite values")

    if not np.isfinite(test_df.to_numpy()).all():
        raise ValueError("Test features contain non-finite values")

    # Verify matching feature columns
    if list(train_df.columns) != list(test_df.columns):
        raise ValueError("Training and test feature columns do not match")

    # Prepare the required data quality report
    report = {
        "source_rows": len(df),
        "training_rows": len(train_df),
        "test_rows": len(test_df),
        "transformed_features": len(feature_names),
        "missing_source_cells": missing_source_cells
    }

    return transformer, train_df, test_df, report


def write_outputs(train_df, test_df, report, output_dir):
    """Write train_features.csv, test_features.csv, data_quality_summary.csv."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    train_df.to_csv(output_path / "train_features.csv", index=False)
    test_df.to_csv(output_path / "test_features.csv", index=False)

    report_df = pd.DataFrame([report])
    report_df.to_csv(output_path / "data_quality_summary.csv", index=False)


def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        '--input',
        default='iris_preprocessing_case_PUBLIC_DERIVED.csv'
    )
    p.add_argument('--output-dir', default='outputs')
    args = p.parse_args()

    transformer, train, test, report = prepare_dataset(args.input)

    write_outputs(train, test, report, args.output_dir)

    print('Preprocessing completed')


if __name__ == '__main__':
    main()
