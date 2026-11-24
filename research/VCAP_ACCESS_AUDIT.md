# VCAP source and access audit

Initial metadata review: 2026-11-24. Local verification was subsequently performed under the project authorization. See the VCAP data audit for the measured cohort and source field mapping.

Salthouse, Timothy (2024), VCAP Longitidunal Dataset, University of Virginia Dataverse, V1.0. [Dataset and download instructions](https://doi.org/10.18130/V3/QRCQ08). [Public Dataverse metadata API](https://dataverse.lib.virginia.edu/api/datasets/:persistentId/?persistentId=doi%3A10.18130%2FV3%2FQRCQ08).

| Official file | ID | Bytes | Catalog MD5 |
|---|---:|---:|---|
| Virginia Cognitive Aging Project Datasets 2001-2019.xlsx | 68817 | 109534974 | `29102b594f50f2a0ee71def49b087071` |
| VCAP_CodeBook.pdf | 68818 | 9292967 | `6aab94004eddc5ab123e55250c9d1c86` |
| Dataset description.pdf | 68819 | 36378 | `1de11ebc687bb582f32404f0e3e4b027` |

The catalog describes multiple occasions linked to participants and demographic, cognitive and non-cognitive measures. The catalog's approximate participant count describes the archive. It does not establish the eligible analytic cohort. Actual repeat counts, observation intervals, date resolution, test comparability, education coverage and practice effects remain unverified.

The API reports CC0 1.0. The dataset description separately requests a signed guestbook, research-only use, no participant identification, secure storage and appropriate citation. The researcher completes the guestbook personally and verifies any access-screen conditions before the files are processed. Keep authorized downloads and access documentation in private storage. The project uses the ignored `.analysis-work/vcap/` directory for local input. Do not send workbook rows to CI or include them in logs, artifacts, Git or website files.

After access, record retrieval date and local SHA-256, confirm the catalog checksum, read the manual, audit keys and test definitions, and establish elapsed time from documented fields. Measure unique participants, at least two and at least three eligible observations, and test-level repeat coverage. Document exclusions before fitting. If an elapsed-time variable cannot be validated, revise the estimand instead of imputing follow-up intervals from wave order.
