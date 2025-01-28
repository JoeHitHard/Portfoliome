import os

from dotenv import load_dotenv

from resume_processer import ResumeProcessor

load_dotenv()

# Initialize processor
processor = ResumeProcessor(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    output_dir="./my-portfolio"
)


# Custom answer handler (optional)
def handle_answers(questions):
    answers = {}
    for q in questions:
        print(q['question_text'])
        answers[q['question_type']] = input("> ")
    return answers


# Execute full pipeline
result = processor.process_resume(
    resume_path="Joseph D.pdf",
    answer_handler=handle_answers  # Omit for default CLI input
)

print(f"Generated portfolio at: {result['output_dir']}")
