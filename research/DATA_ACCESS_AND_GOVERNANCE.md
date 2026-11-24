# Data access and governance

[Research index](README.md) · [Dataset comparison](DATASET_COMPARISON.md)

Reviewed 2026-11-24. The review uses official public documentation and original publications. No applications or agreements were submitted. The profile links document provider-specific conditions; silence about AI does not establish permission.

| Dataset | Access and policy assessment |
| --- | --- |
| [NHANES 2011–2014](datasets/nhanes.md) | Public use subject to the NCHS agreement, statistical use and no reidentification. Dataset-specific AI permission: Not Explicitly Specified in the cited agreement. |
| [VCAP V1.0](datasets/vcap.md) | CC0 catalog label plus guestbook, research-only and no identification expectations, secure storage and citation. Dataset-specific AI terms: Not Explicitly Specified in the cited catalog. This review used metadata and the existing published audit. |
| [OASIS-2](datasets/oasis-2.md) | Access Restricted for implementation. WashU lists an application, institutional email and data-use terms. Terms require attribution and prohibit identification; AI permission Not Explicitly Specified in reviewed public materials. |
| [OASIS-3](datasets/oasis-3.md) | Access Restricted. WashU application and terms plus NITRC account are documented. Release-specific restrictions on further disclosure apply. AI permission Not Explicitly Specified in reviewed terms. |
| [MIDUS](datasets/midus.md) | Use official archive terms. MIDUS explicitly prohibits redistributing obtained data and describes restricted imaging/genomics repositories. AI permission Not Explicitly Specified in reviewed MIDUS policy. Individual biomarker catalog endpoint returned HTTP 429 during review. |
| [NHATS](datasets/nhats.md) | Public-use files require registration; sensitive files require application. Public-use conditions prohibit uploads to public AI platforms and limit transfer to supervised staff or students; other collaborators need separate access. Aggregate reporting and citation are required. [Official conditions](https://www.nhats.org/data-access). |
| [ADNI](datasets/adni.md) | Access Restricted through LONI IDA approval and DUA. Public ADNI DUA bars AI use for ADNI data, with specific concern about tools that transmit or retain inputs. It prohibits individual-level redistribution and allows summary reporting under its terms. |
| [ELSA](datasets/elsa.md) | UKDS licensed access; linked/genetic data have separate access. UKDS security guidance prohibits consumer AI uploads of individual records. Fully local tools are considered separately under the EUL; any external or institutional AI use must be assessed under the applicable terms. |
| [UAS CogCF](datasets/uas-cogcf.md) | Registration and an individual DUA are required. UAS prohibits sharing microdata with generative AI and requires collaborators to have separate accounts and DUAs. [UAS data management policy](https://uasdata.usc.edu/index.php?pid=Data+Management+Policies+and+Services&type=3). |
| [HRS / RAND HRS](datasets/hrs.md) | Public documentation is reviewable; files require registration and conditions. HRS explicitly prohibits AI processing of person-level HRS data, including RAND releases. A human-operated approved environment is required for any future empirical execution. |
| [NACC UDS](datasets/nacc.md) | Access Restricted through Data Front Door request and DUA; optional linked products may have additional limits. Dataset-specific AI permission was Not Verified from reviewed public sources. NACC allows sharing among collaborators covered by the agreement. [Data-file FAQ](https://www.naccdata.org/data-file-faq/). |

For future approved analyses, record the release, signed terms, field-level lineage and access classification in an approved environment. Exclude individual records, raw/derived imaging, access documents and restricted join keys from public Git, CI and deployment. Review attribution and permissible sharing separately for inputs, derivatives and aggregate outputs. For HRS, retain the human-operated analysis separation. Unresolved AI or redistribution terms remain review gates for future empirical work, without blocking public documentation research.
