from google import genai


class GeminiFAQBot:
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate_response(self, user_query: str, context: str) -> str:
        prompt = f"""
You are a helpful FAQ chatbot.

Use the FAQ context below to answer the user's question.
If the answer is not clearly available in the context, say that politely and provide the best helpful response you can.

FAQ Context:
{context}

User Question:
{user_query}
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text
