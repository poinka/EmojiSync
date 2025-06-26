from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer
import numpy as np
import uuid


class VectorDB:
    def __init__(self, dim=384, collection_name="my_collection"):
        self.dim = dim
        self.collection_name = collection_name
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = QdrantClient(":memory:")  # или url="http://localhost:6333"

        self.__setup_db()

    def __setup_db(self):
        # (пере)создаём коллекцию, если не существует
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
        """Заполнение базы из датасета (можно заменить на загрузку файла)"""
        print("Инициализация коллекции: загрузка датасета...")
        initial_texts = [
            "Artificial intelligence is transforming the world.",
            "Qdrant is a vector similarity search engine.",
            "Transformers models produce embeddings from text.",
            "Semantic search helps find relevant information.",
            "Natural Language Processing is a core AI field."
        ]
        for text in initial_texts:
            self.add_text(text)

    def encode(self, text: str) -> np.ndarray:
        embedding = self.model.encode(text, normalize_embeddings=True)
        return np.array(embedding, dtype='float32')

    def add_text(self, text: str, metadata: dict = None):
        vector = self.encode(text)
        payload = {"text": text}
        if metadata:
            payload.update(metadata)
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
