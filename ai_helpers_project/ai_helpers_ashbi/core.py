"""
ai_helpers_ashbi.core
AI helper functions with structured responses.
"""

import re


def detect_category(text: str) -> str:
    """
    Simple keyword-based category detection.
    """
    text = text.lower()

    if text.startswith("what is") or "definition" in text:
        return "definition"
    elif text.startswith("how to") or text.startswith("how do"):
        return "how-to"
    elif text.endswith("?"):
        return "question"
    elif "," in text:
        return "list"
    else:
        return "general"


def get_response(prompt: str) -> dict:
    """
    Generate AI-style response with metadata.
    Returns dictionary required by Flask app.
    """
    response_text = f"This is a generated response for: {prompt}"

    category = detect_category(prompt)
    word_count = len(response_text.split())

    return {
        "prompt": prompt,
        "response": response_text,
        "category": category,
        "word_count": word_count
    }


def summarize_text(text: str, max_sentences: int = 2) -> str:
    """
    Very basic sentence-based summarizer.
    """
    sentences = re.split(r'(?<=[.!?]) +', text)
    summary = " ".join(sentences[:max_sentences])
    return summary.strip()

def format_response(text: str) -> str:
    """
    Clean and format response text.
    """
    return text.strip().capitalize()