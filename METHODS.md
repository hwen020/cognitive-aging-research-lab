# Research methods

## Social track

### Repeated observations

The inspection cohort has 2,400 people and five visits over eight years. The modeled outcome is the unitless synthetic cognition score. The R random-intercept model estimates the annual difference in slopes between synthetic deprivation groups, adjusting for baseline age, education, sex and hypertension and their interactions with time. This conditional descriptive contrast differs from the marginal intervention contrast below. Inspect complete and incomplete estimates together. Neither scenario represents a population sample. The reported intervals use the specified working covariance model. Violation of linearity, correlated residuals or informative dropout can affect coverage.

### Causal design

At time zero, a synthetic individual is assigned high or low deprivation by an independent simulator draw. Age, sex category and education precede assignment. The target is the baseline population mean difference in Year-8 cognition under setting assignment to High versus Low, retaining all synthetic pathways through hypertension and CRP. The [directed graph](analysis/causal_dag.dot) includes those paths and the simulated outcome predictors. Sex is included in the propensity model for balance demonstration even though the simulator assigns it no outcome role. Under the actual simulator, the empty set identifies the estimand. The illustrative propensity model includes age, education and sex. Hypertension and CRP are downstream under the specified data generation order.

Fit logistic propensity scores and stabilized ATE weights. Compute a Hájek contrast of normalized weighted means. Balance uses the unweighted pooled group standard deviation for covariate standardized differences before and after weighting. Gate effect reporting at |SMD| ≤ 0.10, a propensity range within [0.05, 0.95], at least 90% of observations inside empirical overlap, and effective sample size ≥ 50 in each group. The percentile interval uses 500 participant bootstrap replicates, refitting propensities and weight cutoffs on each resample. Compare untruncated weights with 1% and 5% symmetric truncation. Use the untruncated estimator as primary.

The incomplete simulation has attrition downstream of exposure and hypertension. Its effect is withheld because a baseline-only IPTW fit would leave censoring unaddressed. Identification in a real cohort would require consistency, well-defined interventions, exchangeability, positivity, and a defensible censoring and measurement model. Neighborhood history, family resources and lifelong health could jointly influence residential trajectory and cognition in an observational cohort. The simulated overlap and weight checks cannot diagnose those omitted common causes.

## Biological track

In separate REML models for CRP, p-tau and NfL, add the participant's baseline marker value and the current value minus baseline to the social longitudinal specification. Each coefficient is a difference in simulated score units per one simulated marker unit. The change term is a contemporaneous conditional association. Do not give it a temporal or mechanistic interpretation. Marker-specific complete rows are used, including a measured baseline, and exclusions are reported per model. The within-mode Benjamini–Hochberg family consists of all six marker terms. Values remain on their original simulation scale without winsorization.

### Prediction

The target is observed Year-8 cognition. Eligibility is fixed first, then participants are split once per simulation using a seeded 75%/25% split. The allowlist contains baseline age, sex, education, deprivation, and hypertension, optionally augmented with baseline CRP, p-tau and NfL. Baseline and intermediate cognitive scores are excluded. No participant appears in both partitions. GroupKFold inside training selects the Ridge penalty and Random Forest leaf size by MAE. Column transforms fit within each fold. The mean benchmark uses the training outcome mean.

Evaluate all models on the same holdout within a mode. Holdout MAE, RMSE and R² intervals come from 500 paired resamples of participants and condition on the trained predictions. Compare augmented and social models with the same bootstrap draws and report augmented-minus-social MAE. Subgroup MAE describes the two simulated sex categories. Permutation importance is the increase in MAE under held-out feature shuffling. It may be diluted or distorted by correlated features. The incomplete-mode estimates apply to participants with observed targets. Both marker-comparison methods have uncertainty intervals crossing zero in both modes. The simulation supplies no clinical validation or external generalization.
