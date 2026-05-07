import hashlib
from pathlib import Path
from collections import defaultdict


class Deduplicator:
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
    
    def find_duplicates(self) -> list[list[str]]:
        hash_to_files = defaultdict(list)
        
        for md_file in self.vault_path.rglob("*.md"):
            if md_file.name.startswith("."):
                continue
            
            content = md_file.read_text(encoding="utf-8")
            file_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
            hash_to_files[file_hash].append(str(md_file.relative_to(self.vault_path)))
        
        return [files for files in hash_to_files.values() if len(files) > 1]
