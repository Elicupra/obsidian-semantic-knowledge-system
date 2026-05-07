# Semantix

Python CLI tool para ingestión de conocimiento en Obsidian.

## Project Structure

```
src/semantix/
+-- cli.py       # Click CLI (comandos: ingest, deduplicate, backlinks)
+-- ingest.py    # Procesamiento de archivos, URLs, YouTube
+-- generate.py  # Generación de notas Obsidian
+-- models.py    # Providers de IA (Gemini, Claude, Local)
+-- dedupe.py    # Detección de duplicados
+-- backlinks.py # Análisis de backlinks
```

## Commands

```bash
pip install -e .  # Instalar

semantix ingest -i <input> -v <vault>      # Procesar archivo/URL
semantix deduplicate -v <vault>             # Encontrar duplicados
semantix backlinks -v <vault>               # Reporte de backlinks
```

## Config

`.env`:
- `GEMINI_API_KEY`
- `CLAUDE_API_KEY`

## Tech Stack

- Click (CLI)
- yt-dlp (YouTube)
- beautifulsoup4 (HTML)
- pdfplumber (PDF)
- PyYAML (metadata)
