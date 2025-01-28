# resume_processor/main.py
import json
from pathlib import Path
from typing import Dict, Optional, Callable

from file_processing import FileExtractorFactory
from llm_integration import DeepSeekClient
from processing import StructuredResumeParser
from questionnaire import DesignQuestionnaireGenerator
from portfolio_generator import ReactPortfolioGenerator, PortfolioWriter


class ResumeProcessor:
    def __init__(
            self,
            api_key: str,
            output_dir: str = "./portfolio",
            temp_dir: str = "./tmp",
            log_dir: str = "./logs"
    ):
        self.output_dir = output_dir
        self.temp_dir = temp_dir
        self.log_dir = log_dir

        # Initialize dependencies
        self.llm_client = DeepSeekClient(api_key=api_key)
        self.file_extractor_factory = FileExtractorFactory()
        self.resume_parser = StructuredResumeParser(self.llm_client)
        self.questionnaire_gen = DesignQuestionnaireGenerator(self.llm_client)
        self.portfolio_gen = ReactPortfolioGenerator(self.llm_client)

        self._setup_directories()

    def _setup_directories(self):
        Path(self.temp_dir).mkdir(parents=True, exist_ok=True)
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def process_resume(
            self,
            resume_path: str,
            answer_handler: Optional[Callable] = None
    ) -> Dict[str, str]:
        """
        Execute full processing pipeline:
        1. Resume parsing
        2. Design questionnaire
        3. Portfolio generation

        :param resume_path: Path to resume document
        :param answer_handler: Function to collect user answers
        :return: Generated files metadata
        """
        try:
            print("[INFO] Starting resume processing pipeline...")

            # Step 1: Resume Processing
            print("[INFO] Step 1: Extracting and parsing resume...")
            step1_data = self._process_step1(resume_path)
            print("[SUCCESS] Resume parsing completed.")

            # Step 2: Design Questionnaire
            print("[INFO] Step 2: Generating design questionnaire...")
            questions = self.questionnaire_gen.generate_questions(step1_data)
            answers = self._handle_questionnaire(questions, answer_handler)
            print("[SUCCESS] Questionnaire completed.")

            # Step 3: Portfolio Generation
            print("[INFO] Step 3: Generating portfolio...")
            code_files = self.portfolio_gen.generate_code(step1_data, answers)
            print("[SUCCESS] Portfolio generation completed.")

            # Save results
            print("[INFO] Saving intermediate and final outputs...")
            self._save_intermediate_data(step1_data, "step1_output.json")
            PortfolioWriter.write_files(self.output_dir, code_files)
            print(f"[SUCCESS] Portfolio saved in directory: {self.output_dir}")

            return {
                "resume_data": step1_data,
                "generated_files": list(code_files.keys()),
                "output_dir": str(Path(self.output_dir).resolve())
            }

        except Exception as e:
            self._log_error(f"Processing failed: {str(e)}")
            print(f"[ERROR] Processing failed: {str(e)}")
            raise

    def _process_step1(self, resume_path: str) -> Dict:
        print(f"[INFO] Extracting text from resume at: {resume_path}...")
        extractor = self.file_extractor_factory.get_extractor(resume_path)
        text_content = extractor.extract_text(resume_path)
        print("[INFO] Parsing extracted resume content...")
        return self.resume_parser.parse_resume(text_content)

    def _handle_questionnaire(
            self,
            questions: list,
            answer_handler: Optional[Callable] = None
    ) -> Dict:
        if answer_handler:
            return answer_handler(questions)

        # Default console handler
        print("\n=== Design Questionnaire ===")
        answers = {}
        for idx, q in enumerate(questions, 1):
            print(f"\nQ{idx}: {q['question_text']}")
            for opt in q.get('options', []):
                print(f"  {opt['label']} {opt['value']}")
            answers[q['question_type']] = input("Your answer: ").strip()
        return answers

    def _save_intermediate_data(self, data: Dict, filename: str):
        output_path = Path(self.temp_dir) / filename
        print(f"[INFO] Saving intermediate data to: {output_path}")
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _log_error(self, message: str):
        log_file = Path(self.log_dir) / "errors.log"
        print(f"[INFO] Logging error to: {log_file}")
        with open(log_file, 'a') as f:
            f.write(f"{message}\n")
