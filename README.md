# Generative AI Applications Research

EPAM Tech Orda — Generative AI for Software Development, Course Introduction.

## Deliverables

| File | Purpose |
| --- | --- |
| [research_report.md](research_report.md) | Eight use cases, each with two analysis paragraphs covering business value, technical challenges, and weaknesses, plus two linked implementations. |
| [vocabulary.md](vocabulary.md) | Twenty plain-language terms selected from the report, with examples. |
| [vocabulary_graph.html](vocabulary_graph.html) | Offline interactive graph connecting terms to report sections, with explicit and implicit counts displayed separately. |
| [graph_data.json](graph_data.json) | Counts, alias rules, implicit phrase annotations, report hash, and sentence-level evidence. |
| [scripts/build_graph.py](scripts/build_graph.py) | Reproducible graph generator using Python's standard library. |

## Reproduce the graph

From the repository root, with Python 3.9 or newer:

```sh
python3 scripts/build_graph.py
```

The generator overwrites `graph_data.json` and `vocabulary_graph.html` with data from the current report. There are no package installations, API keys, network requests, or paid services.

Explicit frequency counts case-insensitive whole-word occurrences of documented aliases, resolving overlaps in favor of the longest term. Implicit frequency counts sentences containing analyst-selected descriptive phrases but no explicit alias for that term. The two measures intentionally use different units. Implicit counts are conservative, auditable estimates, not an exhaustive automated semantic analysis. Analysis paragraphs in the eight use cases and cross-cutting section are included; introductory material, headings, product lists, and glossary text are excluded.

