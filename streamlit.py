import os
import streamlit as st
from dotenv import load_dotenv

from faq_manager import FAQManager
from gemini_handler import GeminiFAQBot

load_dotenv()

st.set_page_config(
    page_title="FAQ Chatbot Live",
    page_icon="✨",
    layout="centered"
)

st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: bold;
            color: #4F46E5;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            text-align: center;
            color: #6B7280;
            margin-bottom: 2rem;
        }
        .answer-box {
            padding: 1rem;
            border-radius: 12px;
            background-color: #F3F4F6;
            border: 1px solid #E5E7EB;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">✨ FAQ Chatbot Sparkle</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask questions from your FAQ data using Google Gemini, Pandas, and Streamlit.</div>', unsafe_allow_html=True)

api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Missing GEMINI_API_KEY. Add it in your local .env or Streamlit Cloud secrets.")
    st.stop()

faq_manager = FAQManager("faqs.csv")
bot = GeminiFAQBot(api_key=api_key)

with st.sidebar:
    st.header("About")
    st.write("This chatbot uses:")
    st.write("- Google Gemini API")
    st.write("- Pandas for FAQ handling")
    st.write("- Streamlit for the UI")
    st.divider()
    if st.checkbox("Show FAQ dataset"):
        st.dataframe(faq_manager.df)

query = st.text_input("Ask your question", placeholder="e.g. How do I run this app?")

if st.button("Get Answer", use_container_width=True):
    if not query.strip():
        st.warning("Please enter a question first.")
    else:
        matches = faq_manager.find_relevant_faqs(query)

        if matches.empty:
            context = "No matching FAQ entries found."
            st.info("No close FAQ match found. Gemini will answer generally.")
        else:
            context = faq_manager.build_context(matches)
            with st.expander("Matched FAQ entries"):
                st.dataframe(matches[["category", "question", "answer"]])

        with st.spinner("Generating your answer..."):
            response = bot.generate_response(query, context)

        st.subheader("Live Answer")
        st.markdown(f'<div class="answer-box">{response}</div>', unsafe_allow_html=True)
