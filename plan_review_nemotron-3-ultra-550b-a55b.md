# Plan Review: `plan.md` vs. Source Analysis (`src/discogs_analysis.py`)

## Summary
The plan captures the **general structure** and **intent** well, but has **significant implementation flaws** that would prevent a working Dash app. It covers ~9 of the ~13 analytical areas from the source (some consolidated), but the callback architecture is fundamentally broken.

---

## What the Plan Gets Right

| Area | Status |
|------|--------|
| Goal clarity | ✅ Clear, measurable objective |
| Section identification | ✅ 9 tabs map to major analysis areas in source |
| Test cases | ✅ Specific values match source (Meshuggah boxset, $0.50 Wyclef Jean) |
| Risk awareness | ✅ Good identification of performance, path, and conversion issues |
| Code style guidance | ✅ PEP 8, type hints, docstrings, error handling |

---

## Critical Issues (Will Break Implementation)

### 1. **Duplicate `display_content` callbacks** (Tasks 4–12)
Every task defines:
```python
@callback(Output('page-content', 'children'), [Input('tabs', 'value')])
def display_content(tab): ...
```
**Dash forbids multiple callbacks with the same Output.** Only the last one registered will work. You need **one** callback that dispatches based on `tab` value, or use `dash.page_container` / multi-page pattern.

### 2. **Data loads on button click, not startup** (Task 4, line 126)
```python
@callback(Output('data-store', 'data'), [Input('btn-filter', 'n_clicks')])
def load_data(n_clicks):
    if n_clicks is not None and n_clicks > 0: ...
```
- Data won't load until user clicks "Apply Filters"
- Every filter click re-reads CSV (no caching)
- `dcc.Store` has size limits (~2MB default); 408 rows × ~20 cols may exceed it

### 3. **Filter architecture is inverted**
Filters (`filter-artist`, `filter-genre`, etc.) are defined but **never connected as Inputs** to plot callbacks. Instead, callbacks depend on `btn-filter` and `data-store`. The typical Dash pattern:
```python
@callback(Output('graph', 'figure'),
          [Input('filter-artist', 'value'), Input('filter-genre', 'value'), ...])
def update_graph(artist, genre, ...):
    df = load_data()  # cached
    df = apply_filters(df, artist, genre, ...)
    return make_figure(df)
```

### 4. **Data store passes dict, not DataFrame**
Task 4 returns a `profile_summary` dict (aggregates), but Tasks 5–12 treat `data` as a DataFrame:
```python
df = data  # data is a dict, not a DataFrame!
top10 = df.nlargest(10, '_Max_')  # AttributeError: 'dict' has no attribute 'nlargest'
```

### 5. **Missing analytical depth from source**
| Source Section | Plan Coverage | Missing |
|----------------|---------------|---------|
| Label analysis (Label1/Label2/Label3/Label4) | Basic count/spending | Multi-label handling, Label sorting issue (Svart vs 20 Buck Spin) |
| Time series | Yearly bars only | `Date_Added` monthly plots, `Released` vs `Date_Added` correlation |
| Genre analysis | 4 boxplots only | Pairplots, distribution plots (distplot), regression plots, genre reduction (>2 count filter) |
| Subgenre analysis | 3D scatter + cumulative bar | Pairplots, 4× distplots, heatmaps (year×subgenre), animated bar charts |
| Format analysis | Histogram + boxplot | Top 20 by median per format, pairplots, 4× distplots |
| Autographed analysis | Histogram + boxplot | Faceted scatter by subgenre+format (lines 1076–1091) |

### 6. **Column name mismatches**
Plan uses `Artist2`, `Format`, `Label`, `Collection_Autographed`, `_Min_`, `_Median_`, `_Max_` — verify these match `discogs_clean_data.csv` exactly. Source creates `Artist2` at line 144, splits `Label` into `Label1`–`Label4` at line 64, renames `Collection Autographed` → `Collection_Autographed` at line 131.

### 7. **Export callback is non-functional** (Task 13)
```python
@callback(Output('btn-export', 'n_clicks'), [Input('btn-download', 'n_clicks')])
def handle_download(btn_clicks): pass
```
- Outputting to `n_clicks` (read-only property) is invalid
- No actual download implementation (needs `dcc.Download` + `send_data_frame`)

---

## Medium Issues

| Issue | Impact |
|-------|--------|
| No `dash_bootstrap_components` for responsive layout | Sidebar + tabs won't work well on mobile |
| No caching implementation (`diskcache` or `flask_caching` referenced but not used) | CSV re-read on every callback |
| `Date_Added` parsing assumes format; source uses `pd.to_datetime(...).dt.strftime('%m/%Y')` | May fail if format differs |
| Subgenre 3D scatter filters `Collection_Cost < 200` inline — should be a configurable filter | Hardcoded threshold |
| Cumulative subgenre bar uses `groupby().cumsum()` on already-aggregated data — logic differs from source (lines 1283–1290) | May produce different results |

---

## Recommended Fixes (Priority Order)

1. **Restructure callbacks**: Single `display_content` + separate plot callbacks with filter Inputs
2. **Load data at startup** (module level or `dcc.Store` with `storage_type='memory'` + background callback)
3. **Pass filtered DataFrame via `dcc.Store`** (or compute aggregates server-side, pass JSON)
4. **Add `dash_bootstrap_components`** for sidebar + responsive grid
5. **Implement `dcc.Download`** for CSV export
6. **Map every source visualization** to a plan task — don't drop pairplots, heatmaps, animations
7. **Validate column names** against actual CSV before coding

---

## Verdict
**Plan is a good design sketch but not implementation-ready.** A developer following it literally would hit the duplicate-callback and data-flow errors immediately. Fix the callback architecture and data pipeline first, then expand task detail to match the source's analytical depth.