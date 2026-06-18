import os
import streamlit as st
from dotenv import load_dotenv

from faq_manager import FAQManager
from gemini_handler import GeminiFAQBot

load_dotenv()

st.set_page_config(
    page_title="FAQ Chatbot Live",
    page_icon="🤖",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #f8fbff 0%, #eef6ff 100%);
    }
    .hero-box {
        padding: 1.5rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #4f46e5, #06b6d4);
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.12);
        margin-bottom: 1rem;
    }
    .chat-card {
        background: white;
        padding: 1rem;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        margin-bottom: 0.75rem;
        border-left: 6px solid #4f46e5;
    }
    .bot-card {
        border-left: 6px solid #06b6d4;
    }
    .small-note {
        color: #475569;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Missing GEMINI_API_KEY. Add it in Streamlit secrets or your local .env file.")
    st.stop()

faq_manager = FAQManager("faqs.csv")
bot = GeminiFAQBot(api_key=api_key)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown(
    """
    <div class="hero-box">
        <h1 style="margin-bottom:0.4rem;">🤖 FAQ Chatbot</h1>
        <p style="font-size:1.05rem; margin-bottom:0;">
            A polished Streamlit chatbot powered by <b>Google Gemini</b>, <b>Pandas</b>, and your FAQ dataset.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

left_col, right_col = st.columns([2, 1])

with right_col:
    st.subheader("⚙️ Dashboard")
    st.metric("Total FAQs", len(faq_manager.df))
    st.metric("Categories", faq_manager.df["category"].nunique())
    st.caption("Deploy this file on Streamlit Cloud using `streamlit_app.py`.")

    with st.expander("📄 FAQ Preview"):
        st.dataframe(faq_manager.df[["category", "question"]], use_container_width=True)

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

with left_col:
    st.subheader("Ask a question")
    user_query = st.text_input(
        "Enter your question here",
        placeholder="Example: How do I run this app?"
    )

    if st.button("✨ Get Answer", use_container_width=True) and user_query:
        matches = faq_manager.find_relevant_faqs(user_query)

        if matches.empty:
            context = "No matching FAQ entries found."
        else:
            context = faq_manager.build_context(matches)

        with st.spinner("Gemini is thinking..."):
            answer = bot.generate_response(user_query, context)

        st.session_state.chat_history.append({
            "question": user_query,
            "answer": answer
        })

    st.markdown("### 💬 Conversation")

    if st.session_state.chat_history:
        for chat in reversed(st.session_state.chat_history):
            st.markdown(
                f"""
                <div class="chat-card">
                    <b>🙋 You:</b><br>{chat['question']}
                </div>
                <div class="chat-card bot-card">
                    <b>🤖 Bot:</b><br>{chat['answer']}
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("Start by asking a question from the FAQ knowledge base.")

st.markdown("---")
st.markdown(
    "<p class='small-note'>Built with Streamlit, Pandas, and Google Gemini API.</p>",
    unsafe_allow_html=True,
)
