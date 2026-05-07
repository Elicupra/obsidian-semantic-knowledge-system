import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional


class NoteGenerator:
    def __init__(self, vault_path: Path, include_metadata: bool = True):
        self.vault_path = vault_path
        self.include_metadata = include_metadata
    
    def generate(self, data: dict, category: Optional[str] = None) -> Path:
        content = data.get("content", data.get("description", ""))
        title = data.get("title", "Sin título")
        
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
                "title": title,
                "source": source,
                "type": input_type,
                "created": datetime.now().isoformat(),
                "category": category or "N/A",
            }
            lines.append("---")
            lines.append(yaml.dump(metadata, default_flow_style=False, allow_unicode=True))
            lines.append("---\n")
        
        lines.append(f"# {title}\n")
        
        if content:
            lines.append(content)
        
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
