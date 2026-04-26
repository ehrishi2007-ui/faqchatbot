import streamlit as st
from chatbot import FAQChatbot

# ── Page config ──────────────────────────────────────────────
st.set_page_config(page_title="FAQ Chatbot", page_icon="💬", layout="centered")

# ── Custom CSS for chat bubbles ───────────────────────────────
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


# ── Load chatbot (cached so it only builds TF-IDF once) ───────
@st.cache_resource
def load_bot():
    return FAQChatbot()


bot = load_bot()

# ── Session state for chat history ────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "bot",
            "text": "Hi! I'm your FAQ assistant. Ask me anything.",
            "score": None,
        }
    ]

# ── Header ─────────────────────────────────────────────────────
st.title("💬 FAQ Chatbot")
st.caption("Powered by TF-IDF + cosine similarity")
st.divider()

# ── Render chat history ────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="user-bubble">{msg["text"]}</div>', unsafe_allow_html=True
        )
    else:
        score_html = ""
        if msg["score"] is not None:
            score_html = (
                f'<span class="score-pill">confidence: {msg["score"]:.0%}</span>'
            )
        st.markdown(
            f'<div class="bot-bubble">{msg["text"]}{score_html}</div>',
            unsafe_allow_html=True,
        )

# ── Input box at bottom ────────────────────────────────────────
st.divider()
user_input = st.chat_input("Type your question here...")

if user_input:
    # Save user message
    st.session_state.messages.append(
        {"role": "user", "text": user_input, "score": None}
    )

    # Get bot response
    answer, score = bot.get_response(user_input)
    st.session_state.messages.append({"role": "bot", "text": answer, "score": score})

    # Rerun to update UI
    st.rerun()

# ── Sidebar with example questions ────────────────────────────
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
            st.session_state.messages.append({"role": "user", "text": q, "score": None})
            answer, score = bot.get_response(q)
            st.session_state.messages.append(
                {"role": "bot", "text": answer, "score": score}
            )
            st.rerun()

    st.divider()
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "bot", "text": "Chat cleared! Ask me anything.", "score": None}
        ]
        st.rerun()
