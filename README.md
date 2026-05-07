# Obsidian Semantic Knowledge System

A semantic knowledge ingestion and Obsidian note generation agent system.

## Overview

This system transforms unstructured information into reusable knowledge, generating high-quality Obsidian-ready markdown notes while maintaining semantic consistency across your vault.

## Core Features

- **Semantic Knowledge Ingestion**: Process various input types (URLs, PDFs, text, markdown, etc.)
- **Obsidian Note Generation**: Create notes with full Obsidian feature support (frontmatter, backlinks, tags, wikilinks)
- **Quality Filtering**: Evaluate sources for authority, coherence, depth, and bias
- **Duplicate Detection**: SHA256 exact matching + semantic similarity using embeddings
- **Cost Optimization**: Uses Gemini Flash by default, escalating to premium models only when needed

## Key Principles

1. **Knowledge over summarization** - Focus on reusable, actionable information
2. **Semantic consistency** - Reuse existing tags and terminology
3. **Quality filtering** - Evaluate and flag low-quality content
4. **Cost efficiency** - Prefer local processing and low-cost models

## Processing Pipeline

1. **Ingestion** - Validate file type, encoding, generate processing ID
2. **Extraction** - Extract plain text, hierarchy, sections, metadata
3. **Normalization** - Clean artifacts, normalize formatting
4. **Semantic Analysis** - Detect topics, entities, relationships, tags
5. **Vault Cross-Reference** - Search similarity, identify related notes
6. **Quality Evaluation** - Generate quality scores
7. **Review Mode Decision** - Automatic, Manual, Hybrid, or Custom

## Technology Stack

- **Default Model**: Gemini 2.5 Flash
- **Fallback Model**: Claude Sonnet
- **Embedding Model**: bge-m3
- **Output Language**: Spanish (by default)

## Usage

This system is designed to be integrated with AI agents that process information and generate Obsidian-compatible markdown notes.

## License

MIT

## Author

Created for semantic knowledge management with Obsidian