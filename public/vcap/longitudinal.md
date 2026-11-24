# VCAP Longitudinal

Source: [Salthouse (2024), VCAP, University of Virginia Dataverse, V1.0](https://doi.org/10.18130/V3/QRCQ08).

Demographic extract after excluding ambiguous keys: 5,672 participants, 2,903 with 2+ and 1,763 with 3+ occasions. The eligible Digit Symbol cohort has 5,622 participants and 12,222 observations. 2,880 participants have repeated scores; 1,748 have 3+. Median maximum follow-up among returners is 6.25 years (range 0.86 to 18.45).

Join Demographics, Test Dates and DigSym1 on SubjID and Occasion. Collapse identical selected rows and exclude conflicting keys. Require occasion 1, a documented baseline date, baseline test and complete baseline covariates. Require a valid date and score on each included occasion. Time is actual elapsed days divided by 365.2425. Digit Symbol is the number of correct matches in 120 seconds (0–133). The analysis retains raw score units and models baseline age centered at 60, education centered at 16, recorded sex and age-by-time interaction. Compare participant random intercept and correlated intercept/slope by ML AIC. Coefficient intervals use nlme's t approximation.

| Term | Estimate | 95% CI |
| --- | ---: | --- |
| (Intercept) | 62.214 | 61.578 to 62.851 |
| years | -0.304 | -0.358 to -0.250 |
| age_c | -0.592 | -0.613 to -0.572 |
| educ_c | 1.586 | 1.452 to 1.720 |
| sex1 | 6.887 | 6.133 to 7.640 |
| years:age_c | -0.019 | -0.022 to -0.016 |

## Limitations

This volunteer cohort and observed-follow-up sample are susceptible to selection. A baseline-only record does not establish withdrawal, death or ineligibility. The retest indicator probes a discrete first-retest shift; it cannot isolate practice from aging or other visit differences. Observational associations do not identify causal effects. The prediction applies only to subsequent observed Digit Symbol scores, with heterogeneous time intervals, and has no clinical diagnostic interpretation.
