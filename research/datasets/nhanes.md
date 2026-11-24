# NHANES 2011–2014

[Research index](../README.md) · [Comparison](../DATASET_COMPARISON.md) · [Question matrix](../RESEARCH_QUESTION_MATRIX.md)

## Verified Dataset Characteristics

**Review status** — Completed Empirical Research. Public sources reviewed 2026-11-24.

### Overview, population and structure

Two independent national cross-sections; U.S. civilian noninstitutionalized population. Cognitive component targets ages 60+. Within a cycle SEQN links questionnaire, exam and laboratory records; it cannot construct repeat visits.

### Cognitive, social, biological and imaging measures

CFQ_H and CFQ_G document CFDDS (DSST), CFDAST (animal fluency) and CERAD recall fields. DEMO_H documents INDFMPIR (family poverty-income ratio), DMDEDUC2, age, sex, masked strata and PSUs. BPX_H and GHB_H document examination blood pressure and LBXGH (HbA1c). MRI coverage is Not Verified for this analysis.

### Strengths, limitations and added value

Strong social and cardiometabolic coverage and explicit survey design. Item nonresponse, exam eligibility, institutional exclusion and reverse causation limit inference. This is the existing weighted cross-sectional benchmark; VCAP adds within-person change.

### Access and governance

Public use subject to the NCHS agreement, statistical use and no reidentification. Dataset-specific AI permission: Not Explicitly Specified in the cited agreement.

## Proposed Research Design

**Testable question.** Among adults aged 60+ with eligible cognitive assessments, is lower poverty-income ratio associated with lower DSST performance after accounting for age, education, sex, race/ethnicity and survey cycle?

**Design, analysis and limitations.** Pooled design-weighted cross-sectional regression with strata/PSU and eligible examination weights. Check functional form and compare complete-case estimates with a missingness sensitivity analysis. Educational opportunity and health may confound the association; survival and exam participation may select the sample. Temporal direction is unidentified.

**Social and biological suitability.** High for cross-sectional social and cardiometabolic inference; unsuitable for within-person trajectories.

## Completed Empirical Research

Existing project analysis covers survey-weighted cross-sectional associations and cross-cycle prediction of contemporaneous cognitive performance. The proposed question below refers to a design, independently of the existing result. [Existing social report](../../public/nhanes/social.md) · [Existing biological report](../../public/nhanes/biological.md)

## Sources

[CDC cognition codebook](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/CFQ_H.htm) · [Demographics](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/DEMO_H.htm) · [Blood pressure](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/BPX_H.htm) · [HbA1c](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/GHB_H.htm) · [Weighting](https://wwwn.cdc.gov/nchs/nhanes/tutorials/weighting.aspx) · [NCHS agreement](https://www.cdc.gov/nchs/policy/data-user-agreement.html)

[CDC original cognitive performance report](https://www.cdc.gov/nchs/data/nhsr/nhsr126-508.pdf)
