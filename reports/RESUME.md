# Cognitive Aging Research Lab — résumé variants

[Live Demo](https://cognitive-aging-research-lab.onrender.com)

## Social Data Scientist

- Built a reproducible Python pipeline for a 2,400-participant, five-wave synthetic cognitive aging cohort, verifying 12,000 complete observations, canonical CSV checksums, and monotone dropout and marker missingness scenarios.
- Fit and validated R random-intercept models for deprivation-related cognitive trajectories. Implemented a DAG-driven stabilized IPTW workflow with balance, overlap, effective sample size, bootstrap intervals, truncation sensitivity, and automatic effect withholding for the attrition scenario.

## Biological Data Scientist

- Fit R mixed-effects models that separated baseline levels and within-participant changes in synthetic CRP, p-tau, and NfL proxies, with marker-specific missingness accounting and Benjamini–Hochberg adjustment.
- Benchmarked baseline-only Ridge and Random Forest against a training-mean baseline for simulated Year-8 cognition. Verified zero participant overlap across a 1,800/600 train/holdout split, fit preprocessing within grouped training folds, and reported bootstrap uncertainty, subgroup errors, and paired marker-ablation results.

## NHANES v1.1 evidence

**Social Data Scientist.** Harmonized eight official NHANES public-use files across two survey cycles and built an auditable older-adult analysis domain. Used R complex-survey regression with pooled MEC weights, masked strata and PSUs to estimate adjusted socioeconomic associations with cognition, with confidence intervals, missingness summaries, and sensitivity analyses.

**Biological Data Scientist.** Estimated design-weighted associations between measured HbA1c, systolic blood pressure, and cognitive test scores in NHANES. Compared benchmark, linear, and tree models on a later independent survey cycle, checked respondent separation, and quantified paired holdout MAE differences using masked-PSU resampling.

## VCAP v1.2 evidence

**Social Data Scientist.** Harmonized dated repeated assessments across three VCAP workbook sheets, analyzed baseline age and education in R mixed-effects models, and audited observed follow-up, missingness, and retest sensitivity in 5,622 eligible participants.

**Biological Data Scientist.** Evaluated a random forest against score carry-forward for subsequent Digit Symbol performance with disjoint training, validation, and test participants, using paired bootstrap uncertainty and horizon-stratified evaluation. Published a reproducible aggregate research interface.
