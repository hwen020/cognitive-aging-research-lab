# Cognitive Aging Research Lab

Longitudinal Cohort Analytics · Social Epidemiology · Biological Markers · Reproducible Research

One independent portfolio project explores social and biological questions using the same synthetic participants and visits. All scores and marker proxies come from simulation.

## Run the demo

```sh
npm ci
npm run dev
```

Open the local URL printed by Vite. [The original offline demo](reference/original-demo.html) is retained as the UI reference. [The implementation specification](CODEX_IMPLEMENTATION_SPEC.md) describes the full research scope.

## Frontend verification

```sh
npm run build
npm test
npx playwright install chromium
npm run test:e2e
```

The browser suite serves the production build and uses desktop and 390 px viewports. It exercises all seven sections, browser history, pagination, marker and wave changes, and actual downloaded CSV/JSON contents. It checks the print button by intercepting the browser print call. Set `COGNITIVE_BROWSER_CHANNEL=chrome` or `msedge` to use an installed system browser.

## Reproduce the longitudinal analysis

Use Python 3.12 and R 4.6.2 with recommended package nlme 3.1.171. See the [data dictionary](DATA_DICTIONARY.md) for fields, provenance and simulated missingness.

```sh
python -m pip install -r requirements.txt
python -m analysis.cohort .analysis-work
python -m pytest -q
Rscript --vanilla tests/unit/mixed_fixture.R
python -m analysis.run --phase 1
```

The R fits use REML with a participant random intercept, a linear time term, and time interactions with deprivation, age, sex, education and hypertension. Hypertension is included for adjusted description. The causal adjustment set is a separate design question. The reference level is Low deprivation. The incomplete mode uses all retained rows because the outcome and adjustment covariates are present at retained visits. The model assumes independent residuals given the random intercept and covariates. Conditional residual autocorrelation is reported alongside the interval as a diagnostic. Random slopes are outside the model specification.
