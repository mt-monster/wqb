# Brain Labs Data-Analysis Agent

> Spec for the pre-simulation raw-data-analysis agent invoked by the
> `alpha-template-labs-data-analysis` skill. The agent answers one question: **does a
> dataset have a Python-native edge before Stage 2 candidate design?**

## 1. Purpose
Inspect USA/TOP3000/D1 MATRIX datasets in Brain Labs to diagnose
coverage / missingness / frequency / outliers / correlation, then convert findings into
Python-native extractor mechanisms. This is a research step that precedes simulation.

## 2. Inputs
- `dataset_id` (e.g. `imbalance5`)
- `region`, `universe`, `delay` (default USA / TOP3000 / 1)
- `fields`: at most **two MATRIX fields** (VECTOR/GROUP fields are excluded from
  downstream Python design)

## 3. Workflow
1. Pull MATRIX fields via MCP `get_datafields` (no Labs login needed for field list).
2. Only if a new Labs session is required (and quota approved): `authenticate_brainlabs()`
   → open `workspaces_url`.
3. `emit_labs_script(...)` → pasteable Labs script (writes `/tmp/labs_data_analysis_<dataset_id>_raw.json`).
4. In Brain Labs, run the script; inspect:
   - **coverage** (non-NaN ratio)
   - **missingness** (pattern, not just count)
   - **real zeros** vs **sentinel values**
   - **update frequency**
   - **outliers** / **distribution** shape
   - **turnover proxy**
   - **field correlation** (with candidate peer / price fields)
5. `ingest_labs_result(...)` the returned Labs JSON.
6. Classify each field's data shape and downstream Python suitability
   (e.g. point_mass → `rank`+`trade_when`; zero_inflated → event gate; spread → `zscore`).
7. Write `tracking/runs/<ts>_labs_data_analysis_<dataset_id>.json`.
8. Return accepted / rejected mechanisms and the Python-alpha implications.

## 4. Hard rules
- **Do not call `submit_alpha`.**
- **Do not simulate** during this agent unless the user explicitly asks to continue into Stage 3.
- **Do not use VECTOR/GROUP fields** for downstream Python alpha design.
- **Do not copy forum formulas** — use forum material only for diagnostics, field
  direction, failure modes, and preprocessing clues.
- The final recommendation must be **one mechanism using at most two MATRIX fields**.
- Cross-validate Labs conclusions against the WebDataScope offline package
  (`tools/webdata_quality.py --fields <ds>`): consistent coverage/distribution ⇒ high
  confidence; disagreement ⇒ trust Labs live data (the package is a 2012–2021 snapshot).

## 5. Output contract
`tracking/runs/<ts>_labs_data_analysis_<dataset_id>.json`:
```json
{
  "dataset_id": "imbalance5",
  "fields": [
    {"name": "imb5_score", "shape": "spread", "coverage": 0.91,
     "recommended": "rank(ts_zscore(ts_backfill(imb5_score, 66), 189))"}
  ],
  "mechanism": "single MATRIX field, regime-change extraction",
  "python_alpha_implication": "PPA candidate via rank/zscore + returns reversal"
}
```
