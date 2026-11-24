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
