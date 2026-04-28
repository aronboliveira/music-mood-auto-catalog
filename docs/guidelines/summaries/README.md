# Summaries & Guidance Book

A multi-chapter reference covering the design, curation, and operational knowledge behind this music classification pipeline. Written as both a human-readable guide and a machine-consumable knowledge base.

## Chapters

| #   | File                                                                     | Topic                                                                                    |
| --- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| 1   | [01-introduction.md](01-introduction.md)                                 | Project scope, goals, and architectural overview                                         |
| 2   | [02-taxonomy-and-mood-clusters.md](02-taxonomy-and-mood-clusters.md)     | The 65-mood vocabulary, 15 semantic clusters, 6D vectors, and 12 RPG contextual clusters |
| 3   | [03-artist-emotional-profiles.md](03-artist-emotional-profiles.md)       | What each game-OST artist tends to express emotionally                                   |
| 4   | [04-curation-workflow.md](04-curation-workflow.md)                       | End-to-end workflow from raw download to classified placement                            |
| 5   | [05-data-analysis-patterns.md](05-data-analysis-patterns.md)             | Useful data queries, analysis techniques, and what failed                                |
| 6   | [06-logic-successes-and-failures.md](06-logic-successes-and-failures.md) | Algorithms that worked, algorithms that didn't, and why                                  |
| 7   | [07-tips-and-best-practices.md](07-tips-and-best-practices.md)           | Operational hints for maintaining and extending the library                              |
| 8   | [08-cli-reference.md](08-cli-reference.md)                               | Shell commands for filesystem queries, search, and bulk operations                       |

## Machine-Readable Specifications

| File                                                   | Format | Purpose                                                             |
| ------------------------------------------------------ | ------ | ------------------------------------------------------------------- |
| [specs/rpg-clusters.yml](specs/rpg-clusters.yml)       | YAML   | Complete RPG cluster definitions for bot consumption                |
| [specs/mood-vocabulary.yml](specs/mood-vocabulary.yml) | YAML   | Canonical mood list with cluster memberships and vector coordinates |
| [specs/scoring-rules.yml](specs/scoring-rules.yml)     | YAML   | Scoring thresholds, custom scorer logic, anti-gates                 |

## Audience

- **Chapters 1-8**: Written for human readers (the project maintainer, future collaborators, or LLM assistants resuming work). Narrative README-style prose.
- **specs/**: Structured data files targeted at deterministic bots and LLMs that need precise, parseable definitions without ambiguity.

## When to Update

Update these summaries when:

- New RPG contextual folders are added or cluster definitions change
- The mood vocabulary is expanded or labels are retired
- New artist folders enter the RPG-eligible pool
- Significant workflow changes are introduced
