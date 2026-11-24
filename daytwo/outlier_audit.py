
"""Week 11 Class 2 independent lab — complete the TODOs yourself."""
from pathlib import Path
import pandas as pd

REQUIRED = ["sample_id", "alcohol", "malic_acid", "color_intensity", "proline", "target"]

def audit_data(data: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Return retained, quarantine and quality summary tables."""
    # TODO: validate schema, compute Z and IQR for two columns, apply domain checks
    # TODO: preserve raw values and add explicit review flags

    missing_columns = [column for column in REQUIRED if column not in data.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    data = data.copy()

    for column in ["malic_acid", "proline"]:
        if not pd.api.types.is_numeric_dtype(data[column]):
            raise ValueError(f"{column} must be numeric")

        mean = data[column].mean()
        std = data[column].std(ddof=0)

        if pd.isna(std) or std == 0:
            data[column + "_z_flag"] = False
        else:
            z_score = (data[column] - mean) / std
            data[column + "_z_flag"] = z_score.abs() > 3

        q1 = data[column].quantile(0.25)
        q3 = data[column].quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        data[column + "_iqr_flag"] = (
            (data[column] < lower_bound)
            | (data[column] > upper_bound)
        ).fillna(False)

    data["malic_acid_invalid"] = (
        data["malic_acid"].isna() | (data["malic_acid"] < 0)
    )

    data["proline_invalid"] = (
        data["proline"].isna() | (data["proline"] <= 0)
    )

    data["review_needed"] = (
        data["malic_acid_z_flag"]
        | data["malic_acid_iqr_flag"]
        | data["proline_z_flag"]
        | data["proline_iqr_flag"]
        | data["malic_acid_invalid"]
        | data["proline_invalid"]
    )

    quarantine_mask = (
        data["malic_acid_invalid"] | data["proline_invalid"]
    )

    quarantined = data[quarantine_mask].copy()
    retained = data[~quarantine_mask].copy()

    summary = pd.DataFrame({
        "metric": [
            "total_input",
            "retained",
            "quarantined",
            "malic_acid_z_flags",
            "malic_acid_iqr_flags",
            "proline_z_flags",
            "proline_iqr_flags"
        ],
        "count": [
            len(data),
            len(retained),
            len(quarantined),
            int(data["malic_acid_z_flag"].sum()),
            int(data["malic_acid_iqr_flag"].sum()),
            int(data["proline_z_flag"].sum()),
            int(data["proline_iqr_flag"].sum())
        ]
    })

    return {
        "retained": retained,
        "quarantined": quarantined,
        "summary": summary
    }


if __name__ == "__main__":
    data = pd.read_csv(Path(__file__).with_name("wine_quality_case_PUBLIC_DERIVED.csv"))
    results = audit_data(data)
    # TODO: save all three CSVs with documented relative paths

    results["retained"].to_csv("retained_flagged.csv", index=False)
    results["quarantined"].to_csv("quarantined_records.csv", index=False)
    results["summary"].to_csv("quality_summary.csv", index=False)

    print(results["summary"])
