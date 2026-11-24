# Week 11 Class 2 — Outlier Audit

Source: UCI Wine dataset distributed with scikit-learn. Modified for education with three instructor-inserted anomalies.

## Run

The project uses Python, Pandas and NumPy.

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

Run the outlier audit:

```bash
python outlier_audit.py
```

The program generates three CSV files:

- `retained_flagged.csv`
- `quarantined_records.csv`
- `quality_summary.csv`

Run the unit tests:

```bash
python -m unittest -v
```

## Validation and decision policy

The audit checks the `malic_acid` and `proline` measurements using two statistical methods.

The Z-score method flags values where the absolute Z-score is greater than 3. The calculation uses a population standard deviation (`ddof=0`).

The IQR method uses the default Pandas 25th and 75th percentiles. Values below Q1 - 1.5 × IQR or above Q3 + 1.5 × IQR are flagged.

The domain validation rules are:

- `proline` values less than or equal to zero are invalid.
- Negative or missing `malic_acid` values are invalid.

Statistical outliers are flagged for review but are not automatically removed because unusual measurements can still be valid observations. Only records failing the specified domain validation rules are quarantined.

The original measurement values are preserved.

## Results and limitations

The dataset contains 178 records.

The audit retained 177 records and quarantined 1 record because its proline value was negative.

The statistical audit identified:

- 1 Z-score flag for malic acid.
- 4 IQR flags for malic acid.
- 1 Z-score flag for proline.
- 1 IQR flag for proline.

A rare high proline reading may be a legitimate observation and should be investigated before removal.

These domain rules are instructional validation rules, not universal scientific limits. Statistical outlier methods identify unusual values but cannot independently determine whether a measurement is scientifically incorrect.

The dataset is a public-derived teaching version with three instructor-inserted anomalies. It is not an untouched public download.

## GitHub PR

The individual pull request link will be added after the pull request is created.