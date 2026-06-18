import pandas as pd


class FAQManager:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = self.load_faqs()

    def load_faqs(self) -> pd.DataFrame:
        df = pd.read_csv(self.csv_path)
        df.columns = [col.strip().lower() for col in df.columns]

        required = {"category", "question", "answer", "keywords"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        df = df.fillna("")
        return df

    def find_relevant_faqs(self, query: str, top_n: int = 5) -> pd.DataFrame:
        query_words = query.lower().split()

        def score_row(row):
            text = f"{row['question']} {row['answer']} {row['keywords']}".lower()
            return sum(word in text for word in query_words)

        scored = self.df.copy()
        scored["score"] = scored.apply(score_row, axis=1)
        scored = scored[scored["score"] > 0].sort_values(by="score", ascending=False)

        return scored.head(top_n)

    def build_context(self, matches: pd.DataFrame) -> str:
        if matches.empty:
            return "No FAQ context available."

        context_blocks = []
        for _, row in matches.iterrows():
            block = (
                f"Category: {row['category']}\n"
                f"Question: {row['question']}\n"
                f"Answer: {row['answer']}\n"
                f"Keywords: {row['keywords']}"
            )
            context_blocks.append(block)

        return "\n\n".join(context_blocks)
