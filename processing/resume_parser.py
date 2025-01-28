import json
from abc import ABC, abstractmethod

from llm_integration.llm_client import BaseLLMClient


class BaseResumeParser(ABC):
    def __init__(self, llm_client: BaseLLMClient):
        self.llm_client = llm_client

    @abstractmethod
    def parse_resume(self, text: str) -> dict:
        pass


class StructuredResumeParser(BaseResumeParser):
    PROMPT_TEMPLATE = """Extract and structure resume information following this JSON schema:
    {schema}

    Rules:
    1. Normalize dates to ISO 8601
    2. Preserve original section order
    3. Flag uncertain values with _confidence score
    4. Only send the json data 
    5. Dont give it in markdown format
    6. Dont add any description just give the json response
    7. Do not hallucinate only use the data from the prompt

    Resume Content:
    {content}
    """

    def __init__(self, llm_client: BaseLLMClient):
        super().__init__(llm_client)
        self.json_schema = {
            "personal_info": {
                "full_name": "string",
                "professional_title": "string",
                "contact": {
                    "email": "string",
                    "phone": "string",
                    "address": "string"
                },
                "links": {
                    "linkedin": "url",
                    "github": "url",
                    "portfolio": "url",
                    "other_social": {"platform": "url"}
                }
            },
            "professional_summary": "2-4 sentence paragraph",
            "experience": [
                {
                    "company": "string",
                    "position": "string",
                    "dates": {"start": "YYYY-MM", "end": "YYYY-MM/Present"},
                    "location": "string",
                    "highlights": ["string"],
                    "technologies": ["string"],
                    "achievements": ["string with metrics"],
                    "employment_type": "enum[Full-time, Part-time, Contract, Internship]"
                }
            ],
            "education": [
                {
                    "degree": "string",
                    "institution": "string",
                    "dates": {"start": "YYYY-MM", "end": "YYYY-MM"},
                    "gpa": "number",
                    "honors": ["string"],
                    "thesis": {"title": "string", "description": "string"}
                }
            ],
            "technical_skills": {
                "languages": ["string"],
                "frameworks": ["string"],
                "tools": ["string"],
                "cloud": ["string"],
                "databases": ["string"],
                "certifications": [
                    {
                        "name": "string",
                        "issuer": "string",
                        "date": "YYYY-MM",
                        "validity": "expiration date"
                    }
                ]
            },
            "projects": [
                {
                    "name": "string",
                    "description": "string",
                    "role": "string",
                    "technologies": ["string"],
                    "outcomes": ["string with metrics"],
                    "demo_url": "url",
                    "repo_url": "url"
                }
            ],
            "additional_sections": {
                "publications": [
                    {
                        "title": "string",
                        "publisher": "string",
                        "date": "YYYY-MM",
                        "doi": "string"
                    }
                ],
                "languages": [
                    {
                        "language": "string",
                        "proficiency": "CEFR level (A1-C2)"
                    }
                ],
                "volunteer_work": [
                    {
                        "organization": "string",
                        "role": "string",
                        "duration": "string"
                    }
                ]
            }
        }

    def parse_resume(self, text: str) -> dict:
        schema_str = json.dumps(self.json_schema, indent=2)
        prompt = self.PROMPT_TEMPLATE.format(
            schema=schema_str,
            content=text
        )

        response = self.llm_client.generate_response(
            system_prompt="You are an expert resume parser",
            user_input=prompt
        )

        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            # Add fallback parsing logic here
            raise Exception(e, "failed to parse the response from LLM")
