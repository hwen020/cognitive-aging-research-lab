# Codex implementation directive — Cognitive Aging Research Lab

## 0. Mission / non-negotiable intent

Build **one credible, methods-first research portfolio project** relevant to two DIFFERENT UW–Madison Caunca Research Lab positions:
- Social Data Scientist: social determinants, epidemiology, longitudinal cohorts, observational causal inference.
- Biological Data Scientist: biomarkers, neurodegeneration, data harmonization, predictive modeling, high-dimensional analytical workflows.

**Do not turn this into a generic AI dashboard.** The technical centerpiece must be statistical validity, research reproducibility, dataset provenance, explicit assumptions, and defensible limitations. A single repository, one Live Demo, two clearly delineated analysis tracks sharing a common cohort schema and pipeline.

This package contains a functional static UX and synthetic-data prototype (`index.html`). It is a REFERENCE UI and acceptance baseline, **not evidence of fitted causal models or predictive performance**. Rebuild it into a real full-stack research demonstration with validated computational analyses, rather than simply copying its visuals.

## 1. Existing assets / protect unrelated work

- Preserve the already published `aging-genomics-lab` repository, live URL, data, history and public results; DO NOT overwrite or refactor it without explicit need/permission.
- Preserve other applications (`wearable-mobility-research-pipeline`, `travel-desk-demo`, Social DS drafts, private DMC operations) untouched.
- Default to NEW repository `cognitive-aging-research-lab` with this package as input; this supersedes an earlier suggestion to modify Aging Genomics directly. Keep Aging Genomics as an independent related portfolio link. Do not rename or force-push existing repos.
- If a partially implemented Social Data Scientist prototype exists locally, inspect first. Reuse functioning components and historical Git commits rather than start over. Keep all existing data and links where practical. Do not alter an existing published app without checking whether doing so breaks it.

## 2. Immediate output / no fake results

1. Materialize the static demo into a Vite + React + TypeScript project with responsive navigation and pages:
   Overview; Cohort Explorer; Longitudinal Analysis; Causal Inference; Biomarker Explorer; Prediction Modeling; Research Report.
2. Use data-backed queries and computed results. Never invent r, p, AUC, CI, coefficient, q-value or effect estimates as hard-coded UI values.
3. Label all synthetic sources and exploratory outputs conspicuously. Causal inference and predictive evaluation screens can display `Not yet computed` until a validated pipeline is implemented. No medical claims.
4. Deliver runnable local app, tests, dev README, provenance, GitHub Actions, deployment config, and a handoff checklist.
5. Favor professional research-software usability over decorative graphics.

## 3. Architecture

Preferred practical stack:
- Frontend: React + TypeScript + Vite; accessible responsive layout; Plotly or Recharts for accessible charts; TanStack Query optional.
- Backend: FastAPI (Python 3.12+), Pydantic v2, pandas/Polars, NumPy, SciPy, statsmodels, scikit-learn.
- Reproducible statistical component: R >= 4.3, renv with packages such as lme4/lmerTest, broom.mixed, ggplot2, survey, WeightIt/cobalt (only if appropriate and audited). R scripts callable via a documented CLI or versioned analysis job. If Render Free cannot run R within limits, run analysis in reproducible CI and publish versioned, immutable artifacts; don't silently replace intended R models with mock metrics.
- Data: parquet/CSV curated synthetic demo, plus versioned metadata; SQLite or DuckDB for the read-only demo. Avoid persistent PostgreSQL if unnecessary for free deployment.
- Tests: pytest for data/statistics/API, Vitest for UI logic, Playwright desktop + 390px mobile E2E; CI with GitHub Actions.
- Deployment: one Render Free service only if within practical limits, or static frontend + published precomputed validated artifacts. Document cold starts and cost constraints. Do not use a service that needs an always-running paid worker for an occasional portfolio demo.

Recommended structure:
```
frontend/src/{components,pages,features,api,styles,types}
backend/app/{main.py,models.py,services,api}
analysis/{r,python,notebooks}
data/{synthetic,manifests,schemas}
reports/{social,biological,model_cards}
tests/{unit,integration,e2e}
.github/workflows/ci.yml
README.md, DATA_DICTIONARY.md, METHODS.md, PROVENANCE.md, LIMITATIONS.md
```

## 4. Common longitudinal cohort contract

Synthetic dataset MUST be generated from a fixed seed with a verifiable generator, and regenerated identically on different machines.
- Cohort target: 2,400 participants x 5 waves at years [0, 2, 4, 6, 8] = 12,000 baseline demo observations before optional attrition.
- Canonical keys: `participant_id`, `visit_year`; enforce uniqueness and ordered waves.
- Baseline features: `age_at_baseline`, `sex` (synthetic categorical example, do not imply exhaustive biological definitions), education_years, socioeconomic/deprivation index, baseline hypertension, optional smoking/diabetes.
- Repeated features: `age_at_visit`, CRP-like proxy, p-tau-like proxy, NfL-like proxy, cognitive score; additional clinical or imaging derived variables only with clear provenance.
- Data dictionary: name, type, unit, wave availability, allowed range, missingness, synthetic/real source status, lineage.
- Must include realistic missingness and attrition as a separately labeled simulation mode and document its assumptions; all analyses must report complete-case and/or justified handling.
- Never present synthetic biomarkers as authentic human assay measurements or clinical normal ranges; p-tau and NfL demo units remain arbitrary unless backed by authorized source documentation.
- Any externally sourced data must follow the license, terms and access requirements and have a reproducible accession, URL, retrieval date, checksum and data transformation manifest.

## 5. Social research pathway (essential)

- Social determinants explorer: stratify by deprivation, education and vascular risk with descriptive n and missingness.
- Longitudinal trajectories: actual repeated-measures analysis (not just charting means) in R using random participant intercept; justify random slopes if added. Prespecify covariate adjustments and interactions. Show estimate, CI, assumptions, sample counts and diagnostics; avoid p-value-only story.
- Causal research plan: research question, target estimand, formal DAG (with direction and timing), adjustment set, unmeasured confounding discussion, time-zero definition.
- Implement a transparent IPTW observational analysis only if exposure and confounders make a defensible estimand: propensity model, overlap/positivity, stabilized weights, truncation sensitivity, standardized mean differences before/after, effective sample size, robust uncertainty. Explain why causal interpretation remains conditional. Do not treat post-exposure mediators as confounders by default.
- Include a clear **no causal inference computed** state if the above validation isn't implemented.

## 6. Biological research pathway (essential)

- Biomarker explorer: CRP, p-tau, NfL synthetic proxies; variable distributions, participant-filtered plots, measured or simulated missingness, winsorization decisions, correlations and multiple-testing note.
- Statistical modeling: adjusted regressions / mixed-effects fits with model specification, coefficient/CI, diagnostics and explicitly defined outcome scales. Respect repeated measures.
- Prediction question: predict Year-8 cognition using only features available at or before baseline. Prediction horizon/eligible participants defined before splitting.
- Models: no-feature mean baseline, Ridge/Lasso, Random Forest (optional Gradient Boosting). Evaluation: held-out participant split; GroupKFold if multiple records are used; preprocessing fit inside training folds; ensure no leakage by participant, timepoint, normalization, or report-generation.
- Report MAE, RMSE, R² on held-out participants, bootstrap or appropriate CI and subgroup errors. If models aren't actually trained, show no metrics.
- Biomarker improvement test: baseline demographic/social model vs. baseline + biomarkers; paired participant-level comparison and uncertainty. Don't claim clinical value based only on a synthetic score difference.
- Feature importance: permutation importance on held-out test set if model supports it; no mechanistic or causal conclusions from feature ranks.
- If including neuroimaging in a later phase, use only permitted imagery/derived features and explicitly distinguish image features from measured biomarkers.

## 7. Pages and functional behavior

1. **Overview** — dataset provenance badge, cohort metrics, synthetic trajectories, two-track research structure, validity warnings.
2. **Cohort Explorer** — filters by wave, sex, deprivation, hypertension, with reactive unique participant and row counts; table virtualization/pagination; full filtered CSV; JSON data dictionary.
3. **Longitudinal Analysis** — group trajectories, actual adjusted model results with n/CI and methods; fallback non-inferential means clearly labeled.
4. **Causal Inference** — formalized DAG, estimand, confounders, model diagnostics; no fake effect.
5. **Biomarker Explorer** — wave and marker selectors, scatterplots/correlations computed from selected data, clear units and multiple-testing caveat.
6. **Prediction Modeling** — experiment setup, split audit, baseline comparisons, metrics only after real pipeline runs, model card, data leakage guardrails.
7. **Research Report** — downloadable provenance-rich JSON and independently reproducible HTML/PDF/Markdown scientific reports for social and biological tracks. PDF optional if environment supports it; do not fake results.

Common UX: accessible tables/charts; functional keyboard navigation; no dead buttons; responsive desktop and 390px phone; loading/error/empty states; no identifiable records. Import only approved public data; no upload of private patient data to a public demo.

## 8. Tests and measurable acceptance criteria

- `pytest -q` green; type checking/lint green; frontend unit tests green; Playwright smoke on Chromium desktop/mobile.
- Deterministic generator: fixed seed creates identical CSV SHA-256; 2,400 unique IDs; exactly 12,000 initial rows; expected five waves; unique composite key.
- Filtering data changes both charts and CSV consistently. Exported CSV header, row count and selected filter agree with UI.
- Statistical regression results tested on a tiny known synthetic fixture against separately calculated expected values and tolerances; model outputs have methodological provenance.
- Causal module refuses to report an effect when balance or overlap diagnostics fail.
- Prediction: group train/test person ID overlap = 0; all features available by prediction cut-off; no preprocessing fitted on test set; reproducibility with fixed seed.
- Biomarker chart association values recalculate from selected wave; misleading causal/clinical language absent.
- Validate privacy and secrets: no real participant data, API keys, private emails, tokens, personally identifying information or employer data in repo/history/artifacts.
- Render release check: `/healthz` if backend exists; desktop/mobile page flows; real download contents; no blocking auth; reproducible docs.

## 9. Suggested delivery phases

**P0 — portfolio-ready UI**: preserve interactive demo behavior, synthetic banners, export, responsive navigation, data dictionary, tests, docs. No false model claims.
**P1 — actual longitudinal statistics**: R package locking, mixed-effects models, assumptions/diagnostics, provenance-bearing artifacts.
**P2 — causal estimand and validation**: DAG, IPTW only where identifiable under stated assumptions, diagnostics + sensitivity.
**P3 — biological analytics / prediction**: adjusted biomarkers, proper participant-level held-out evaluation, benchmark comparisons, model cards.
**P4 — research-facing polish**: publication-style report export, public dataset integration where legally available, deployment and CI release.

For each phase: code -> tests -> review -> docs -> git commit. Do not claim a phase passes until actually verified. If package or service constraints block real analysis, document limitation and retain an honest not-computed state.

## 10. Codex operating instructions

1. Inspect supplied demo and any existing social DS project. Print repo/file inventory and explain what will be reused before editing.
2. Implement incrementally; do not delete old repositories/branches, database records or published URLs.
3. Give short check-ins with changed files, actual commands, tests and remaining limitations.
4. Commit in logical small increments (no force push); before publishing run secret scan, license review and docs checks.
5. Do NOT submit job applications or claim results; this project is portfolio infrastructure. Create distinct resume bullets for Social DS and Biological DS using only features actually implemented and verified.
6. Return: local run commands, tested feature matrix, test outputs, repository/commit if pushed, Live Demo link if actually deployed, explicit list of unfinished requirements.

## 11. Branding and portfolio positioning

**Name:** Cognitive Aging Research Lab
**Subtitle:** Longitudinal Cohort Analytics · Social Epidemiology · Biological Markers · Reproducible Research
**Narrative:** A research-grade, transparent workflow that integrates cohort harmonization, longitudinal statistics, causal design and biomarker-aware predictive modeling. State which components are implemented vs planned. Do not label synthetic research as a clinical study or report statistically invalid findings.

Portfolio variants from ONE repository:
- Social DS emphasis: harmonization, social exposure, trajectories, DAG/IPTW, observational study limitations.
- Biological DS emphasis: longitudinal biological markers, data integrity, regression/ML, leakage-proof validation, reproducibility.
