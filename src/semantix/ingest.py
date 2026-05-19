import hashlib
from pathlib import Path
from urllib.parse import urlparse
from typing import Optional


SYSTEM_PROMPT = """Eres un agente de ingesta de conocimiento para una bóveda Obsidian.

Tu objetivo NO es resumir. Tu objetivo es:
- Extraer conocimiento reutilizable y conceptos accionables
- Preservar la jerarquía semántica del contenido original
- Generar una nota Obsidian lista para usar como segundo cerebro

REGLAS ESTRICTAS:
- Nunca produzcas resúmenes superficiales ni lenguaje de marketing
- Preserva terminología técnica exacta del original
- Si el contenido es código, presérvalo íntegro en bloques de código
- Reescribe con tus palabras solo cuando mejore la claridad, no para condensar
- Mantén densidad conceptual alta
- Responde exclusivamente en español"""


USER_PROMPT = """Procesa esta fuente como agente de conocimiento Obsidian.

## Metadatos de entrada
- Título: {title}
- Tipo de fuente: {source_type}
- URL/Origen: {source_url}

## Contenido fuente
{content}

---

## Instrucciones de salida

Genera una nota Obsidian completa con esta estructura exacta:

### 1. Frontmatter YAML
Incluye: title, source, source_type, created (hoy), language, tags (máx 6), topics, entities, related (vacío por ahora)

### 2. Cuerpo de la nota

# [Título descriptivo]

## Idea Central
Una sola oración que capture la tesis o propósito del contenido.

## Conceptos Clave
Para cada concepto relevante:
**[Nombre del concepto]**: explicación precisa y reutilizable. Incluye ejemplos concretos si los hay en el original.

## Desarrollo
Secciones basadas en la estructura lógica del contenido original — no en su formato.
Usa subsecciones si el tema lo requiere. Preserva pasos, listas, código y datos numéricos exactos.

## Relaciones
- Conceptos relacionados que probablemente ya existan en la bóveda: [[...]]
- Tecnologías o personas mencionadas: [[...]]

## Acciones
- [ ] Tareas o next steps si el contenido los implica

## Observaciones Críticas
Limitaciones, sesgos detectados o información que requiere validación adicional.

## Referencias
Fuentes citadas en el contenido original."""


class Ingestor:
    def __init__(self, model_provider):
        self.model_provider = model_provider
    
    def process(self, input_path: str) -> dict:
        if self._is_url(input_path):
            return self._process_url(input_path)
        elif Path(input_path).exists():
            return self._process_file(input_path)
        else:
            raise ValueError(f"Input invalido: {input_path}")
    
    def summarize(self, content: str, title: str = "", source_type: str = "article", source_url: str = "") -> str:
        prompt = USER_PROMPT.format(
            title=title,
            source_type=source_type,
            source_url=source_url,
            content=content[:15000]
        )

        try:
            summary = self.model_provider.generate(SYSTEM_PROMPT, prompt)
            return summary
        except Exception as e:
            return f"# Error al procesar\n\n{str(e)}\n\n---Contenido original---\n\n{content[:2000]}..."
    
    def _is_url(self, input_str: str) -> bool:
        try:
            result = urlparse(input_str)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def _process_url(self, url: str) -> dict:
        parsed = urlparse(url)
        
        if "youtube.com" in parsed.netloc or "youtu.be" in parsed.netloc:
            return self._process_youtube(url)
        elif parsed.netloc:
            return self._process_web(url)
        
        raise ValueError(f"URL no soportada: {url}")
    
    def _process_web(self, url: str) -> dict:
        import requests
        from bs4 import BeautifulSoup
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else url
        text = soup.get_text(separator="\n", strip=True)
        
        return {
            "type": "web",
            "source": url,
            "title": title,
            "content": text,
            "hash": hashlib.sha256(text.encode()).hexdigest()[:16]
        }
    
    def _process_youtube(self, url: str) -> dict:
        import yt_dlp
        
        ydl_opts = {
            "quiet": True,
            "extract_flat": False,
            "writesubtitles": True,
            "writeautomaticsub": True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        return {
            "type": "video",
            "source": url,
            "title": info.get("title", ""),
            "description": info.get("description", ""),
            "transcript": info.get("subtitles", {}),
            "hash": hashlib.sha256(url.encode()).hexdigest()[:16]
        }
    
    def _process_file(self, file_path: str) -> dict:
        path = Path(file_path)
        ext = path.suffix.lower()
        
        if ext == ".pdf":
            return self._process_pdf(file_path)
        elif ext in [".txt", ".md"]:
            return self._process_text(file_path)
        elif ext == ".html":
            return self._process_html(file_path)
        
        raise ValueError(f"Extension no soportada: {ext}")
    
    def _process_pdf(self, file_path: str) -> dict:
        try:
            import pdfplumber
        except ImportError:
            return {"type": "pdf", "source": file_path, "error": "pdfplumber no instalado"}
        
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        
        return {
            "type": "pdf",
            "source": file_path,
            "content": text,
            "hash": hashlib.sha256(text.encode()).hexdigest()[:16]
        }
    
    def _process_text(self, file_path: str) -> dict:
        content = Path(file_path).read_text(encoding="utf-8")
        return {
            "type": "text",
            "source": file_path,
            "content": content,
            "hash": hashlib.sha256(content.encode()).hexdigest()[:16]
        }
    
    def _process_html(self, file_path: str) -> dict:
        from bs4 import BeautifulSoup
        
        content = Path(file_path).read_text(encoding="utf-8")
        soup = BeautifulSoup(content, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        
        return {
            "type": "html",
            "source": file_path,
            "title": soup.title.string if soup.title else file_path,
            "content": text,
            "hash": hashlib.sha256(text.encode()).hexdigest()[:16]
        }
