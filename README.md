# 💬 FAQ Chatbot using NLP + Streamlit

An intelligent FAQ Chatbot built using Python, Streamlit, Natural Language Processing (NLP), TF-IDF Vectorization, and Cosine Similarity.

This chatbot helps users get instant answers to frequently asked questions by matching user queries with the most relevant stored FAQs instead of using hardcoded keyword matching.

It provides a clean chat-style interface, confidence score for responses, session-based chat history, and security improvements for safe deployment.

---

# 🚀 Features

* Interactive chat-style UI using Streamlit
* FAQ matching using TF-IDF + Cosine Similarity
* NLP preprocessing using NLTK
* Confidence score for each response
* Sidebar with example questions
* Clear chat functionality
* Session-based chat history
* Secure JSON loading and validation
* XSS protection using HTML escaping
* Input length limitation
* Session-based rate limiting
* Exception-safe error handling
* Automatic chat history trimming

---

# 🛠 Tech Stack

## Frontend

* Streamlit

## Backend

* Python

## NLP Libraries

* NLTK
* Scikit-learn

## Data Handling

* JSON

## Similarity Matching

* TF-IDF Vectorizer
* Cosine Similarity

---

# 📂 Project Structure

```text
FAQ_Chatbot/
│
├── app.py
├── chatbot.py
│
├── data/
│   └── faqs.json
│
├── requirements.txt
└── README.md
```

---

# 📘 How It Works

1. FAQs are stored inside `faqs.json`
2. Questions are preprocessed using NLP:

   * Lowercasing
   * Tokenization
   * Stopword removal
3. TF-IDF converts text into numerical vectors
4. Cosine similarity compares user input with stored FAQs
5. Best matching answer is returned to the user
6. Confidence score is displayed with the answer

---

# 🔐 Security Fixes Implemented

This project includes fixes for common chatbot security vulnerabilities:

* XSS prevention for unsafe HTML rendering
* Path traversal protection for JSON loading
* JSON schema validation
* Input length limitation (max 500 chars)
* Session-based request limiting
* Exception-safe error handling
* Chat history memory control

These improvements make the chatbot safer and more production-ready.

---

# ▶ Installation

## Step 1: Clone Repository

```bash
git clone https://github.com/your-username/faq-chatbot.git
cd faq-chatbot
```

---

## Step 2: Create Virtual Environment

```bash
python -m venv .venv
```

Activate environment:

### Windows

```bash
.venv\Scripts\activate
```

### Mac/Linux

```bash
source .venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4: Run Application

```bash
streamlit run app.py
```

The app will open in your browser automatically.

Usually at:

```text
http://localhost:8501
```

---

# 📦 requirements.txt

```text
streamlit
nltk
scikit-learn
numpy
```

---

# 🎯 Example Questions

* What is your return policy?
* How do I track my order?
* Do you offer free shipping?
* How can I contact support?
* What payment methods do you accept?

---

# 🌟 Future Improvements

* Voice-based chatbot
* Admin panel for managing FAQs
* Database integration
* Hugging Face transformer models
* Context-aware chatbot
* User feedback learning system
* Deployment on Streamlit Cloud

---


# 📄 License

This project was built as part of a student internship task at [CodeAlpha](https://www.codealpha.tech).
