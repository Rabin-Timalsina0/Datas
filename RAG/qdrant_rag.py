import os
import logging
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, PointStruct
from transformers import AutoTokenizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FAQ-Retriever")

# Use environment variables directly (set via Cloud Run secrets/env vars)
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not QDRANT_URL:
    raise ValueError("QDRANT_URL environment variable must be set")
if not QDRANT_API_KEY:
    logger.warning("QDRANT_API_KEY not set, continuing without authentication")

# Initialize Qdrant client
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    timeout=30,
    prefer_grpc=False
)

# Test connection at startup
try:
    collections = client.get_collections()
    logger.info(f"Connected to Qdrant. Available collections: {[c.name for c in collections.collections]}")
except Exception as e:
    logger.error(f"Failed to connect to Qdrant: {str(e)}")
    raise

class FAQRetriever:
    def __init__(self, score_threshold: float = 0.4):
        self.score_threshold = score_threshold
        self.cache = {}
        
    def get_answer(self, query: str) -> str:
        cache_key = query.lower().strip()
        if cache_key in self.cache:
            return self.cache[cache_key]
            
        try:
            tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
            inputs = tokenizer(query, return_tensors='pt', padding='max_length', max_length=16, truncation=True)
            query_embedding = inputs['input_ids'].squeeze(0).tolist()  # Using input_ids as embedding
            
            results = client.query_points(
                collection_name="faqs",
                query=query_embedding,
                limit=1,
                score_threshold=self.score_threshold,
                with_payload=True
            )
            
            if results and results.points:
                response = results.points[0].payload.get("answer", "No answer field in payload")
                self.cache[cache_key] = response
                return response
            else:
                return "I couldn't find an answer to your question. Please contact support for help."
                
        except Exception as e:
            logger.error(f"FAQ search error: {str(e)}")
            return "I'm having trouble accessing our knowledge base. Please try again later."
