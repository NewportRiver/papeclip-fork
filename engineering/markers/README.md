# Marker Index

Catalog source commit: `63f9c58e5967a7c7a7141e1cc980559fbaf3fe53`

Marker IDs are stable hashes of repository-relative identity. They are retrieval keys, not replacements for source paths.

## Marker types

- `F-XXXXXXXXXX` — tracked file.
- `S-XXXXXXXXXX` — source symbol and line.
- `D-XXXXXXXXXX` — reserved domain/contract marker.
- `T-XXXXXXXXXX` — reserved task marker.
- `C-XXXXXXXXXX` — reserved configuration/contract marker.
- `E-XXXXXXXXXX` — reserved runtime evidence marker.

## Counts

- Files: 9681
- Symbols: 163042
- AU tasks mapped: 37

## Query examples

```sh
python3 - <<'PY'
import json
d=json.load(open('engineering/markers/MARKER_INDEX.json'))
print(next(x for x in d['markers'] if x['path']=='server/src/index.ts'))
print(d['tasks']['AU-035'])
PY
```

Full marker records and task cross-references are in `MARKER_INDEX.json`.
