# NACC UDS

[Research index](../README.md) · [Comparison](../DATASET_COMPARISON.md) · [Question matrix](../RESEARCH_QUESTION_MATRIX.md)

## Verified Dataset Characteristics

**Review status** — Metadata Only. Public sources reviewed 2026-11-24.

### Overview, population and structure

US Alzheimer’s Disease Research Center cohort with standardized longitudinal UDS visits beginning in 2005. The v4 dictionary confirms NACCID, NACCVNUM (visit order), VISITDATE and FORMVER. A specific freeze must be pinned.

### Cognitive, social, biological and imaging measures

Dictionary and researcher guide document education and demographic fields, CDR, MoCA and clinician assessments. MRI, biomarker and neuropathology products are requested separately; visit-matched overlap is Not Verified. Do not treat MMSE and MoCA as interchangeable.

### Strengths, limitations and added value

Adds clinically characterized cognitive and functional progression beyond both existing studies. Referral enrichment, center follow-up differences, version changes and ascertainment constrain population inference.

### Access and governance

Access Restricted through Data Front Door request and DUA; optional linked products may have additional limits. Dataset-specific AI permission was Not Verified from reviewed public sources. NACC allows sharing among collaborators covered by the agreement. [Data-file FAQ](https://www.naccdata.org/data-file-faq/).

## Proposed Research Design

**Testable question.** Among UDS participants with baseline MCI and later visits, is education associated with time to first recorded worsening in global CDR, conditional on age, sex, center, baseline CDR and protocol version?

**Design, analysis and limitations.** Model interval-censored progression, treating death as competing where ascertainment permits. Stratify or adjust by center and test robustness to version and follow-up rules. Referral and differential return select cases; education may influence scoring and diagnosis.

**Social and biological suitability.** High clinical relevance, conditional feasibility for UDS-only pilot; imaging and social confounder coverage need a separate decision.

## Completed Empirical Research

This profile is a public-source evaluation. The proposed design has no project sample estimate or model result.

## Sources

[NACC Data Front Door](https://www.naccdata.org/data-front-door) · [Official forms and dictionaries](https://www.naccdata.org/data-forms-and-documentation) · [UDS v4 dictionary](https://files.alz.washington.edu/documentation/uds4-rdd.pdf) · [Researcher guide](https://www.naccdata.org/the-nacc-researchers-guide/)

[Morris et al. original UDS description](https://pubmed.ncbi.nlm.nih.gov/17132964/)
