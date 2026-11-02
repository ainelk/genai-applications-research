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

Download `vocabulary_graph.html` and open it in a browser. GitHub displays its source rather than running it. Use the term selector to inspect connections and evidence; the complete counts table is always visible.

## Reproduce the graph

From the repository root, with Python 3.9 or newer:

```sh
python3 scripts/build_graph.py
```

The generator overwrites `graph_data.json` and `vocabulary_graph.html` with data from the current report. There are no package installations, API keys, network requests, or paid services.

Explicit frequency counts case-insensitive whole-word occurrences of documented aliases, resolving overlaps in favor of the longest term. Implicit frequency counts sentences containing analyst-selected descriptive phrases but no explicit alias for that term. The two measures intentionally use different units. Implicit counts are conservative, auditable estimates, not an exhaustive automated semantic analysis. Analysis paragraphs in the eight use cases and cross-cutting section are included; introductory material, headings, product lists, and glossary text are excluded.

## Access and submission status

- EPAM assignment page: accessible in the signed-in browser on 2 November 2026; requirements checked against the live page.
- GitHub: authenticated account accessible; this dedicated public repository is the shareable project destination.
- Public research sources: consulted through search and primary-source pages; no paid product trials were performed.
- DIAL AI: signed-in chat interface accessible with a selectable model and message composer. No prompt was submitted and model execution/quotas were not tested.
- CodeMie: its link redirected to an authentication origin. Automatic approval review blocked that optional authentication check because explicit authorization to sign in there was not provided. No workaround was attempted; entitlement remains unverified.
- Other linked course services and GitHub Copilot entitlement: not tested. They are not needed to read or reproduce these deliverables. Their access must not be inferred from access to DIAL or the course page.
- GitHub integration write access: the connected integration returned HTTP 403 for this new repository, although the signed-in browser can manage it. Repository publication uses the browser instead.
- Access findings are recorded here rather than reported as an all-resources pass. The course's remaining service entitlements should be checked before they are needed.
- The submission text file must contain the learner's actual `@epam.com` email and this repository URL. It must be named `Intro_<first_name>_<last_name>.txt` and uploaded to the university platform. Personal contact information is not stored in this public repository.
- University upload/submission is not marked complete by this repository. The platform states that only one upload attempt is available.

## AI assistance and learner review

AI assisted the research synthesis, initial vocabulary, phrase annotation, and graph implementation. Product links support the listed features; proposed benefits and architectures are analysis, not benchmark results. The learner should review the report and personalize the vocabulary before claiming manual work. No completion of manual review, Copilot integration, CodeMie configuration, or specific score is claimed.

Only project-related files belong in this repository. The submission text file is kept separate because it contains the learner's email.
