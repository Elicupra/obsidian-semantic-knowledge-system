import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional, Any
import json


class NoteGenerator:
    def __init__(self, vault_path: Path, include_metadata: bool = True):
        self.vault_path = vault_path
        self.include_metadata = include_metadata
    
    def generate(self, data: dict, category: Optional[str] = None) -> Path:
        content = data.get("content", data.get("description", ""))
        title = data.get("title", "Sin titulo")
        
        markdown = self._build_markdown(
            title=title,
            content=content,
            source=data.get("source", ""),
            input_type=data.get("type", "unknown"),
            category=category
        )
        
        file_path = self._save_note(title, markdown, category)
        return file_path
    
    def _build_markdown(self, title: str, content: str, source: str, input_type: str, category: Optional[str]) -> str:
        lines = []
        
        if self.include_metadata:
            metadata = {
                "title": str(title),
                "source": str(source),
                "type": str(input_type),
                "created": datetime.now().isoformat(),
                "category": str(category or "N/A"),
            }
            lines.append("---")
            lines.append(self._simple_yaml_dump(metadata))
            lines.append("---\n")
        
        lines.append(f"# {title}\n")
        
        if content:
            lines.append(str(content))
        
        return "\n".join(lines)
    
    def _simple_yaml_dump(self, data: dict) -> str:
        lines = []
        for key, value in data.items():
            if isinstance(value, str):
                lines.append(f"{key}: {value}")
            elif isinstance(value, (int, float, bool)):
                lines.append(f"{key}: {value}")
            elif value is None:
                lines.append(f"{key}: null")
            else:
                lines.append(f"{key}: {json.dumps(value)}")
        return "\n".join(lines)
    
    def _save_note(self, title: str, content: str, category: Optional[str]) -> Path:
        safe_title = self._sanitize_filename(title)
        
        if category:
            folder = self.vault_path / category
            folder.mkdir(parents=True, exist_ok=True)
            file_path = folder / f"{safe_title}.md"
        else:
            file_path = self.vault_path / f"{safe_title}.md"
        
        file_path.write_text(content, encoding="utf-8")
        return file_path
    
    def _sanitize_filename(self, name: str) -> str:
        import re
        name = re.sub(r'[<>:"/\\|?*]', "_", name)
        name = name[:200]
        return name.strip("_")