\# Week 11 Class 1 – Gapminder Missing Data Lab



\## Project overview



This lab applies missing-data profiling and imputation to a 96-record country/year dataset derived from the Gapminder sample made available through Plotly Express.



The instructional dataset contains 17 deliberately blanked field values. These missing values were introduced for this classroom exercise and should not be interpreted as naturally occurring missingness in the original public dataset.



\## Method



The CSV file was loaded using Pandas. The script checks the required six columns, unique country/year combinations and positive population values.



A missingness report was generated for every source column. It records the number and percentage of missing values, with percentages rounded to two decimal places.



Before imputation, two Boolean flags were created:



\- `lifeExp\_was\_missing`

\- `gdpPercap\_was\_missing`



Missing continent labels were filled using observed continent labels from other records belonging to the same country.



Missing `lifeExp` and `gdpPercap` values were filled using their respective continent-level medians. Where a continent group had no available median, the corresponding global median was used as a fallback.



The original observed numeric values were preserved. The script also checks that the row count remains unchanged and that the required target columns contain no unresolved missing values.



\## Outputs



The script generates:



\- `outputs/missingness\_report.csv`

\- `outputs/imputed\_gapminder.csv`



The missingness report is calculated from the original dataset before imputation.



\## Limitation and risk



Median imputation replaces missing observations with estimated values rather than the actual values. This can reduce natural variation in the data and may hide differences between countries. Continent-level medians may also fail to represent the circumstances of an individual country.



Imputed values should therefore be treated as estimates, not original measurements.



\## How to run



From the `dayone` folder, run:



```bash

python missing\_data\_lab.py

```



The script requires Pandas.



\## Data source



The dataset is a public-derived Gapminder country-level sample made available through Plotly Express. The classroom version was modified by deliberately blanking 17 field values for this exercise. No missing values were recovered from a clean public copy.

