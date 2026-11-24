# Model card — simulated eight-year cognition

| Field | Description |
| --- | --- |
| Intended use | Demonstrate reproducible evaluation of baseline-only longitudinal prediction |
| Outcome | Unitless simulated cognition at Year 8 |
| Population | Seeded 2,400-person synthetic cohort, eligible with an observed Year-8 outcome |
| Inputs | Baseline age, sex category, education, deprivation, hypertension, optionally three simulated proxies |
| Validation | Seeded participant holdout, zero ID overlap, five training-only folds, MAE tuning |
| Models | Training mean, Ridge and Random Forest, with and without biomarker proxies |
| Reporting | Holdout MAE, RMSE, R², 500 participant resamples, subgroup MAE, paired marker comparison and permutation importance |
| Limitations | Artificial features and outcome, no observed cohort, no external validation, conditional bootstrap intervals, dropout selection in the incomplete scenario |

Complete and incomplete simulations are separate experiments with the same design. Neither paired marker comparison demonstrated a clear holdout improvement within the reported uncertainty. These models are unsuitable for screening, diagnosis, clinical decisions or forecasting a real population.

See the [biological report](../public/reports/biological.md) and [aggregate evaluation bundle](../src/generated/results.json).
