import json
import re
from abc import ABC, abstractmethod
from typing import Dict

from llm_integration import DeepSeekClient
from ..schemas import CodeFile


class BasePortfolioGenerator(ABC):
    @abstractmethod
    def generate_code(
            self,
            resume_data: dict,
            design_answers: dict
    ) -> Dict[str, CodeFile]:
        pass


PROMPT_TEMPLATE = """
Generate a React portfolio website using these inputs:

1. Resume Data:
{resume_json}

2. Design Choices:
{design_choices}

Technical Requirements:
- React 18+ functional components
- CSS Modules for styling
- Framer Motion animations
- Mobile-first responsive design
- WCAG 2.1 AA compliant
- Use JSON data from './data/resume.json'

File Structure:
{file_structure}

Create ALL files following these rules:
1. Use /** @component */ JSDoc tags
2. Include prop-types where applicable
3. Use CSS custom properties from theme.css
4. Add ARIA labels for accessibility
5. Implement error boundaries

Output format for each file:
=== relative_file_path ===
file_content
===
"""


class ReactPortfolioGenerator(BasePortfolioGenerator):
    def __init__(self, llm_client: DeepSeekClient):
        self.llm_client = llm_client

    def generate_code(self, resume_data: dict, design_answers: dict) -> Dict[str, CodeFile]:
        prompt = self._build_prompt(resume_data, design_answers)
        response = self.llm_client.generate_response(
            system_prompt="You are an expert React full-stack developer",
            user_input=prompt
        )
        return self._parse_response(response)

    def _build_prompt(self, resume_data: dict, design_answers: dict) -> str:
        return PROMPT_TEMPLATE.format(
            resume_json=json.dumps(resume_data, indent=2),
            design_choices=json.dumps(design_answers, indent=2),
            file_structure=self._render_file_tree()
        )

    def _render_file_tree(self) -> str:
        return """
        src/
        ├── components/
        │   ├── App.jsx
        │   ├── Header.jsx
        │   ├── Experience.jsx
        │   ├── Projects.jsx
        │   └── Skills.jsx
        ├── styles/
        │   ├── theme.css
        │   └── components/
        │       ├── Experience.module.css
        │       └── Projects.module.css
        └── data/
            └── resume.json
        """

    def _parse_response(self, raw_response: str) -> Dict[str, CodeFile]:
        pattern = r"=== (.*?) ===\n(.*?)(?=\n===|$)"
        files = {}
        for match in re.finditer(pattern, raw_response, re.DOTALL):
            path = match.group(1).strip()
            content = match.group(2).strip()
            files[path] = CodeFile(
                path=path,
                content=content,
                is_binary=False
            )
        return files
