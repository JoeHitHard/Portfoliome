from pathlib import Path
from typing import Dict

from .schemas import CodeFile


class PortfolioWriter:
    @staticmethod
    def write_files(output_dir: str, files: Dict[str, CodeFile]):
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        for rel_path, file in files.items():
            full_path = Path(output_dir) / rel_path
            full_path.parent.mkdir(parents=True, exist_ok=True)

            if file['is_binary']:
                with open(full_path, 'wb') as f:
                    f.write(file['content'].encode('utf-8'))
            else:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(file['content'])
