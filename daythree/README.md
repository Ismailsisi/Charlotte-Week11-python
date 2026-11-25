# 

# \# Week 11 Class 3 | Feature preprocessing

# 

# \## Dataset source and changes

# 

# The dataset is based on the Iris flower dataset, originally published by the UCI Machine Learning Repository and made available through scikit-learn.

# 

# Sources:

# \- https://archive.ics.uci.edu/dataset/53/iris

# \- https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load\_iris.html

# 

# The dataset contains 150 records and four numerical flower measurements with species labels.

# 

# For this teaching exercise, three additional columns were introduced:

# \- `sample\_id`: synthetic sample identifier.

# \- `collection\_site`: synthetic categorical field.

# \- `instrument\_type`: synthetic categorical field.

# 

# Seven numerical observations and four collection site values were deliberately made missing.

# 

# The added categorical fields are synthetic and must not be interpreted as original scientific measurements.

# 

# \## Run instructions

# 

# Python and the following dependencies are required:

# \- NumPy

# \- Pandas

# \- Scikit-learn

# 

# Install dependencies:

# 

# ```bash

# python -m pip install -r requirements.txt

# ```

# 

# Run preprocessing from the `daythree` directory:

# 

# ```bash

# python preprocess\_iris.py --input iris\_preprocessing\_case\_PUBLIC\_DERIVED.csv --output-dir outputs

# ```

# 

# Run the smoke test from the repository root:

# 

# ```bash

# python -m unittest discover -s daythree -p "test\_student\_smoke.py"

# ```

# 

# \## Feature choices

# 

# The four numerical predictors are:

# \- `sepal\_length\_cm`

# \- `sepal\_width\_cm`

# \- `petal\_length\_cm`

# \- `petal\_width\_cm`

# 

# The two categorical predictors are:

# \- `collection\_site`

# \- `instrument\_type`

# 

# The `species` column is the target label and is excluded from the predictors.

# 

# The `sample\_id` column is an identifier and is also excluded.

# 

# Numerical missing values are handled using median imputation, followed by standard scaling.

# 

# Categorical missing values are handled using most-frequent imputation, followed by one-hot encoding.

# 

# The encoder uses `handle\_unknown="ignore"` so previously unseen categories can be transformed without raising an exception.

# 

# \## Why no leakage?

# 

# The dataset is split before fitting the preprocessing pipeline.

# 

# The split uses:

# \- `test\_size=0.2`

# \- `random\_state=42`

# \- `stratify=species`

# 

# The preprocessing pipeline is fitted only on the training records.

# 

# The fitted pipeline is then reused to transform the test records without fitting again.

# 

# This prevents information from the test dataset from influencing the imputation values, scaling parameters, or category encoding learned during training.

# 

# \## Results and known limitations

# 

# The preprocessing produced:

# 

# | Result | Value |

# |---|---:|

# | Source rows | 150 |

# | Training rows | 120 |

# | Test rows | 30 |

# | Transformed features | 9 |

# | Missing source cells | 11 |

# 

# Generated output files:

# \- `outputs/train\_features.csv`

# \- `outputs/test\_features.csv`

# \- `outputs/data\_quality\_summary.csv`

# 

# The training and test datasets have matching feature columns and contain finite numerical values.

# 

# The transformed outputs do not contain `species` or `sample\_id`.

# 

# The additional categorical fields are synthetic teaching data. The resulting features are intended for preprocessing practice and are not a deployment-ready scientific model.

# 

# \## Pull request link

# 

# To be added after creating the GitHub Pull Request.

# 

