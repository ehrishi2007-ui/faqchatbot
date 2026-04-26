# app.py (SECURE VERSION)

import streamlit as st
import html
from chatbot import FAQChatbot

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="FAQ Chatbot", page_icon="💬", layout="centered")

# ---------------- SECURITY CONSTANTS ----------------
MAX_INPUT_LENGTH = 500
MAX_MESSAGES = 100
MAX_REQUESTS_PER_MINUTE = 20

# ---------------- SAFE CSS ----------------
st.markdown(
    """
<style>
.user-bubble {
    background: #4f46e5;
    color: white;
    padding: 10px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 6px 0 6px auto;
    max-width: 75%;
    width: fit-content;
    font-size: 15px;
    word-wrap: break-word;
}

.bot-bubble {
    background: #f0f2f6;
    color: #1a1a2e;
    padding: 10px 16px;
    border-radius: 18px 18px 18px 4px;
    margin: 6px auto 6px 0;
    max-width: 75%;
    width: fit-content;
    font-size: 15px;
    word-wrap: break-word;
}

.score-pill {
    font-size: 11px;
    color: #888;
    margin-left: 8px;
}
</style>
""",
    unsafe_allow_html=True,
)


# ---------------- LOAD BOT ----------------
@st.cache_resource
def load_bot():
    try:
        return FAQChatbot()
    except Exception:
        st.error("Failed to load chatbot data safely.")
        st.stop()


bot = load_bot()


# ---------------- RATE LIMITING ----------------
if "request_count" not in st.session_state:
    st.session_state.request_count = 0

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "bot",
            "text": "Hi! I'm your FAQ assistant. Ask me anything.",
            "score": None,
        }
    ]


def safe_html(text):
    return html.escape(str(text))


def trim_chat_history():
    if len(st.session_state.messages) > MAX_MESSAGES:
        st.session_state.messages = st.session_state.messages[-MAX_MESSAGES:]


# ---------------- HEADER ----------------
st.title("💬 FAQ Chatbot")
st.caption("Powered by TF-IDF + cosine similarity")
st.divider()


# ---------------- RENDER CHAT ----------------
for msg in st.session_state.messages:
    safe_text = safe_html(msg["text"])

    if msg["role"] == "user":
        st.markdown(
            f'<div class="user-bubble">{safe_text}</div>', unsafe_allow_html=True
        )
    else:
        score_html = ""

        if msg["score"] is not None:
            score_html = (
                f'<span class="score-pill">confidence: {msg["score"]:.0%}</span>'
            )

        st.markdown(
            f'<div class="bot-bubble">{safe_text}{score_html}</div>',
            unsafe_allow_html=True,
        )


# ---------------- USER INPUT ----------------
st.divider()
user_input = st.chat_input("Type your question here...")


if user_input:
    # Input length protection
    user_input = user_input.strip()[:MAX_INPUT_LENGTH]

    if not user_input:
        st.warning("Please enter a valid question.")
        st.stop()

    # Simple session rate limiting
    if st.session_state.request_count >= MAX_REQUESTS_PER_MINUTE:
        st.warning("Rate limit reached. Please wait before sending more messages.")
        st.stop()

    st.session_state.request_count += 1

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "text": user_input, "score": None}
    )

    try:
        answer, score = bot.get_response(user_input)

        st.session_state.messages.append(
            {"role": "bot", "text": answer, "score": score}
        )

    except Exception:
        st.session_state.messages.append(
            {
                "role": "bot",
                "text": "Something went wrong. Please try again later.",
                "score": None,
            }
        )

    trim_chat_history()
    st.rerun()


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("Try asking:")

    example_questions = [
        "What is your return policy?",
        "How do I track my order?",
        "Do you offer free shipping?",
        "How can I contact support?",
        "What payment methods do you accept?",
    ]

    for q in example_questions:
        if st.button(q, use_container_width=True):
            st.session_state.messages.append(
                {"role": "user", "text": q[:MAX_INPUT_LENGTH], "score": None}
            )

            try:
                answer, score = bot.get_response(q)

                st.session_state.messages.append(
                    {"role": "bot", "text": answer, "score": score}
                )

            except Exception:
                st.session_state.messages.append(
                    {
                        "role": "bot",
                        "text": "Unable to process request safely.",
                        "score": None,
                    }
                )

            trim_chat_history()
            st.rerun()

    st.divider()

    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "bot", "text": "Chat cleared! Ask me anything.", "score": None}
        ]
        st.session_state.request_count = 0
        st.rerun()
