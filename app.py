import os
import streamlit as st
from dotenv import load_dotenv

from faq_manager import FAQManager
from gemini_handler import GeminiFAQBot

load_dotenv()

st.set_page_config(page_title="FAQ Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 FAQ Chatbot")
st.write("Ask a question based on your FAQ dataset using Gemini, Pandas, and Streamlit.")

api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Missing GEMINI_API_KEY. Please add it to your .env file or Streamlit secrets.")
    st.stop()

faq_manager = FAQManager("faqs.csv")
bot = GeminiFAQBot(api_key=api_key)

with st.expander("View FAQ Data"):
    st.dataframe(faq_manager.df)

user_query = st.text_input("Enter your question:")

if st.button("Ask") and user_query:
    matches = faq_manager.find_relevant_faqs(user_query)

    if matches.empty:
        st.warning("No relevant FAQ found. Gemini will answer more generally.")
        context = "No matching FAQ entries found."
    else:
        st.subheader("Matched FAQs")
        st.dataframe(matches[["category", "question", "answer"]])
        context = faq_manager.build_context(matches)

    with st.spinner("Generating answer..."):
        response = bot.generate_response(user_query, context)

    st.subheader("Answer")
    st.write(response)
