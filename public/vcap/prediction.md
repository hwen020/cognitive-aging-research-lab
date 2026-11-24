# VCAP Prediction

Source: [Salthouse (2024), VCAP, University of Virginia Dataverse, V1.0](https://doi.org/10.18130/V3/QRCQ08).

One baseline-to-next observed eligible score pair per returning participant. Train 1,728, validation 576, test 576. Maximum participant overlap across partitions: 0. Horizon is unknown at baseline and is excluded as a feature. Candidate forest leaf sizes were selected by validation MAE. The test set compares the selected forest with the carry-forward baseline. Intervals use 1,000 bootstrap resamples of held-out participants conditional on fitted models.

| Model | MAE (95% CI) | RMSE (95% CI) |
| --- | ---: | ---: |
| carry_forward | 7.757 (7.146, 8.389) | 10.854 (9.604, 12.092) |
| random_forest | 7.596 (6.997, 8.227) | 10.597 (9.435, 11.819) |
Paired forest-minus-baseline MAE -0.161 (95% CI -0.402 to 0.091).
- up to 3 years: n = 353; carry-forward MAE 7.224; forest MAE 7.180.
- over 3 years: n = 223; carry-forward MAE 8.601; forest MAE 8.255.

## Limitations

This volunteer cohort and observed-follow-up sample are susceptible to selection. A baseline-only record does not establish withdrawal, death or ineligibility. The retest indicator probes a discrete first-retest shift; it cannot isolate practice from aging or other visit differences. Observational associations do not identify causal effects. The prediction applies only to subsequent observed Digit Symbol scores, with heterogeneous time intervals, and has no clinical diagnostic interpretation.
