# ADNI

[Research index](../README.md) · [Comparison](../DATASET_COMPARISON.md) · [Question matrix](../RESEARCH_QUESTION_MATRIX.md)

## Verified Dataset Characteristics

**Review status** — Metadata Only. Public sources reviewed 2026-11-24.

### Overview, population and structure

Multisite, diagnosis-enriched observational cohort with phase- and diagnosis-specific schedules. The legacy ADNIMERGE documentation shows RID and VISCODE; confirm a current phase-specific visit crosswalk and exam dates.

### Cognitive, social, biological and imaging measures

Official materials show ADAS13, CDRSB, demographic fields, MRI and PET tables, and blood/CSF assay products. The dictionary guide gives PTDEMOG/PTRACCAT as an explicit example. Coverage of a single harmonized hippocampal volume field across selected phases: Not Verified.

### Strengths, limitations and added value

Rich imaging and molecular phenotyping adds value beyond both studies. Recruitment, scanner differences, evolving entry criteria, modality selection and missing visits constrain generalization.

### Access and governance

Access Restricted through LONI IDA approval and DUA. Public ADNI DUA bars AI use for ADNI data, with specific concern about tools that transmit or retain inputs. It prohibits individual-level redistribution and allows summary reporting under its terms.

## Proposed Research Design

**Testable question.** Among a single ADNI phase's participants with baseline MCI, does baseline T1 hippocampal volume improve prediction of 24-month ADAS13 beyond baseline ADAS13, age, sex, education and site?

**Design, analysis and limitations.** Subject-disjoint validation, site-held-out sensitivity, and preprocessing in training only. Define outcome window, harmonize one approved derivative, adjust for head size, benchmark MAE and calibrate uncertainty. Missing scans and delayed visits may select healthier people; referral enrichment limits transport.

**Social and biological suitability.** High biological relevance, low immediate feasibility under the DUA and phase/linkage workload; limited suitability for representative social research.

## Completed Empirical Research

This profile is a public-source evaluation. The proposed design has no project sample estimate or model result.

## Sources

[ADNI data](https://adni.loni.usc.edu/data-samples/adni-data/) · [Dictionary guide](https://adni.loni.usc.edu/quick-start-guide-asset/datadic.html) · [Legacy field examples](https://adni.loni.usc.edu/wp-content/uploads/2012/08/instruction-ADNIMERGE-packages.pdf) · [Data organization](https://adni.loni.usc.edu/quick-start-guide-asset/data_org.html) · [DUA](https://adni.loni.usc.edu/wp-content/themes/adni_2023/documents/ADNI_Data_Use_Agreement.pdf)

[Petersen et al. clinical characterization](https://pmc.ncbi.nlm.nih.gov/articles/PMC2809036/)
