import os
import streamlit as st
from dotenv import load_dotenv

from faq_manager import FAQManager
from gemini_handler import GeminiFAQBot

load_dotenv()

st.set_page_config(
    page_title="FAQ Chatbot Live",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 FAQ Chatbot")
st.caption("Live FAQ assistant powered by Google Gemini, Pandas, and Streamlit")

api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Missing GEMINI_API_KEY. Add it in Streamlit secrets or your local .env file.")
    st.stop()

faq_manager = FAQManager("faqs.csv")
bot = GeminiFAQBot(api_key=api_key)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.header("About")
    st.write("This chatbot answers questions using FAQ data and Gemini.")
    st.subheader("FAQ Preview")
    st.dataframe(faq_manager.df[["category", "question"]], use_container_width=True)
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

st.subheader("Ask your question")
user_query = st.text_input("Type your question here")

if st.button("Get Answer") and user_query:
    matches = faq_manager.find_relevant_faqs(user_query)

    if matches.empty:
        context = "No matching FAQ entries found."
    else:
        context = faq_manager.build_context(matches)

    with st.spinner("Thinking..."):
        answer = bot.generate_response(user_query, context)

    st.session_state.chat_history.append({
        "question": user_query,
        "answer": answer
    })

if st.session_state.chat_history:
    st.subheader("Conversation")
    for idx, chat in enumerate(reversed(st.session_state.chat_history), start=1):
        with st.container():
            st.markdown(f"**You:** {chat['question']}")
            st.markdown(f"**Bot:** {chat['answer']}")
            st.divider()
else:
    st.info("Ask a question to start chatting.")
