from typing import TypedDict, Dict, Any


class CodeFile(TypedDict):
    path: str
    content: str
    is_binary: bool


class PortfolioStructure(TypedDict):
    files: Dict[str, CodeFile]
    dependencies: Dict[str, str]
    configs: Dict[str, Any]
