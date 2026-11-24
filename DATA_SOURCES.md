# Research data sources

NHANES 2011–2012 and 2013–2014 are separate public CDC/NCHS survey cycles. The source manifest records both the official SAS transport and codebook URLs, file sizes, SHA-256 hashes, publication dates where documented, and the CDC variable labels for CFQ, DEMO, BPX and GHB. The download command validates both files against this manifest. Use CDC's moved `/Nchs/Data/Nhanes/Public/{year}/DataFiles/` paths. See [source manifest](analysis/nhanes_sources.json) and [CDC cognitive testing documentation](https://www.cdc.gov/healthy-aging-data/nhanes/index.html).

HRS documentation and policy are listed in [Data governance](DATA_GOVERNANCE.md). No HRS dataset is bundled or executed.