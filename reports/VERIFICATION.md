# Local verification record

Verification environment: Windows, Python 3.12.10, R 4.6.2 with nlme 3.1.171, Node 20.16.0, and system Chrome driven by Playwright. Browser tests serve the production bundle and use desktop and 390 px viewports.

| Phase | Passed locally | Earlier failures or pending remote checks |
| --- | --- | --- |
| P0 | TypeScript/Vite build, two cohort/association tests, six browser checks | Initial browser runs caught an unbound correlation display and ambiguous locators. An Edge/dev-server run also timed out. The fixes and production-preview Chrome run passed all six checks. |
| P1 | Two Python cohort tests, R analytic slope fixture, complete and incomplete nlme fits, production build | Both languages generated the same complete CSV SHA-256. The incomplete cohort had 11,004 visits and 2,013 observed Year-8 outcomes. |
| P2 | Three IPTW tests, complete and incomplete pipeline outputs, six browser checks after integrating results | Deliberate propensity separation and simulated dropout withheld results as intended. The complete simulation passed the reporting gates. |
| P3 | Three prediction tests, six R biomarker fits across two modes, five trained/evaluated comparators per mode, six browser checks | Complete and incomplete holdouts each had zero participant overlap. All paired marker comparison intervals included zero. |
| P4 | Eight Python tests, R slope fixture, clean regeneration and numeric comparison, production build, two JavaScript tests, and six browser checks including research report downloads | GitHub Actions and live Render verification require authenticated accounts and are pending. The print check verifies the browser print invocation. Standalone PDF generation was skipped. |

## Evidence

- Complete simulation: 2,400 participants, 12,000 rows, five visits. Holdout split 1,800 train / 600 test.
- Simulated attrition and missingness: 2,400 baseline participants and 11,004 rows. Holdout split 1,509 train / 504 test among 2,013 participants with a Year-8 outcome.
- Reproduction: `python -m analysis.run --phase 3 --out .analysis-work/reproduced.json`, then `python -m analysis.verify .analysis-work/reproduced.json`. Exact comparisons cover cohort checksums, feature timing, split counts and source fingerprints. Numeric tolerances are documented in the verification code.
- The first GitHub Actions browser job reached the production build, then Playwright rejected the `ubuntu-latest` runner image (Ubuntu 26.04). The workflow pins Ubuntu 24.04 for the browser installation and analysis runtime. A local production preview verifies the static output. No backend health endpoint applies to this static design.
