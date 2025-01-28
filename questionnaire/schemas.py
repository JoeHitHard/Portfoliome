from typing import TypedDict, List, Dict

class QuestionOption(TypedDict):
    label: str
    value: str

class DesignQuestion(TypedDict):
    question_type: str
    question_text: str
    options: List[QuestionOption]
    multiselect: bool