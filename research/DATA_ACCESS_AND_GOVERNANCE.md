# Data access and governance

NHANES public-use data are governed by the [NCHS Data User Agreement](https://www.cdc.gov/nchs/policy/data-user-agreement.html). This project publishes source references and aggregates.

VCAP V1.0 lists CC0 1.0 in its catalog metadata. The repository's research-only, privacy, secure-storage and citation expectations apply to this workflow. The researcher handles the guestbook and reviews any additional access-screen conditions before supplying files. See the [VCAP access audit](VCAP_ACCESS_AUDIT.md).

OASIS-2 access, AI rules and redistribution conditions will be assessed after VCAP acceptance. UAS CogCF requires registration and review of conditions before accessing participant data. NACC requires a request and applicable data-use agreement. Verify AI use and redistribution with each provider prior to processing. Aggregate release requires disclosure review.

The [HRS AI/LLM policy](https://hrsdata.isr.umich.edu/data-products/ai-llm-use-policy) permits documentation and generic code work. HRS participant data stay in a separate environment inaccessible to AI tools. An authorized human independently runs analysis there. Validate disclosure compliance before sharing aggregated results.

Keep lawful private snapshots and provenance in approved private storage, excluding them from Git and automated browser builds. Before eventual cleanup, verify a backup copy and its checksum for raw sources and authorization records. Derived outputs and caches can be rebuilt when their inputs and environments are available.
