# Judged-to-candidate Space subset check

- Judged revision: `9494ace83ec1c99632a33b773f64c82e12891405`
- Protected manifest: 17 files
- Candidate tree: 22 files
- Missing judged paths: 0
- Byte-identical judged files: 16
- Intentionally changed judged file: `logbook.json`

`logbook.json` retains the original five child entries in their original order
and adds two new children. All six historical Markdown pages and all ten other
assets are byte-identical to the judged revision. The old path set is therefore
a subset of the candidate path set; the only modified old path is the index
needed to make the two additive pages reachable.
