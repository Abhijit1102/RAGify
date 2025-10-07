from src.config import Config
from src.vector_db.qdrant_connection import qdrant_client
from qdrant_client.http import models as rest
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, FilterSelector


class QdrantManager:
    """Singleton manager for Qdrant client."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QdrantManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return
        if not qdrant_client:
            raise ValueError("Qdrant client not initialized")
        self.client = qdrant_client
        self._initialized = True

    def get_collection_manager(self, collection_name: str, vector_size: int = Config.OPENAI_EMBEDDING_DIMENSION):
        """Return a per-user collection manager."""
        return UserCollectionManager(self.client, collection_name, vector_size)


class UserCollectionManager:
    """Manager for a single Qdrant collection (per user)."""

    def __init__(self, client, collection_name: str, vector_size: int):
        self.client = client
        self.collection_name = collection_name
        self.vector_size = vector_size

    def create_collection(self):
        """Ensure the collection exists. Create it if missing."""
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=rest.VectorParams(
                    size=self.vector_size,
                    distance=rest.Distance.COSINE
                )
            )
            # Create payload index for filtering
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="file_name",
                field_schema=rest.PayloadSchemaType.KEYWORD
            )

    def insert_data(self, vectors: list, payloads: list, ids: list = None, batch_size: int = 100):
        import hashlib

        # Generate unique IDs if not provided
        if ids is None:
            ids = [
                int(hashlib.md5(payloads[i]["text"].encode("utf-8")).hexdigest(), 16) % (10**18)
                for i in range(len(payloads))
            ]

        for i in range(0, len(vectors), batch_size):
            batch_points = [
                {"id": ids[j], "vector": vectors[i + j], "payload": payloads[i + j]}
                for j in range(len(vectors[i:i + batch_size]))
            ]
            self.client.upsert(collection_name=self.collection_name, points=batch_points)

    def search(self, query_vector: list, limit: int = 5):
        return self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=True
        )

    def get_text_from_results(self, results):
        return "\n\n".join([p.payload.get("text", "") for p in results])

    def delete_by_file_name(self, file_name: str):
        """Delete all vectors for a specific file."""
        filter_condition = Filter(
            must=[FieldCondition(key="file_name", match=MatchValue(value=file_name))]
        )
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=FilterSelector(filter=filter_condition)
        )


# Singleton instance
qdrant_manager = QdrantManager()
