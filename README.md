# FAQ Chatbot

An intelligent FAQ chatbot built with **Google Gemini API**, **Streamlit**, and **Pandas**.

## Features
- Ask questions through a simple Streamlit UI
- Load and manage FAQ data from CSV using Pandas
- Use Gemini to answer based on FAQ context
- Easy to customize and extend

## Project Structure

```text
.
├── app.py
├── faq_manager.py
├── gemini_handler.py
├── faqs.csv
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

1. Clone the repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file from `.env.example`
4. Add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```
5. Run the app:
   ```bash
   streamlit run app.py
   ```

## FAQ CSV Format

The CSV file uses these columns:
- `category`
- `question`
- `answer`
- `keywords`

## Notes

- This project demonstrates **Pandas basics** like loading CSVs, filtering rows, and simple text matching.
- Gemini is used to generate a polished response grounded in the FAQ data.
