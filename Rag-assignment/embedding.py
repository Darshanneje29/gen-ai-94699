from typing import List
from langchain.embeddings import init_embeddings


embed_model = init_embeddings(
    model="text-embedding-all-minilm-l6-v2-embedding",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy_api",
    check_embedding_ctx_length=False,
)

def get_embeddings(texts: List[str]) -> List[list[float]]:
    if not texts:
        return []
    
    embedeings=embed_model.embed_documents(texts) 
    return embedeings
