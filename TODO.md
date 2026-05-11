# TODO - Semantix

## Pruebas Realizadas

### 1. Prueba de ingest (URL web) - COMPLETA
- **Fecha**: 2025-05-11
- **Input**: https://www.upwork.com/resources/web-development-projects-kick-off-freelance-career
- **Vault**: D:\SynologyDrive\SynologyDrive\ObsidianVault\synology\Semantix
- **Resultado**: ✅ Nota creada exitosamente
- **Mejora implementada**: Resumen con LLM (Groq) - contenido ahora legible

## Tareas Completadas

### ✅ 1. Agregar dependencia pdfplumber
- **Archivo**: pyproject.toml
- **Cambio**: Agregado `"pdfplumber>=0.10.0"` a dependencies

### ✅ 2. Agregar Groq como provider
- **Archivo**: src/semantix/models.py
- **Cambios**:
  - Nuevo `GroqProvider` con integracion real a API de Groq
  - Modelo: `llama-3.3-70b-versatile`
  - Actualizado `get_provider()` para incluir Groq

### ✅ 3. Integrar LLM en pipeline de ingest
- **Archivos modificados**:
  - `src/semantix/ingest.py`: Agregado metodo `summarize()`
  - `src/semantix/cli.py`: Nueva opcion `--summarize/--no-summarize` (default: True)
- **Comando de prueba**:
  ```bash
  semantix ingest -i <url> -v <vault> -m groq
  ```

## Pendientes
- Ninguno