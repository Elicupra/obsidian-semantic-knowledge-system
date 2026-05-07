import re
from pathlib import Path
from collections import defaultdict


class BacklinkManager:
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.link_pattern = re.compile(r'\[\[([^\]]+)\]\]')
    
    def generate_report(self) -> dict:
        backlinks = defaultdict(list)
        total_links = 0
        
        for md_file in self.vault_path.rglob("*.md"):
            if md_file.name.startswith("."):
                continue
            
            content = md_file.read_text(encoding="utf-8")
            links = self.link_pattern.findall(content)
            
            for link in links:
                backlinks[link].append(str(md_file.relative_to(self.vault_path)))
                total_links += 1
        
        return {
            "total_notes": len(list(self.vault_path.rglob("*.md"))),
            "total_backlinks": total_links,
            "backlinks": dict(backlinks)
        }
