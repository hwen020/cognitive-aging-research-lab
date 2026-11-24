# Research methods

## Social track

### Repeated observations

The inspection cohort has 2,400 people and five visits over eight years. The modeled outcome is the unitless synthetic cognition score. The R random-intercept model estimates the annual difference in slopes between synthetic deprivation groups, adjusting for baseline age, education, sex and hypertension and their interactions with time. This conditional descriptive contrast differs from the marginal intervention contrast below. Inspect complete and incomplete estimates together. Neither scenario represents a population sample. The reported intervals use the specified working covariance model. Violation of linearity, correlated residuals or informative dropout can affect coverage.

### Causal design

At time zero, a synthetic individual is assigned high or low deprivation by an independent simulator draw. Age, sex category and education precede assignment. The target is the baseline population mean difference in Year-8 cognition under setting assignment to High versus Low, retaining all synthetic pathways through hypertension and CRP. The [directed graph](analysis/causal_dag.dot) includes those paths and the simulated outcome predictors. Sex is included in the propensity model for balance demonstration even though the simulator assigns it no outcome role. Under the actual simulator, the empty set identifies the estimand. The illustrative propensity model includes age, education and sex. Hypertension and CRP are downstream under the specified data generation order.

Fit logistic propensity scores and stabilized ATE weights. Compute a Hájek contrast of normalized weighted means. Balance uses the unweighted pooled group standard deviation for covariate standardized differences before and after weighting. Gate effect reporting at |SMD| ≤ 0.10, a propensity range within [0.05, 0.95], at least 90% of observations inside empirical overlap, and effective sample size ≥ 50 in each group. The percentile interval uses 500 participant bootstrap replicates, refitting propensities and weight cutoffs on each resample. Compare untruncated weights with 1% and 5% symmetric truncation. Use the untruncated estimator as primary.

The incomplete simulation has attrition downstream of exposure and hypertension. Its effect is withheld because a baseline-only IPTW fit would leave censoring unaddressed. Identification in a real cohort would require consistency, well-defined interventions, exchangeability, positivity, and a defensible censoring and measurement model. Neighborhood history, family resources and lifelong health could jointly influence residential trajectory and cognition in an observational cohort. The simulated overlap and weight checks cannot diagnose those omitted common causes.
