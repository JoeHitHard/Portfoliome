import json
from abc import ABC, abstractmethod
from typing import List

from llm_integration import DeepSeekClient
from ..schemas import DesignQuestion


class BaseQuestionnaireGenerator(ABC):
    @abstractmethod
    def generate_questions(self, resume_data: dict) -> List[DesignQuestion]:
        pass


PROMPT_TEMPLATE = """
Analyze this resume JSON and generate design clarification questions following these rules:

1. Identify 3-5 most important missing elements
2. Create questions using this format:
{{
  "question_type": "type",
  "question_text": "text",
  "options": [{{"label": "a)", "value": "option1"}}],
  "multiselect": false
}}

Required question types:
- missing_info: Ask about absent resume sections
- design_preference: Layout/style choices
- content_emphasis: Section prioritization
- style_customization: Color/theming
- interactive_elements: Feature toggles

Resume Data:
{resume_json}

Output ONLY valid JSON array:
"""


class DesignQuestionnaireGenerator(BaseQuestionnaireGenerator):
    def __init__(self, llm_client: DeepSeekClient):
        self.llm_client = llm_client

    def generate_questions(self, resume_data: dict) -> List[DesignQuestion]:
        prompt = PROMPT_TEMPLATE.format(resume_json=json.dumps(resume_data, indent=2))

        response = self.llm_client.generate_response(
            system_prompt="You are a UX-focused portfolio design assistant",
            user_input=prompt
        )

        return self._parse_response(response)

    def _parse_response(self, raw_response: str) -> List[DesignQuestion]:
        try:
            return json.loads(raw_response)
        except json.JSONDecodeError:
            return []
