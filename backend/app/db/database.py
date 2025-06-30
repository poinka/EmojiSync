import os
import torch
import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import uuid
import random
import faiss


class VectorDB:
    def __init__(self, dim=768, collection_name="my_collection"):
        print("Init database")
        self.dim = dim
        self.collection_name = collection_name
        self.nbits = 128
        self.model = AutoModelForSequenceClassification.from_pretrained('SamLowe/roberta-base-go_emotions')
        self.tokenizer = AutoTokenizer.from_pretrained('SamLowe/roberta-base-go_emotions')
        self.index = faiss.IndexLSH(self.dim, self.nbits)
        self.vector_ids = []
        self.client = QdrantClient(host="qdrant", port=6333) #":memory:" или url="http://localhost:6333"
        self.__setup_db()

    def __setup_db(self, force_recreate=False): # Set True to force recreate the collection
        print("Setup database")
        # создаём коллекцию, если не существует
        if force_recreate:
            if self.client.collection_exists(self.collection_name):
                self.client.delete_collection(self.collection_name)
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.dim,
                    distance=Distance.COSINE
                )
            )
        elif not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.dim,
                    distance=Distance.COSINE
                )
            )
        # Проверка: пуста ли коллекция?
        count = self.client.count(self.collection_name, exact=True).count
        if count < 100000:
            print("Collection is empty — loading dataset...")
            self.__load_dataset()
        else:
            print("Dataset already loaded. Skipping.")
        print("Rebuilding FAISS index...")
        self.__rebuild_faiss_index()
            

    

    def __rebuild_faiss_index(self):
        print("Rebuilding FAISS index...")
        self.index = faiss.IndexLSH(self.dim, self.nbits)
        self.vector_ids = []

        offset = None
        batch = 0
        while True:
            points, next_offset = self.client.scroll(
                collection_name=self.collection_name,
                offset=offset,
                limit=256,
                with_payload=True,
                with_vectors=True
            )

            if not points:
                print("No more points. Finished building FAISS index.")
                break

            for point in points:
                vector = np.array(point.vector, dtype=np.float32)
                self.index.add(vector.reshape(1, -1))
                self.vector_ids.append(str(point.id))

            print(f"Batch {batch}: loaded {len(points)} vectors")
            batch += 1

            # ⛔ Обязательно обнови offset. Если next_offset is None — выход
            if next_offset is None:
                print("Reached end of collection.")
                break
            offset = next_offset





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
            self.add_text(row['quote'], row['author'], row['category'], vector)
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

    def add_text(self, text: str, author: str, category: str, vector):
        #vector = self.encode(text)
        if isinstance(vector, str):
            vector = np.array(eval(vector), dtype=np.float32)
        
        payload = {"text": text, "author": author, "category": category}
        vector_id = str(uuid.uuid4())
        point = PointStruct(
            id=vector_id,
            vector=vector.tolist(),
            payload=payload
        )
        self.client.upsert(collection_name=self.collection_name, points=[point])
        self.index.add(vector.reshape(1, -1))  # FAISS
        self.vector_ids.append(vector_id)

    def search(self, text: str, top_k: int = 10):
        vector = self.encode(text)
        vector = vector / np.linalg.norm(vector)
        vector = vector.reshape(1, -1).astype(np.float32)

        # FAISS LSH поиск
        _, indices = self.index.search(vector, top_k)
        if len(indices[0]) == 0:
            return "No matches found"

        # Найдём id векторов
        nearest_ids = [self.vector_ids[idx] for idx in indices[0] if idx < len(self.vector_ids)]
        if not nearest_ids:
            return "No matches found"

        # Выберем случайный id
        selected_id = random.choice(nearest_ids)

        # Получим payload из Qdrant
        result = self.client.retrieve(collection_name=self.collection_name, ids=[selected_id], with_payload=True)
        return {"text": result[0].payload["text"], 
                "author": result[0].payload["author"]
        }




if __name__ == '__main__':
    db = VectorDB()
    print(db.search("I love potato"))
