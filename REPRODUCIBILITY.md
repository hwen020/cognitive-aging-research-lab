# Reproduce NHANES aggregates

Use Python 3.12 with pandas (see `requirements.txt`) and R 4.6.2 with survey and jsonlite. The recommended R package rpart is included in the R distribution.

```sh
python -m analysis.nhanes
Rscript --vanilla analysis/r/nhanes.R
```

The first command downloads and verifies the eight XPT files and eight official codebooks, validates numeric fields, checks unique survey-cycle keys and writes the ignored analytical CSV. The R release pipeline reads that file and writes only aggregate results. The synthetic pipeline uses separate sources, commands and results.

Run `python -m analysis.nhanes_release` to regenerate published artifacts. Run `python -m analysis.verify_nhanes` to compare with the tracked result. R 4.6.2, survey 4.5 and jsonlite 2.0.0 were used for initial execution. Retain official XPTs and codebooks in ignored local storage. Raw files are reproducible from the source manifest; the derived CSV can be regenerated. Site artifacts contain no individual rows.
