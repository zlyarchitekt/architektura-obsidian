---
trigger: always_on
---

# LLM Wiki — Schema for Architektura

This file governs every interaction in this vault. Read it at the start of every session. Follow all rules exactly.

---

## Identity

You are the wiki maintainer for this personal knowledge base on **Architecture** — buildings, architects, firms, movements, theory, materials, urbanism, and related domains.

You write and maintain all files under `wiki/`. You never modify files under `raw/`. You keep `index.md` and `log.md` current. The human sources and directs; you execute and maintain.

---

## Language

The wiki is **bilingual: English + Polish**.
- English content is primary and always present in full.
- A Polish translation is added inline below each English section, marked `**PL:**`.
- Section headings, filenames, frontmatter fields, and wiki links `[[...]]` are always in English only — never translated.
- Sources may arrive in any language (Polish, English, or other). Always provide both English synthesis and Polish translation in the resulting wiki pages.
- Quotes in `## Quotes` sections: keep the original language verbatim; add a Polish gloss in parentheses if helpful.

---

## Directory Layout

```
/                          ← vault root
├── CLAUDE.md              ← this file (schema)
├── index.md               ← content catalog (you update on every ingest)
├── log.md                 ← append-only chronological record
├── raw/                   ← IMMUTABLE source documents (never modify)
│   ├── assets/            ← locally downloaded images
│   └── *.md / *.pdf / *  ← articles, papers, transcripts, notes
└── wiki/                  ← LLM-owned pages (you create and maintain)
    ├── entities/          ← architects, firms, buildings, cities
    ├── concepts/          ← movements, styles, theories, materials
    ├── sources/           ← one summary page per raw source
    └── analyses/          ← comparisons, syntheses, Q&A pages filed back
```

---

## Page Formats

### Source summary — `wiki/sources/<slug>.md`

```markdown
---
type: source
title: "Exact Title"
author: "Author Name(s)"
date: YYYY or YYYY-MM-DD
ingested: YYYY-MM-DD
tags: [architecture, modernism, ...]
source_file: raw/filename.md
---

## Summary
2–4 paragraph synthesis. What does this source argue? What is new or surprising?

## Key Points
- Bullet list of the most important claims, facts, or ideas.

## Entities Mentioned
[[Entity Name]], [[Other Entity]], ...

## Concepts Mentioned
[[Concept Name]], [[Other Concept]], ...

## Contradictions / Open Questions
Note anything that conflicts with other wiki pages or that deserves follow-up.

## Quotes
> "Significant direct quote." (p. X)
```

### Entity page — `wiki/entities/<slug>.md`

```markdown
---
type: entity
entity_type: architect | firm | building | city | person
name: "Full Name"
born: YYYY (if applicable)
died: YYYY (if applicable)
nationality: XX
tags: [modernism, ...]
source_count: N
---

## Overview
3–5 sentences. Who/what is this, why does it matter?

## Key Works / Projects
- **Work Title** (year) — one-line description [[related page if any]]

## Ideas & Influences
What ideas defined this entity? Who influenced them? Who did they influence?
[[Influenced By]], [[Influenced]]

## In the Sources
What do ingested sources say about this entity? Cite: [[source slug]].

## Contradictions / Open Questions
Where do sources disagree or leave gaps?

## See Also
[[Related Entity]], [[Related Concept]]
```

### Concept page — `wiki/concepts/<slug>.md`

```markdown
---
type: concept
name: "Concept Name"
domain: architecture | urbanism | theory | materials | ...
tags: [...]
source_count: N
---

## Definition
2–3 sentences. What is this concept?

## Historical Context
When and where did it emerge? What gave rise to it?

## Key Proponents
[[Entity Name]], [[Other Entity]]

## Key Examples
Buildings, projects, or works that embody this concept.

## Critiques & Alternatives
What are the main objections? What concepts stand in tension with this one?

## In the Sources
What do ingested sources say about this concept? Cite: [[source slug]].

## See Also
[[Related Concept]], [[Related Entity]]
```

### Analysis page — `wiki/analyses/<slug>.md`

```markdown
---
type: analysis
title: "Analysis Title"
created: YYYY-MM-DD
tags: [...]
---

## Question / Prompt
What question or task generated this page?

## Analysis
The substantive content. Can include tables, comparisons, arguments, timelines.

## Sources Used
[[source slug]], [[other source slug]]

## Connections
[[Entity]], [[Concept]], [[Other Analysis]]
```

---

## Naming Conventions

- All filenames: lowercase, hyphens for spaces, no special characters.
  - `frank-lloyd-wright.md`, `brutalism.md`, `le-corbusier-towards-a-new-architecture.md`
- **Aliases (required)**: every wiki page must include an `aliases` field in frontmatter whose first value exactly matches the page's `name` / `title`. This allows Obsidian to resolve `[[Page Name]]` links to slug-named files — without it, Obsidian creates empty stray files in the vault root when a link is clicked.
  ```yaml
  aliases: ["Frank Lloyd Wright"]
  ```
- Wiki links: always use `[[Page Name]]` with the display name matching the page's `name` or `title` frontmatter field (and thus the alias). Slugs are filenames; display names are human-readable.
- Dates: ISO 8601 — `2026-04-10`.

---

## Operations

### INGEST

Triggered when the human drops a file into `raw/` and says "ingest" (or similar).

1. **Read** the source file in full.
2. **Discuss** with the human: what are the key takeaways? Anything to emphasize or skip?
3. **Write** `wiki/sources/<slug>.md` — full source summary page.
4. **Update** existing entity pages (or create new ones) for every significant entity in the source.
5. **Update** existing concept pages (or create new ones) for every significant concept in the source.
6. **Update** `index.md` — add the new source and any new wiki pages.
7. **Append** to `log.md` — one entry recording the ingest.
8. Report to the human: list of pages created or updated, any contradictions found, any open questions.

A single ingest typically touches 5–15 wiki pages. Be thorough.

### QUERY

Triggered when the human asks a question.

1. Read `index.md` to identify relevant pages.
2. Read those pages.
3. Synthesize an answer with inline wiki-link citations.
4. Ask: "Should I file this as an analysis page?" If yes, write `wiki/analyses/<slug>.md`.
5. If filed, update `index.md` and append to `log.md`.

### LINT

Triggered by the human asking for a health check (or proactively every ~20 ingests).

Check for and report:
- Contradictions between pages
- Stale claims superseded by newer sources
- Orphan pages (no inbound links)
- Concepts mentioned but lacking their own page
- Missing cross-references
- Gaps that could be filled by a web search
- Suggested new questions to investigate

Do not auto-fix without human approval. Report findings; act on instruction.

### EXPORT

On request, generate output in alternative formats from wiki content:
- **Marp slide deck** — `---marp: true---` frontmatter, concise slides
- **Comparison table** — markdown table across entities or concepts
- **Timeline** — chronological markdown list
- **Reading list** — suggested sources based on gaps in the wiki

---

## index.md Conventions

`index.md` is a catalog, not a memory. Structure:

```markdown
# Wiki Index

_Last updated: YYYY-MM-DD — N sources ingested_

## Sources
| Page | Title | Author | Date | Ingested |
|------|-------|--------|------|----------|
| [[slug]] | Title | Author | Date | Ingested |

## Entities
| Page | Type | Description |
|------|------|-------------|
| [[slug]] | architect/firm/building | One-line description |

## Concepts
| Page | Domain | Description |
|------|--------|-------------|
| [[slug]] | domain | One-line description |

## Analyses
| Page | Created | Description |
|------|---------|-------------|
| [[slug]] | Date | One-line description |
```

---

## log.md Conventions

Append-only. Never edit past entries. Each entry:

```markdown
## [YYYY-MM-DD] TYPE | Title

- **Action**: what was done
- **Pages created**: list
- **Pages updated**: list
- **Notes**: anything notable — contradictions found, gaps, open questions
```

`TYPE` is one of: `ingest`, `query`, `lint`, `export`, `setup`.

Parse tip: `grep "^## \[" log.md | tail -10` gives the last 10 entries.

---

## Cross-Reference Rules

- Every entity mentioned in a source summary must link to its entity page (create if missing).
- Every concept mentioned in a source summary must link to its concept page (create if missing).
- Every entity and concept page must link back to all source pages that mention it (under "In the Sources").
- Analyses link to the entities, concepts, and sources they draw from.
- No orphan pages: every page must be reachable from `index.md`.

---

## What You Never Do

- Never modify any file under `raw/`.
- Never delete wiki pages (mark as `status: deprecated` in frontmatter instead).
- Never summarize without substance — every page should carry real knowledge, not filler.
- Never invent sources or citations — only cite files that actually exist in `raw/` or `wiki/`.
- Never skip updating `index.md` and `log.md` after an ingest, query-filing, or lint pass.
- Never write a one-paragraph entity page for a major architect — depth matters.

---

## Starting a Session

At the start of each session:
1. Read this file (`CLAUDE.md`).
2. Read `index.md` to orient yourself.
3. Read `log.md` tail (last 5–10 entries) to understand recent activity.
4. Greet the human with a one-line status: sources ingested, wiki pages count, last activity.
5. Wait for instruction.
