# Database Naming Conventions

This document outlines the standardized naming conventions for Directus collections, based on the original schema from `lateral.db`. The standard convention is to use **snake_case** and **plural nouns**.

| Original Name | Standardized Name | Notes |
| :--- | :--- | :--- |
| `articles` | `articles` | Unchanged |
| `authors` | `authors` | Unchanged |
| `Concepts` | `concepts` | Lowercase |
| `embedding_strategies` | `embedding_strategies` | Unchanged |
| `references` | `references` | Unchanged |
| `text_blocks` | `text_blocks` | Unchanged |
| `patterns` | `patterns` | Unchanged |
| `document_sections` | `document_sections` | Unchanged |
| `article_authors` | `article_authors` | Unchanged (Junction Table) |
| `article_references` | `article_references` | Unchanged (Junction Table) |
| `biographies` | `biographies` | Unchanged |
| `DiscourseSegments` | `discourse_segments` | Snake Case |
| `ConceptAnalyses` | `concept_analyses` | Snake Case |
| `Senses` | `senses` | Lowercase |
| `processing_log` | `processing_logs` | Pluralized |
| `sentences` | `sentences` | Unchanged |
| `llm_run_logs` | `llm_run_logs` | Unchanged |
| `images` | `images` | Unchanged |
| `tables` | `tables` | Unchanged |
| `pattern_versions` | `pattern_versions` | Unchanged |
| `text_spans` | `text_spans` | Unchanged |
| `ArticleConceptSenses` | `article_concept_senses` | Snake Case (Junction Table) |
| `sense_embeddings` | `sense_embeddings` | Unchanged |
| `sense_clustering_runs` | `sense_clustering_runs` | Unchanged |
| `matched_tags` | `matched_tags` | Unchanged |
| `pattern_processing_errors` | `pattern_processing_errors` | Unchanged |
| `Evidence` | `evidence_items` | Renamed for clarity |
| `sense_cluster_assignments` | `sense_cluster_assignments` | Unchanged |
| `generated_insights` | `generated_insights` | Unchanged |