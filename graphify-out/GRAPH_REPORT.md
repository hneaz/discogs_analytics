# Graph Report - discogs_analytics  (2026-09-01)

## Corpus Check
- 2 files · ~381,098 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 104 nodes · 102 edges · 4 communities (3 shown, 1 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1b29a89c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- /graphify
- What You Must Do When Invoked
- My Discogs Collection - Analytics
- notes.md

## God Nodes (most connected - your core abstractions)
1. `/graphify` - 74 edges
2. `What You Must Do When Invoked` - 12 edges
3. `My Discogs Collection - Analytics` - 9 edges
4. `Installation <a name="installation"></a>` - 4 edges
5. `Step 3 - Extract entities and relationships` - 4 edges
6. `Session: /graphify — .` - 2 edges
7. `Table of Contents` - 1 edges
8. `Project Motivation<a name="motivation"></a>` - 1 edges
9. `Virtual environment` - 1 edges
10. `Python packages:` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities (4 total, 1 thin omitted)

### Community 0 - "/graphify"
Cohesion: 0.03
Nodes (73): Assistant - 2026-08-31T18:04:08Z, Assistant - 2026-08-31T18:04:18Z, Assistant - 2026-08-31T18:04:47Z, Assistant - 2026-08-31T18:05:16Z, Assistant - 2026-08-31T18:05:53Z, Assistant - 2026-08-31T18:06:03Z, Assistant - 2026-08-31T18:06:16Z, Assistant - 2026-08-31T18:06:38Z (+65 more)

### Community 1 - "What You Must Do When Invoked"
Cohesion: 0.13
Nodes (15): Part A - Structural extraction for code files, Part B - Semantic extraction (parallel subagents), Part C - Merge AST + semantic into final extraction, Step 0 - GitHub repos and multi-path merge (only if a URL or several paths), Step 1 - Ensure graphify is installed, Step 2.5 - Video and audio (only if video files detected), Step 2 - Detect files, Step 3 - Extract entities and relationships (+7 more)

### Community 2 - "My Discogs Collection - Analytics"
Cohesion: 0.15
Nodes (12): Authors, File Descriptions <a name="files"></a>, Installation <a name="installation"></a>, Jupyter notebook (if needed):, Licensing, Authors, Acknowledgements<a name="licensing"></a>, My Discogs Collection - Analytics, Project Motivation<a name="motivation"></a>, Python packages: (+4 more)

## Knowledge Gaps
- **96 isolated node(s):** `Table of Contents`, `Project Motivation<a name="motivation"></a>`, `Virtual environment`, `Python packages:`, `Jupyter notebook (if needed):` (+91 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `/graphify` connect `/graphify` to `What You Must Do When Invoked`, `notes.md`?**
  _High betweenness centrality (0.742) - this node is a cross-community bridge._
- **Why does `What You Must Do When Invoked` connect `What You Must Do When Invoked` to `/graphify`?**
  _High betweenness centrality (0.219) - this node is a cross-community bridge._
- **What connects `Table of Contents`, `Project Motivation<a name="motivation"></a>`, `Virtual environment` to the rest of the system?**
  _96 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `/graphify` be split into smaller, more focused modules?**
  _Cohesion score 0.0273972602739726 - nodes in this community are weakly interconnected._
- **Should `What You Must Do When Invoked` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._