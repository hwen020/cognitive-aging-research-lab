# Study designs and statistical methods

[Research index](README.md) · [Dataset profiles](README.md#dataset-profiles)

| Design | Candidate datasets | Primary analysis and uncertainty | Diagnostic / sensitivity |
| --- | --- | --- | --- |
| Pooled survey cross-sections | NHANES | Design-weighted regression and design-based intervals within eligible domains | Correct exam weights, item missingness, independent cycles |
| Dated repeated cognitive testing | VCAP, MIDUS, ELSA, UAS, HRS | Mixed models with exposure-by-time or design-weighted panel estimates where applicable; participant or household-aware uncertainty | Practice, instrument versions, clustering, observation weights and dropout |
| Older-adult annual panels with proxies | NHATS, HRS | Define survivor/observed estimand and separately model response, proxy transition and death | Contrast design weights with attrition sensitivity; avoid assigning test scores to proxy visits |
| Repeated structural imaging | OASIS-2, OASIS-3, ADNI | Participant-level trajectories or validated landmark prediction with prespecified MRI/clinical timing | Compare timing windows, check scanners and processing versions, assess return selection |
| Clinical progression | NACC, ADNI, OASIS-3 | Interval-censored clinical progression or ordinal repeated outcome, accounting for competing death when available | Freeze and protocol version, baseline diagnosis, site effects and endpoint misclassification |

Prediction requires participant-disjoint splits, input availability before the index landmark, fold-local preprocessing and a simple baseline. Site-held-out validation is a sensitivity analysis when cohort size supports it. Paired held-out error intervals quantify incremental value. Repeated visits must never be treated as independent training and test observations. Proposed regressions estimate associations unless a distinct identification design is justified.
