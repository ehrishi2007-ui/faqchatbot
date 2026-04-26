import json
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)

THRESHOLD = 0.15  # minimum score to return a match


def load_faqs(path="data/faqs.json"):
    with open(path, "r") as f:
        return json.load(f)


def preprocess(text: str) -> str:
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text.lower())
    cleaned = [t for t in tokens if t.isalpha() and t not in stop_words]
    return " ".join(cleaned)


class FAQChatbot:
    def __init__(self):
        self.faqs = load_faqs()
        questions_raw = [faq["question"] for faq in self.faqs]
        self.answers = [faq["answer"] for faq in self.faqs]

        processed_qs = [preprocess(q) for q in questions_raw]
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(processed_qs)

    def get_response(self, user_input: str) -> tuple[str, float]:
        cleaned = preprocess(user_input)
        if not cleaned.strip():
            return "Please type a valid question.", 0.0

        vec = self.vectorizer.transform([cleaned])
        scores = cosine_similarity(vec, self.tfidf_matrix).flatten()
        best_idx = int(np.argmax(scores))
        best_score = float(scores[best_idx])

        if best_score < THRESHOLD:
            return (
                "Sorry, I couldn't find a match. Try rephrasing or contact support@example.com.",
                best_score,
            )
        return self.answers[best_idx], best_score
