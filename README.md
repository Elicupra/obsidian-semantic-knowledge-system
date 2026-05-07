# Semantix

CLI para ingestión de conocimiento semántico en Obsidian.

## Instalación

```bash
pip install -e .
```

## Uso

```bash
# Procesar un archivo
semantix ingest -i documento.pdf -v /path/to/vault

# Procesar una URL
semantix ingest -i https://ejemplo.com -v /path/to/vault

# Procesar video de YouTube
semantix ingest -i https://youtube.com/watch?v=xxx -v /path/to/vault

# Detectar duplicados
semantix deduplicate -v /path/to/vault

# Reporte de backlinks
semantix backlinks -v /path/to/vault
```

## Configuración

Crea un archivo `.env` con las siguientes variables:

```
GEMINI_API_KEY=tu_api_key
CLAUDE_API_KEY=tu_api_key
```

## Categorías

Usa `-c` para especificar categoría:
```bash
semantix ingest -i archivo.md -v /path/to/vault -c AI
```
