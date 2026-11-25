
"""Week 11 Class 1 — independent missing-data lab.

Run from this folder:
    python missing_data_lab.py

Fill TODO sections. Do not paste the teaching notebook solution.
"""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).with_name("gapminder_instructional_missing.csv")
OUTPUT = Path(__file__).with_name("outputs")
REQUIRED = {"country", "continent", "year", "lifeExp", "pop", "gdpPercap"}


def load_and_validate(path: Path) -> pd.DataFrame:
    """Read source, check schema, unique country/year and positive population."""

    df = pd.read_csv(path)

    missing_columns = REQUIRED - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if df.duplicated(subset=["country", "year"]).any():
        raise ValueError("Duplicate country/year combinations found.")

    if (df["pop"] <= 0).any():
        raise ValueError("Population must be positive.")

    return df


def missingness_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return column, missing_count, missing_pct for every source column."""

    missing_count = df.isna().sum()

    report = pd.DataFrame({
        "column": missing_count.index,
        "missing_count": missing_count.values,
        "missing_pct": (missing_count.values / len(df) * 100).round(2)
    })

    return report


def impute_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preserve original observed values; mark and fill only specified missing cells.

    - continent: derive missing label from other rows of same country
    - lifeExp: continent-level median, fallback global median
    - gdpPercap: continent-level median, fallback global median
    - add lifeExp_was_missing and gdpPercap_was_missing boolean columns
    """

    result = df.copy()

    # Add missingness flags before filling.
    result["lifeExp_was_missing"] = result["lifeExp"].isna()
    result["gdpPercap_was_missing"] = result["gdpPercap"].isna()

    # Fill missing continent labels using the same country's observed continent.
    country_continent = result.groupby("country")["continent"].transform(
        lambda group: group.ffill().bfill()
    )

    result["continent"] = result["continent"].fillna(country_continent)

    # Calculate global medians.
    global_lifeExp_median = result["lifeExp"].median()
    global_gdpPercap_median = result["gdpPercap"].median()

    # Calculate continent-level medians.
    lifeExp_median = result.groupby("continent")["lifeExp"].transform("median")
    gdpPercap_median = result.groupby("continent")["gdpPercap"].transform("median")

    # Fill missing values using continent medians, then global medians.
    result["lifeExp"] = result["lifeExp"].fillna(lifeExp_median)
    result["lifeExp"] = result["lifeExp"].fillna(global_lifeExp_median)

    result["gdpPercap"] = result["gdpPercap"].fillna(gdpPercap_median)
    result["gdpPercap"] = result["gdpPercap"].fillna(global_gdpPercap_median)

    return result


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)

    source = load_and_validate(DATA)
    report = missingness_report(source)
    cleaned = impute_data(source)

    # Verify required fields contain no missing values.
    if cleaned[["continent", "lifeExp", "gdpPercap"]].isna().any().any():
        raise ValueError("Missing values remain in required target columns.")

    # Verify that no rows were added or deleted.
    if len(cleaned) != len(source):
        raise ValueError("Row count changed during imputation.")

    # Verify originally observed numeric values did not change.
    for column in ["lifeExp", "gdpPercap"]:
        observed = source[column].notna()

        if not cleaned.loc[observed, column].equals(
            source.loc[observed, column]
        ):
            raise ValueError(f"Originally observed {column} values changed.")

    report.to_csv(OUTPUT / "missingness_report.csv", index=False)
    cleaned.to_csv(OUTPUT / "imputed_gapminder.csv", index=False)

    print("Created reports in", OUTPUT)


if __name__ == "__main__":
    main()
