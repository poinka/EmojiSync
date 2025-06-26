import os
import torch
import faiss
import numpy as np
import pandas as pd
import torch
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import uuid


class VectorDB:
    def __init__(self, dim=768, collection_name="my_collection"):
        print("Init database")
        self.dim = dim
        self.collection_name = collection_name
        self.model = AutoModelForSequenceClassification.from_pretrained('SamLowe/roberta-base-go_emotions')
        self.tokenizer = AutoTokenizer.from_pretrained('SamLowe/roberta-base-go_emotions')
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

    def encode(self, text, device='cpu'):
        # Tokenization
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        inputs = {key: val.to(device) for key, val in inputs.items()}
        
        # Get model outputs
        with torch.no_grad():
            outputs = self.model(**inputs, output_hidden_states=True)
        
        # Extract the last hidden state (batch_size, seq_len, hidden_size)
        hidden_states = outputs.hidden_states[-1]  # Last layer
        # Use the [CLS] token embedding (first position)
        cls_embedding = hidden_states[:, 0, :].squeeze().cpu().numpy()
        return cls_embedding.astype(np.float32)

    def add_text(self, text: str, category: str):
        vector = self.encode(text)
        payload = {"text": text, "category": category}
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector.tolist(),
            payload=payload
        )
        self.client.upsert(collection_name=self.collection_name, points=[point])

    def search(self, text: str, top_k: int = 1):
        vector = self.get_embedding(text, self.tokenizer, self.model)
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=vector.tolist(),
            limit=top_k,
            with_payload=True
        )
        return [hit.payload['text'] for hit in results.points][0]


if __name__ == '__main__':
    db = VectorDB()
    print(db.search("I love potato"))