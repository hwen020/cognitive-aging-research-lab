# NHANES 2011–2014 | Biological research

Public CDC/NCHS data from two independent survey cycles. Outcomes are measured cognitive test scores. The results describe cross-sectional associations and concurrent prediction.

Survey-weighted DSST models adjust for age, recorded sex, race/Hispanic-origin category, and cycle. Education is coded as five levels, with college graduate or above as the reference; PIR is a poverty-income ratio point. The joint model adds HbA1c per percentage point and systolic pressure per 10 mm Hg.

MEC examination weight divided by two; cycle-nested masked strata and PSUs. The full examined sample defines the survey design before the age-60+ domain restriction. Models use complete cases.

R 4.6.2; survey 4.5.

## Sample flow

- total demographics: 19,931
- mec: 19,151
- age 60 plus: 3,472
- dsst observed: 3,014
- social primary: 2,756
- biological primary: 2,586

## Missingness in the examined age-60+ domain

- dsst: 13.19%
- immediate: 9.82%
- delayed: 9.97%
- fluency: 10.43%
- education: 0.20%
- pir: 9.27%
- hba1c: 4.90%
- sbp10: 3.86%

## Model results

### DSST (n = 2,586)

`dsst ~ education + pir + RIDAGEYR + sex + race + wave + hba1c +     sbp10`

Residual RMSE: 16.161; residual df: 17.

| Exposure | Estimate | 95% CI | BH q |
| --- | ---: | --- | ---: |
| hba1c | -1.092 | -1.836 to -0.348 | 0.03508 |
| sbp10 | -0.403 | -0.769 to -0.037 | 0.05227 |

### IMMEDIATE (n = 2,677)

`immediate ~ education + pir + RIDAGEYR + sex + race + wave +     hba1c + sbp10`

Residual RMSE: 5.305; residual df: 17.

| Exposure | Estimate | 95% CI | BH q |
| --- | ---: | --- | ---: |
| hba1c | -0.131 | -0.360 to 0.098 | 0.2453 |
| sbp10 | -0.176 | -0.317 to -0.036 | 0.04464 |

### DELAYED (n = 2,672)

`delayed ~ education + pir + RIDAGEYR + sex + race + wave + hba1c +     sbp10`

Residual RMSE: 2.807; residual df: 17.

| Exposure | Estimate | 95% CI | BH q |
| --- | ---: | --- | ---: |
| hba1c | -0.132 | -0.243 to -0.020 | 0.0478 |
| sbp10 | -0.056 | -0.116 to 0.003 | 0.08423 |

### FLUENCY (n = 2,661)

`fluency ~ education + pir + RIDAGEYR + sex + race + wave + hba1c +     sbp10`

Residual RMSE: 6.798; residual df: 17.

| Exposure | Estimate | 95% CI | BH q |
| --- | ---: | --- | ---: |
| hba1c | -0.213 | -0.586 to 0.160 | 0.2453 |
| sbp10 | -0.155 | -0.266 to -0.045 | 0.03508 |

## Sensitivity

- Joint quadratic-term p-value: 0.2184.
- Unweighted clinical predictor correlation: 0.029.
- unadjusted_hba1c, hba1c: n = 2,902, estimate -3.234 (95% CI -4.656 to -1.812).
- unadjusted_sbp, sbp10: n = 2,922, estimate -1.493 (95% CI -1.985 to -1.002).
- bio_two_bp_readings, hba1c: n = 2,581, estimate -1.096 (95% CI -1.839 to -0.353).
- bio_two_bp_readings, sbp10: n = 2,581, estimate -0.374 (95% CI -0.733 to -0.015).

## Predictive performance

Train 2011–2012: 1,201. Test 2013–2014: 1,385. Overlap: 0.
Metrics are unweighted in the holdout complete cases.

| Model | MAE | RMSE | R² |
| --- | ---: | ---: | ---: |
| training_mean | 13.893 | 17.081 | -0.002 |
| social_linear | 9.918 | 12.572 | 0.457 |
| augmented_linear | 9.854 | 12.516 | 0.462 |
| augmented_tree | 11.149 | 14.039 | 0.323 |

Paired augmented-minus-social MAE = -0.063 (95% masked-PSU bootstrap interval -0.123 to -0.005). Negative values favor the augmented model. The interval conditions on fitted models.

## Interpretation and reproduction

Residual summaries are model checks. Selection into cognitive test completion and missing predictors can alter the modeled domain. Test language, age top coding, omitted confounding and measurement limitations can affect associations. These cycles cannot identify cognitive decline or treatment effects.

Run `python -m analysis.nhanes`, then `Rscript --vanilla analysis/r/nhanes.R` from the repository root. The source list is also available in the downloadable aggregate JSON.

### Official source versions and hashes

- DEMO_G, September 2013. XPT SHA-256 `eaf0525d1952626885af3e935415a1f66ad62c18698080e7354789c125af252d`. [CDC codebook](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2011/DataFiles/DEMO_G.htm)
- CFQ_G, March 2017. XPT SHA-256 `086c0c5a1bcfe965671ec0ff1cd607d6924ce4ddee82610d21eea69bfbf353e7`. [CDC codebook](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2011/DataFiles/CFQ_G.htm)
- BPX_G, September 2013. XPT SHA-256 `1dd66110f41465d601cd54f1e3c6010baafb9375f09fbcaa3aef2536876146fd`. [CDC codebook](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2011/DataFiles/BPX_G.htm)
- GHB_G, September 2013. XPT SHA-256 `8ff7cc95461fdfd47d2c9640b944a2bcd45926a3c0e64c98a09a4cef6c0f88d7`. [CDC codebook](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2011/DataFiles/GHB_G.htm)
- DEMO_H, October 2015. XPT SHA-256 `f8f0cbb3085a323d4cde22349b164878fea1e64dbc404e65b5815c7816b547d7`. [CDC codebook](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/DEMO_H.htm)
- CFQ_H, March 2017. XPT SHA-256 `f1120a0fb956bfb327dbd02a8a2ad2a37054fac38acd2a23ab5b4aca1eb3dabd`. [CDC codebook](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/CFQ_H.htm)
- BPX_H, October 2015. XPT SHA-256 `b6641efc30ac9b9de328dfbf4110d0d120439aadca2c2bc89f2e77310d1a0c8e`. [CDC codebook](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/BPX_H.htm)
- GHB_H, October 2015. XPT SHA-256 `0695894ad55ac96f315a8415401977b0856c402d16762115b534bcd5dfeae89e`. [CDC codebook](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/GHB_H.htm)
