# VCAP Reproducibility

Source: [Salthouse (2024), VCAP, University of Virginia Dataverse, V1.0](https://doi.org/10.18130/V3/QRCQ08).

Workbook SHA-256: `9388aa0d6afed2f75528b4978e0fba98371fbc3af44322fd83c8b54c9dac2b0a`. R 4.6.2 and nlme 3.1.171. From the repository root with the authorized workbook in .analysis-work/vcap, install openpyxl, pandas, scikit-learn and NumPy, plus R nlme and jsonlite. The verified Windows environment used Python 3.11.7, pandas 2.1.4, NumPy 1.26.4, scikit-learn 1.2.2, and openpyxl 3.0.10.

```sh
python -m analysis.vcap
Rscript analysis/r/vcap.R .analysis-work/vcap/analysis-private.csv .analysis-work/vcap/model.json
python -m analysis.vcap_prediction
python -m analysis.vcap_release
```

Keep all row-level inputs and derived records local and untracked.
