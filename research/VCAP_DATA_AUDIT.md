# VCAP data audit

The [VCAP V1.0 release](https://doi.org/10.18130/V3/QRCQ08) includes a workbook, the Dataset Description and a 297-page Codebook. All three match the catalog MD5 values. The workbook SHA-256 is documented in the reproduction report. The workbook contains 83 sheets, including an effectively empty Sheet1. The analysis uses three selected sheets.

| Workbook field | Interpretation |
| --- | --- |
| SubjID and Occasion | Participant and repeat occasion keys. Session number within a burst is separate. |
| Test Dates / Session 1 | Recorded first-session test date per occasion. Years are elapsed calendar days divided by 365.2425 from occasion 1. |
| DigSym1 / Score | Session 1 Digit Symbol correct matches in 120 seconds, 0–133. Codebook p. 22. |
| Demographics / Age, Educ, Sex | Baseline age, years of education, recorded sex (0/1), all from occasion 1. Codebook pp. 7–10. |
| Recall1, MMSE, other cognition sheets | Inventory only. No pooling across tests or alternate session forms. |

Demographics, Test Dates and DigSym1 each had six conflicting-key rows. All rows for those keys were excluded. After cleaning keys the linked demographic extract has 12,332 records from 5,672 participants. There are 2,903 participants with at least two occasions and 1,763 with at least three. The eligible analysis has 12,222 records from 5,622 participants. Of these, 2,880 have at least two and 1,748 at least three measurements. There were no unmatched retained test/date keys or participants with a nonincreasing sequence of observed dates.

The Codebook uses -99 for missing/refused in selected fields. Score, age, education and sex are checked against their documented bounds or categories. Date order and ambiguous records are checked before model fitting. Using one test from the same session each occasion preserves common scoring, while retesting and changes in administration remain possible. No MRI, assays or diagnoses enter the analysis. [Data quality report](../reports/VCAP_DATA_QUALITY.md)
