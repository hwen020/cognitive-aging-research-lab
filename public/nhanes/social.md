# NHANES 2011–2014 | Social research

Public CDC/NCHS data from two independent survey cycles. Outcomes are measured cognitive test scores. The results describe cross-sectional associations and concurrent prediction.

Survey-weighted DSST models adjust for age, recorded sex, race/Hispanic-origin category, and cycle. Education is coded as five levels, with college graduate or above as the reference; PIR is a poverty-income ratio point.

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

### DSST (n = 2,756)

`dsst ~ education + pir + RIDAGEYR + sex + race + wave`

Residual RMSE: 16.423; residual df: 19.

| Exposure | Estimate | 95% CI | BH q |
| --- | ---: | --- | ---: |
| education4 | -2.506 | -4.525 to -0.487 | 0.02206 |
| education3 | -7.138 | -9.380 to -4.897 | 7.499e-06 |
| education2 | -11.637 | -14.442 to -8.832 | 3.241e-07 |
| education1 | -20.082 | -22.360 to -17.803 | 2.747e-12 |
| pir | 2.020 | 1.513 to 2.528 | 3.979e-07 |

### IMMEDIATE (n = 2,855)

`immediate ~ education + pir + RIDAGEYR + sex + race + wave`

Residual RMSE: 5.378; residual df: 19.

| Exposure | Estimate | 95% CI | BH q |
| --- | ---: | --- | ---: |
| education4 | -0.452 | -1.071 to 0.166 | 0.15 |
| education3 | -1.111 | -1.806 to -0.417 | 0.006122 |
| education2 | -1.771 | -2.604 to -0.938 | 0.0006122 |
| education1 | -3.156 | -4.322 to -1.990 | 4.614e-05 |
| pir | 0.284 | 0.069 to 0.499 | 0.01637 |

### DELAYED (n = 2,850)

`delayed ~ education + pir + RIDAGEYR + sex + race + wave`

Residual RMSE: 2.823; residual df: 19.

| Exposure | Estimate | 95% CI | BH q |
| --- | ---: | --- | ---: |
| education4 | -0.023 | -0.415 to 0.369 | 0.9026 |
| education3 | -0.475 | -0.917 to -0.034 | 0.04022 |
| education2 | -0.585 | -1.006 to -0.164 | 0.01293 |
| education1 | -1.033 | -1.730 to -0.336 | 0.009032 |
| pir | 0.100 | 0.011 to 0.188 | 0.03533 |

### FLUENCY (n = 2,836)

`fluency ~ education + pir + RIDAGEYR + sex + race + wave`

Residual RMSE: 6.821; residual df: 19.

| Exposure | Estimate | 95% CI | BH q |
| --- | ---: | --- | ---: |
| education4 | -1.694 | -2.735 to -0.652 | 0.005975 |
| education3 | -3.532 | -4.688 to -2.376 | 1.122e-05 |
| education2 | -4.009 | -4.950 to -3.069 | 3.199e-07 |
| education1 | -4.690 | -5.874 to -3.505 | 3.979e-07 |
| pir | 0.299 | 0.097 to 0.500 | 0.009032 |

## Sensitivity

- social_on_bio_complete: n = 2,586, PIR coefficient 1.889 (95% CI 1.371 to 2.406).
- social_age_70_plus: n = 1,267, PIR coefficient 1.754 (95% CI 1.009 to 2.499).

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
