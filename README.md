# Semantix

CLI para ingestion de conocimiento semantico en Obsidian.

## Instalacion

```bash
pip install -e .
```

## Configuracion

### Configurar API Key

```bash
# Configuracion interactiva (recomendado)
semantix config set

# Configurar con clave directa
semantix config set -p groq -k TU_API_KEY
```

### Proveedores disponibles

| Proveedor | Descripcion | Modelo por defecto |
|-----------|-------------|-------------------|
| groq | GPU accelerators for AI inference (free tier) | llama-3.3-70b-versatile |
| openrouter | Unified API for 200+ LLMs | anthropic/claude-3.5-sonnet |
| openai | GPT-4, GPT-4o models | gpt-4o |
| google | Google Gemini models | gemini-1.5-pro |
| claud e | Anthropic Claude | claude-3-5-sonnet-20241022 |
| local | Local models via Ollama | llama3 |

### Comandos de configuracion

```bash
# Ver configuracion actual
semantix config show

# Establecer proveedor por defecto
semantix config default -p groq

# Eliminar configuracion de un proveedor
semantix config remove -p groq
```

Las API keys se almacenan de forma segura en el gestor de credenciales del sistema operativo (Windows Credential Manager / macOS Keychain / Linux Secret Service).

## Uso

```bash
# Procesar un archivo
semantix ingest -i documento.pdf -v /path/to/vault

# Procesar una URL
semantix ingest -i https://ejemplo.com -v /path/to/vault

# Procesar video de YouTube
semantix ingest -i https://youtube.com/watch?v=xxx -v /path/to/vault

# Especificar modelo
semantix ingest -i archivo.md -v /path/to/vault -m groq

# Especificar categoria
semantix ingest -i archivo.md -v /path/to/vault -c AI

# Sin resumen LLM
semantix ingest -i archivo.md -v /path/to/vault --no-summarize

# Detectar duplicados
semantix deduplicate -v /path/to/vault

# Reporte de backlinks
semantix backlinks -v /path/to/vault
```

## Opciones

- `-i, --input`: Archivo, URL o path a procesar
- `-v, --vault`: Ruta al vault de Obsidian
- `-m, --model`: Modelo a usar (groq, openrouter, openai, google, claude, local)
- `-c, --category`: Categoria/carpeta destino
- `--summarize/--no-summarize`: Usar LLM para resumir contenido (default: True)
- `--metadata/--no-metadata`: Incluir metadata YAML (default: True)
- `-vv, --verbose`: Modo verbose