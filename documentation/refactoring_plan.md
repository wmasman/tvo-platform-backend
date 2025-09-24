# Schema Refactoring Plan

This document outlines the plan to refactor the Directus schema to include proper relational links between collections, while preserving the existing primary keys from the `lateral.db` database.

## Todo List

- [ ] Refactor `article_authors` to a Many-to-Many relationship
- [ ] Refactor `text_blocks` to have a Many-to-One relationship with `articles`
- [ ] Refactor `document_sections` to have a Many-to-One relationship with `articles`
- [ ] Refactor `article_references` to a Many-to-Many relationship
- [ ] Refactor `biographies` to have a Many-to-One relationship with `articles`
- [ ] Refactor `discourse_segments` to have a Many-to-One relationship with `articles`
- [ ] Refactor `concept_analyses` to have a Many-to-One relationship with `articles`
- [ ] Refactor `senses` to have a Many-to-One relationship with `concepts`
- [ ] Refactor `article_concept_senses` to a Many-to-Many relationship
- [ ] Refactor `sense_embeddings` to have a Many-to-One relationship with `concept_analyses`
- [ ] Refactor `sense_clustering_runs` to have a Many-to-One relationship with `concept_analyses`
- [ ] Refactor `matched_tags` to have Many-to-One relationships with `articles` and `pattern_versions`
- [ ] Refactor `pattern_processing_errors` to have Many-to-One relationships with `articles` and `pattern_versions`
- [ ] Refactor `evidence_items` to have a Many-to-One relationship with `article_concept_senses`
- [ ] Refactor `sense_cluster_assignments` to have a Many-to-One relationship with `sense_clustering_runs`
- [ ] Refactor `generated_insights` to have a Many-to-One relationship with `sense_clustering_runs`
- [ ] Refactor `images` to have a Many-to-One relationship with `articles`
- [ ] Refactor `tables` to have a Many-to-One relationship with `articles`
- [ ] Refactor `text_spans` to have a Many-to-One relationship with `text_blocks`

## Key Preservation Strategy

The existing primary keys from the `lateral.db` database will be preserved in the Directus schema. This will be achieved by setting the `id` field of each collection to be of the same type as the original primary key, and ensuring that the `special` flag is not set to `uuid` unless the original primary key was a UUID.

## Relationship Diagram

```mermaid
erDiagram
    articles ||--o{ text_blocks : contains
    articles ||--o{ document_sections : contains
    articles ||--o{ biographies : contains
    articles ||--o{ discourse_segments : contains
    articles ||--o{ concept_analyses : contains
    articles ||--o{ images : contains
    articles ||--o{ tables : contains
    articles }|o--o| authors : "article_authors"
    articles }|o--o| "references" : "article_references"
    concepts ||--o{ senses : contains
    articles }|o--o| senses : "article_concept_senses"
    concept_analyses ||--o{ sense_embeddings : contains
    concept_analyses ||--o{ sense_clustering_runs : contains
    articles ||--o{ matched_tags : contains
    pattern_versions ||--o{ matched_tags : contains
    articles ||--o{ pattern_processing_errors : contains
    pattern_versions ||--o{ pattern_processing_errors : contains
    article_concept_senses ||--o{ evidence_items : contains
    sense_clustering_runs ||--o{ sense_cluster_assignments : contains
    sense_clustering_runs ||--o{ generated_insights : contains
    text_blocks ||--o{ text_spans : contains