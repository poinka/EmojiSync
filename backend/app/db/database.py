import os

import faiss
import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer
import numpy as np
import uuid


class VectorDB:
    def __init__(self, dim=768, collection_name="my_collection"):
        print("Init database")
        self.dim = dim
        self.collection_name = collection_name
        self.model = SentenceTransformer('SamLowe/roberta-base-go_emotions')
        self.client = QdrantClient(":memory:")  # или url="http://localhost:6333"
        self.__setup_db()

    def __setup_db(self):
        # создаём коллекцию, если не существует
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.dim,
                    distance=Distance.COSINE
                )
            )
        # Проверка: пуста ли коллекция?
        count = self.client.count(self.collection_name, exact=True).count
        if count == 0:
            self.__load_dataset()

    def __load_dataset(self):
        """Заполнение базы из датасета"""
        print("Fill database")
        quotes = pd.read_csv("selected_quotes.csv")
        limit = 100
        for i, row in quotes.iterrows():
            self.add_text(row['quote'], row['category'])
            if i > limit:
                break

    def encode(self, text: str) -> np.ndarray:
        embedding = self.model.encode(text, normalize_embeddings=True)
        return np.array(embedding, dtype='float32')

    def add_text(self, text: str, category: str):
        vector = self.encode(text)
        payload = {"text": text, "category": category}
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector.tolist(),
            payload=payload
        )
        self.client.upsert(collection_name=self.collection_name, points=[point])

    def search(self, query: str, top_k: int = 1):
        query_vector = self.encode(query)
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector.tolist(),
            limit=top_k,
            with_payload=True
        )
        return [hit.payload['text'] for hit in results.points][0]


if __name__ == '__main__':
    db = VectorDB()
    print(db.search("I love potato"))