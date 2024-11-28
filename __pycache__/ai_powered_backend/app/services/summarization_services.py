from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def summarize_transcript(transcript):
    summary = summarizer(transcript, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']
