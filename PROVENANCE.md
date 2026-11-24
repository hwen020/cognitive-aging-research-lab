# Provenance and release scope

- Participant records are generated locally from seed 20261123. The complete CSV checksum is independently verified in Python and TypeScript. The second scenario adds only generated dropout and omissions. See the [data dictionary](DATA_DICTIONARY.md).
- The React app uses the supplied offline prototype for layout and interaction. It loads no third-party data, fonts, imagery or scripts at runtime. The cohort exports contain generated identifiers and values.
- The published build is designed to serve the versioned aggregate artifact and two method reports. The artifact records input fingerprints, method source fingerprints, numeric runtime versions, counts, effect-reporting gates and model audits. Raw CSVs are generated on demand and excluded from Git.
- Project authorship and licensing are separate from dependency licenses. The repository does not declare a license for original project content. No external cohort dataset is bundled. Package names and versions appear in the npm lockfile and Python requirements. R uses the recommended nlme shipped with the pinned distribution.
