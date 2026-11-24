# Synthetic longitudinal cohort

The same fixed seed, 20261123, produces 2,400 participants and five scheduled visits in the browser and Python. The canonical complete CSV SHA-256 is `5104d2c3ca510a4f0ac537652c3f4b76f6b4e567d42cad9029c3b24b5297de74`. Encoding is UTF-8 with LF line endings and decimals without trailing zeroes. All fields are generated locally.

| Field | Type, units, validity and lineage |
| --- | --- |
| `participant_id` | String, P0001–P2400, sequential artificial key |
| `visit_year` | Integer years since baseline, 0/2/4/6/8, unique within participant |
| `age_at_baseline` | Decimal years, 54–84, seeded draw before exposure |
| `age_at_visit` | Decimal years, baseline age plus visit year |
| `sex` | Synthetic categorical example, Female/Male, independently drawn at baseline |
| `deprivation` | High/Low, assigned via a seeded probability at baseline |
| `education_years` | Decimal years, 9–20, seeded pre-exposure draw |
| `hypertension` | Yes/No, proxy drawn conditional on age and deprivation |
| `crp` | Nonnegative decimal proxy, simulated mg/L, generated using age-related risk, deprivation, visit and noise |
| `ptau`, `nfl` | Nonnegative decimal proxies in arbitrary simulation units, generated from age, visit and noise |
| `cognitive_score` | Unitless score, accepted range 0–150, generated from individual intercept, visit, covariates, markers and noise |

Complete mode has every field at every scheduled visit. The separately labeled incomplete mode retains every baseline visit, then simulates permanent dropout with visit-specific probability 0.025 + 0.025 × High deprivation + 0.02 × hypertension. Independent per-marker draws omit measurements at probability 0.03 + 0.02 × High deprivation + 0.03 × Year 8 among retained rows. Missing markers are blank in CSV. QC validates required fields, ranges, invariant baseline fields, ordered waves and unique keys.

## Official NHANES module

The [parsed source manifest](analysis/nhanes_sources.json) records selected official fields and their source codebooks. SEQN and cycle are local merge keys only. Positive `WTMEC2YR / 2` supplies the pooled MEC weight. `SDMVSTRA` and `SDMVPSU` supply masked variance units. `RIDAGEYR` is age (top-coded by CDC), `RIAGENDR` is recorded sex, `RIDRETH3` is the published race/Hispanic-origin category, `DMDEDUC2` is education (special codes 7 and 9 become missing), and `INDFMPIR` is poverty income ratio (valid range 0–5). CERAD immediate recall sums three completed trials, and delayed recall, animal fluency and DSST use official score fields. HbA1c uses `LBXGH` (%) and pressure uses the mean of available systolic or diastolic readings in mm Hg. A reading count supports the BP sensitivity analysis.
