from transformers import pipeline

question_generator = pipeline("text2text-generation", model="valhalla/t5-base-e2e-qg")


def generate_questions(text):
    questions = question_generator(f"generate questions: {text}")
    return [q['generated_text'] for q in questions]
