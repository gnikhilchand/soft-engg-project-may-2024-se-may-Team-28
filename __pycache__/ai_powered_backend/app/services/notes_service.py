# from transformers import pipeline
#
# notes_generator = pipeline("text-generation", model="meta-llama/Meta-Llama-3.1-8B-Instruct")
#
#
# def generate_notes(topic):
#     notes = notes_generator(topic, max_length=150, num_return_sequences=1)
#     return notes[0]['generated_text']
