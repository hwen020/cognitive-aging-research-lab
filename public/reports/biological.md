# Cognitive Aging Research Lab — Biological research

All participants, marker proxies and scores are simulated. Estimates are conditional on this generator and cannot be used for clinical or real-population conclusions.

Dataset seed: 20261123. Artifact schema: 1.
Runtime: NumPy 2.5.5, pandas 2.3.3.

R random-intercept models estimate separate associations for each marker's baseline level and its change from baseline, using marker-specific complete rows. Each mode adjusts six marker-term p-values with Benjamini–Hochberg.
Prediction uses only baseline data and an observed Year-8 target, one row per eligible participant. Preprocessing and validation stay within training folds. The held-out intervals are conditional on the trained models.

## Complete simulation

2,400 participants, 12,000 observations. CSV SHA-256: `5104d2c3ca510a4f0ac537652c3f4b76f6b4e567d42cad9029c3b24b5297de74`.
Visit counts: Year 0=2,400, Year 2=2,400, Year 4=2,400, Year 6=2,400, Year 8=2,400.
Missing proxy values: crp=0, ptau=0, nfl=0.

| Marker | Term | Rows | Estimate | 95% CI | BH q |
| --- | --- | ---: | ---: | --- | ---: |
| crp | marker_baseline | 12,000 | -0.4021 | -0.6875 to -0.1166 | 0.0116 |
| crp | marker_within | 12,000 | -0.1767 | -0.2497 to -0.1038 | 6.16e-06 |
| ptau | marker_baseline | 12,000 | -0.0518 | -0.1021 to -0.0015 | 0.0523 |
| ptau | marker_within | 12,000 | -0.0527 | -0.0601 to -0.0454 | 3.02e-44 |
| nfl | marker_baseline | 12,000 | -0.0448 | -0.0818 to -0.0079 | 0.0262 |
| nfl | marker_within | 12,000 | -0.0024 | -0.0079 to 0.0030 | 0.378 |

scikit-learn 1.7.2. Train/test: 1,800/600. Participant overlap: 0.

| Prediction model | MAE (95% CI) | RMSE (95% CI) | R² (95% CI) |
| --- | --- | --- | --- |
| Random forest + markers | 2.6964 (2.5444 to 2.8583) | 3.3557 (3.1657 to 3.5346) | 0.7493 (0.7201 to 0.7759) |
| Random forest social | 2.6922 (2.5453 to 2.8517) | 3.3408 (3.1427 to 3.5173) | 0.7515 (0.7228 to 0.7789) |
| Ridge + markers | 2.6081 (2.4466 to 2.7590) | 3.2414 (3.0658 to 3.4099) | 0.7661 (0.7406 to 0.7923) |
| Ridge social | 2.6038 (2.4436 to 2.7497) | 3.2308 (3.0550 to 3.3960) | 0.7676 (0.7412 to 0.7935) |
| Training mean | 5.5584 (5.2634 to 5.8618) | 6.7132 (6.4087 to 7.0232) | -0.0033 (-0.0165 to -0.0000) |

Marker contribution (paired marker-augmented minus social MAE):
- Random forest: 0.0042 (-0.0322 to 0.0437).
- Ridge: 0.0043 (-0.0169 to 0.0238).

## Incomplete simulation

2,400 participants, 11,004 observations. CSV SHA-256: `506bcb34df4764c24cab64861625fd375afb390d6acf47d639af8e3df1d49764`.
Visit counts: Year 0=2,400, Year 2=2,300, Year 4=2,194, Year 6=2,097, Year 8=2,013.
Missing proxy values: crp=456, ptau=504, nfl=514.

| Marker | Term | Rows | Estimate | 95% CI | BH q |
| --- | --- | ---: | ---: | --- | ---: |
| crp | marker_baseline | 10,258 | -0.4011 | -0.6928 to -0.1094 | 0.0106 |
| crp | marker_within | 10,258 | -0.1775 | -0.2581 to -0.0970 | 4.71e-05 |
| ptau | marker_baseline | 10,139 | -0.0502 | -0.1019 to 0.0014 | 0.0681 |
| ptau | marker_within | 10,139 | -0.0511 | -0.0592 to -0.0430 | 3.41e-34 |
| nfl | marker_baseline | 10,162 | -0.0521 | -0.0898 to -0.0143 | 0.0106 |
| nfl | marker_within | 10,162 | -0.0032 | -0.0092 to 0.0028 | 0.295 |

scikit-learn 1.7.2. Train/test: 1,509/504. Participant overlap: 0.

| Prediction model | MAE (95% CI) | RMSE (95% CI) | R² (95% CI) |
| --- | --- | --- | --- |
| Random forest + markers | 2.7018 (2.5344 to 2.8753) | 3.3570 (3.1770 to 3.5564) | 0.7335 (0.6978 to 0.7652) |
| Random forest social | 2.6606 (2.5130 to 2.8271) | 3.3100 (3.1262 to 3.5009) | 0.7409 (0.7066 to 0.7717) |
| Ridge + markers | 2.5618 (2.4117 to 2.7132) | 3.1602 (2.9871 to 3.3362) | 0.7638 (0.7336 to 0.7922) |
| Ridge social | 2.5693 (2.4163 to 2.7235) | 3.1696 (2.9991 to 3.3476) | 0.7624 (0.7319 to 0.7902) |
| Training mean | 5.3278 (5.0145 to 5.6447) | 6.5095 (6.1545 to 6.8647) | -0.0021 (-0.0172 to -0.0000) |

Marker contribution (paired marker-augmented minus social MAE):
- Random forest: 0.0412 (-0.0170 to 0.1032).
- Ridge: -0.0076 (-0.0168 to 0.0017).

## Analysis source fingerprints

- `analysis/causal.py` — `6cb46b930bcf95340514875805604e138c313b702da7512eee259f13c440baed`
- `analysis/cohort.py` — `080bfd33b58cf93e37b10f257b3de37172b6c80287695945075f2aaffbbdd48d`
- `analysis/prediction.py` — `53de240e3dd4f18ac32de88c9451463a2352425d79092ac76026f6d9e202b120`
- `analysis/r/biological.R` — `43d7320b5aed2ee3f85bf18e49634c2e16d50a1d7057636b7d69036458cd26a6`
- `analysis/r/fit.R` — `48efe451cce7a2bb1a41b789bc128064c8d46e9cd9079653753684df16864594`
- `analysis/run.py` — `30f9ce6c2f7327a20cacf51eb6a067f62d91a404f66577bb9935be3f5fcfb45d`
