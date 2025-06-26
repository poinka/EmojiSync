import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorDB:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = faiss.IndexFlatL2(384)  # Размер эмбеддингов модели
        self.texts = []

        self.__setup_db()

    def __setup_db(self):
        # TODO
        ...

    def add_text(self, text: str):
        embedding = self.model.encode([text])
        self.index.add(np.array(embedding, dtype='float32'))
        self.texts.append(text)

    def search(self, query: str, top_k: int = 5):
        query_vec = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_vec, dtype='float32'), top_k)
        results = []
        for i in indices[0]:
            if i < len(self.texts):
                results.append(self.texts[i])
        return results
