import os
import torch
import faiss
import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import uuid
import random


class VectorDB:
    def __init__(self, dim=768, collection_name="my_collection"):
        print("Init database")
        self.dim = dim
        self.collection_name = collection_name
        self.nbits = 128
        self.model = AutoModelForSequenceClassification.from_pretrained('SamLowe/roberta-base-go_emotions')
        self.tokenizer = AutoTokenizer.from_pretrained('SamLowe/roberta-base-go_emotions')
        self.client = QdrantClient(":memory:")  # или url="http://localhost:6333"
        self.index = faiss.IndexLSH(self.dim, self.nbits)
        self.vector_ids = []
        self.__setup_db()

    def __setup_db(self):
        print("Setup database")
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
        quotes = pd.read_csv("selected_quotes_embeddings.csv")
        limit = 100000
        vectors = []
        for i, row in quotes.iterrows():
            if isinstance(row['embeddings'], str):
                vector = np.array(eval(row['embeddings']), dtype=np.float32)
            else:
                vector = row['embeddings']
            vector = vector / np.linalg.norm(vector)
            vectors.append(vector)
            self.add_text(row['quote'], row['category'], vector)
            if i > limit:
                break
        self.index.add(np.array(vectors, dtype=np.float32))

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

    def add_text(self, text: str, category: str, vector):
        #vector = self.encode(text)
        if isinstance(vector, str):
            vector = np.array(eval(vector), dtype=np.float32)
        
        payload = {"text": text, "category": category}
        vector_id = str(uuid.uuid4())
        point = PointStruct(
            id=vector_id,
            vector=vector.tolist(),
            payload=payload
        )
        self.client.upsert(collection_name=self.collection_name, points=[point])
        self.vector_ids.append(vector_id)
        self.index.add(vector.reshape(1, -1))

    def search(self, text: str, top_k: int = 10):
        vector = self.encode(text)
        vector = vector / np.linalg.norm(vector)
        vector = vector.reshape(1, -1).astype(np.float32)
        _, indices = self.index.search(vector, top_k)
        if len(indices[0]) == 0:
            return "No matches found"
        nearest_ids = [self.vector_ids[idx] for idx in indices[0] if idx < len(self.vector_ids)]
        if not nearest_ids:
            return "No matches found"
        selected_id = random.choice(nearest_ids)
        result = self.client.retrieve(collection_name=self.collection_name, ids=[selected_id], with_payload=True)
        return result[0].payload["text"]


if __name__ == '__main__':
    db = VectorDB()
    print(db.search("I love potato"))