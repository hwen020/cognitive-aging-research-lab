# Cognitive Aging Research Lab — Social research

All participants, marker proxies and scores are simulated. Estimates are conditional on this generator and cannot be used for clinical or real-population conclusions.

Dataset seed: 20261123. Artifact schema: 1.
Runtime: NumPy 2.5.5, pandas 2.3.3.

The descriptive model uses a REML participant random intercept, linear follow-up time and interactions with deprivation and baseline covariates. IPTW targets the total Year-8 mean contrast under high versus low simulated assignment.
The simulator assigns exposure independently at time zero. The fitted propensity includes age, education and sex. Downstream hypertension and CRP are excluded from the adjustment set.
Intervals for IPTW refit the propensity model across participant resamples. Identification of an observational effect would require assumptions about confounding, consistency, overlap and censoring.

## Complete simulation

2,400 participants, 12,000 observations. CSV SHA-256: `5104d2c3ca510a4f0ac537652c3f4b76f6b4e567d42cad9029c3b24b5297de74`.
Visit counts: Year 0=2,400, Year 2=2,400, Year 4=2,400, Year 6=2,400, Year 8=2,400.
Missing proxy values: crp=0, ptau=0, nfl=0.
R 4.6.2 / nlme 3.1.171, 12,000 model rows.
Adjusted annual slope difference: -0.2489 points (95% CI -0.2607 to -0.2372).
Residual lag-1 ACF: -0.2535; inspect uncertainty in light of the working covariance assumption.
IPTW overlap: 99.92% of participants; effective sample sizes (low/high): 1232.5965 to 1166.5474.

| Covariate | Unweighted SMD | Weighted SMD |
| --- | ---: | ---: |
| age_at_baseline | 0.0309 | -0.0000 |
| education_years | 0.0212 | -0.0000 |
| sex_female | 0.0052 | -0.0002 |

| Truncation per tail | Contrast | 95% CI |
| ---: | ---: | --- |
| 0% | -5.2720 | -5.5725 to -5.0221 |
| 1% | -5.2726 | -5.5731 to -5.0221 |
| 5% | -5.2774 | -5.5828 to -5.0193 |

## Incomplete simulation

2,400 participants, 11,004 observations. CSV SHA-256: `506bcb34df4764c24cab64861625fd375afb390d6acf47d639af8e3df1d49764`.
Visit counts: Year 0=2,400, Year 2=2,300, Year 4=2,194, Year 6=2,097, Year 8=2,013.
Missing proxy values: crp=456, ptau=504, nfl=514.
R 4.6.2 / nlme 3.1.171, 11,004 model rows.
Adjusted annual slope difference: -0.2476 points (95% CI -0.2603 to -0.2350).
Residual lag-1 ACF: -0.2698; inspect uncertainty in light of the working covariance assumption.
IPTW effect withheld. Year-8 attrition requires a separate censoring design.

## Analysis source fingerprints

- `analysis/causal.py` — `6cb46b930bcf95340514875805604e138c313b702da7512eee259f13c440baed`
- `analysis/cohort.py` — `080bfd33b58cf93e37b10f257b3de37172b6c80287695945075f2aaffbbdd48d`
- `analysis/prediction.py` — `53de240e3dd4f18ac32de88c9451463a2352425d79092ac76026f6d9e202b120`
- `analysis/r/biological.R` — `43d7320b5aed2ee3f85bf18e49634c2e16d50a1d7057636b7d69036458cd26a6`
- `analysis/r/fit.R` — `48efe451cce7a2bb1a41b789bc128064c8d46e9cd9079653753684df16864594`
- `analysis/run.py` — `30f9ce6c2f7327a20cacf51eb6a067f62d91a404f66577bb9935be3f5fcfb45d`
