# VCAP Model Diagnostics

Source: [Salthouse (2024), VCAP, University of Virginia Dataverse, V1.0](https://doi.org/10.18130/V3/QRCQ08).

Random slope convergence: True. Intercept AIC 93673.07; slope AIC 93583.0787617028. Slope SD 0.5207868; normalized residual lag-one ACF -0.431. The negative residual autocorrelation warrants caution about the conditional covariance specification. Normalized residual quantiles (2.5%, 50%, 97.5%): -1.568, 0.009, 1.417.

## Retest shift sensitivity

| Term | Estimate | 95% CI |
| --- | ---: | --- |
| (Intercept) | 61.742 | 61.100 to 62.385 |
| years | -0.548 | -0.608 to -0.488 |
| age_c | -0.595 | -0.616 to -0.575 |
| educ_c | 1.587 | 1.453 to 1.722 |
| sex1 | 6.883 | 6.130 to 7.636 |
| retest | 2.539 | 2.105 to 2.974 |
| years:age_c | -0.019 | -0.021 to -0.016 |

## Repeat-participant sensitivity

| Term | Estimate | 95% CI |
| --- | ---: | --- |
| (Intercept) | 63.672 | 62.806 to 64.538 |
| years | -0.356 | -0.404 to -0.309 |
| age_c | -0.583 | -0.614 to -0.552 |
| educ_c | 1.594 | 1.411 to 1.777 |
| sex1 | 6.694 | 5.673 to 7.715 |
| years:age_c | -0.018 | -0.021 to -0.015 |
