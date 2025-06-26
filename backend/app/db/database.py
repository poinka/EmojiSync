import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

class VectorDB:
    def __init__(self):
        self.model = SentenceTransformer('SamLowe/roberta-base-go_emotions')
        self.index = faiss.IndexFlatL2(768)  # Размер эмбеддингов модели
        self.texts = []

        self.__setup_db()

    def __setup_db(self):
        # TODO
        quotes = pd.read_csv("selected_quotes.csv")
        for _, row in quotes.iterrows():
            self.add_text(row['text'], row['category'])

    def add_text(self, text: str, category: str):
        embedding = self.model.encode([text])
        self.index.add(np.array(embedding, dtype='float32'))
        self.texts.append((text, category))

    def search(self, query: str, top_k: int = 5):
        query_vec = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_vec, dtype='float32'), top_k)
        results = []
        for i in indices[0]:
            if i < len(self.texts):
                results.append(self.texts[i])
        return results
