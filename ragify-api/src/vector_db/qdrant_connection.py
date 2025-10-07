from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from src.config import Config
import time

def get_qdrant_client(max_retries=3, retry_interval=5):
    """Return a connected Qdrant client."""
    retries = 0
    while retries < max_retries:
        try:
            client = QdrantClient(
                url=Config.QDRANT_URL,
                api_key=Config.QDRANT_API_KEY,
                timeout=10
            )
            client.get_collections()  # health check
            print("✅ Qdrant connected")
            return client
        except UnexpectedResponse as e:
            print(f"❌ Qdrant error: {e}")
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")
        retries += 1
        time.sleep(retry_interval)
    raise ConnectionError("Failed to connect to Qdrant after retries.")

qdrant_client = get_qdrant_client()
