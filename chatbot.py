import json
import os
import nltk
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

THRESHOLD = 0.15
MAX_FAQ_PATH_BASE = os.path.abspath("data")


def load_faqs(path="data/faqs.json"):
    try:
        full_path = os.path.abspath(path)

        # Path traversal protection
        if not full_path.startswith(MAX_FAQ_PATH_BASE):
            raise ValueError("Invalid file path.")

        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Schema validation
        if not isinstance(data, list):
            raise ValueError("FAQ data must be a list.")

        validated = []

        for item in data:
            if (
                isinstance(item, dict)
                and "question" in item
                and "answer" in item
                and isinstance(item["question"], str)
                and isinstance(item["answer"], str)
                and item["question"].strip()
                and item["answer"].strip()
            ):
                validated.append(item)

        if not validated:
            raise ValueError("No valid FAQ entries found.")

        return validated

    except Exception:
        return [
            {
                "question": "Default question",
                "answer": "FAQ data could not be loaded safely.",
            }
        ]


def preprocess(text: str) -> str:
    try:
        stop_words = set(stopwords.words("english"))

        tokens = word_tokenize(text.lower())

        cleaned = [
            token for token in tokens if token.isalpha() and token not in stop_words
        ]

        return " ".join(cleaned)

    except Exception:
        return ""


class FAQChatbot:
    def __init__(self):
        self.faqs = load_faqs()

        questions_raw = [faq["question"] for faq in self.faqs]

        self.answers = [faq["answer"] for faq in self.faqs]

        processed_qs = [preprocess(q) for q in questions_raw]

        self.vectorizer = TfidfVectorizer()

        self.tfidf_matrix = self.vectorizer.fit_transform(processed_qs)

    def get_response(self, user_input: str) -> tuple[str, float]:
        try:
            cleaned = preprocess(user_input)

            if not cleaned.strip():
                return ("Please type a valid question.", 0.0)

            vec = self.vectorizer.transform([cleaned])

            scores = cosine_similarity(vec, self.tfidf_matrix).flatten()

            best_idx = int(np.argmax(scores))
            best_score = float(scores[best_idx])

            if best_score < THRESHOLD:
                return (
                    "Sorry, I couldn't find a match. Please rephrase your question.",
                    best_score,
                )

            return (self.answers[best_idx], best_score)

        except Exception:
            return ("System temporarily unavailable. Please try again later.", 0.0)
