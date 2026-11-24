# Cognitive Aging Research Lab

Longitudinal Cohort Analytics · Social Epidemiology · Biological Markers · Reproducible Research

One independent portfolio project explores social and biological questions using the same synthetic participants and visits. All scores and marker proxies come from simulation.

[Live Demo](https://cognitive-aging-research-lab.onrender.com)

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
python -m analysis.run --phase 3 --out .analysis-work/reproduced.json
python -m analysis.verify .analysis-work/reproduced.json
python -m analysis.reports
```

The R fits use REML with a participant random intercept, a linear time term, and time interactions with deprivation, age, sex, education and hypertension. Hypertension is included for adjusted description. The causal adjustment set is a separate design question. The reference level is Low deprivation. The incomplete mode uses all retained rows because the outcome and adjustment covariates are present at retained visits. The model assumes independent residuals given the random intercept and covariates. Conditional residual autocorrelation is reported alongside the interval as a diagnostic. Random slopes are outside the model specification.

## Research artifacts

- [Methods](METHODS.md), [provenance](PROVENANCE.md), and [limitations](LIMITATIONS.md)
- [Social report](public/reports/social.md) and [biological report](public/reports/biological.md)
- [Aggregate analysis bundle](src/generated/results.json) and [model card](reports/MODEL_CARD.md)
- [Résumé variants](reports/RESUME.md) and [local verification record](reports/VERIFICATION.md)
- Related independent project: [Aging Genomics Lab](https://aging-genomics-lab.onrender.com)

## Deployment

The [Render Blueprint](render.yaml) defines a single static site. Its build uses the committed results and creates `dist/`. Statistical generation runs offline and in the configured GitHub Actions workflow. Serving the demo requires no running R/Python process, database or web-service cold start. Hosting is subject to the account's static-site build and bandwidth allowance. [Render static site documentation](https://render.com/docs/static-sites)

Before making a remote public, audit staged files, all Git refs and reachable history, and the GitHub repository's releases, pull requests, workflow logs and artifacts. Check known rewritten SHAs if applicable. For a new deployment, use a new GitHub repository and new Render service with the project name. After the first GitHub Actions run passes, check the live page at desktop and 390 px, plus actual CSV, JSON and Markdown downloads.
