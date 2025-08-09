"""
RAG pipeline wiring: splitter -> embeddings -> vector store -> retriever.
"""
import os
from typing import List, Optional
from dataclasses import dataclass
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Weaviate as LCWeaviate
import weaviate
import weaviate.embedded as weaviate_embedded

from .text_utils import normalize_text, clean_and_reduce_noise
from .prompts import format_docs

@dataclass
class RAGConfig:
    collection: str = os.getenv("RAG_COLLECTION", "HODLDocs")
    chunk_size: int = int(os.getenv("RAG_CHUNK_SIZE", "1200"))
    chunk_overlap: int = int(os.getenv("RAG_CHUNK_OVERLAP", "200"))
    embed_model: str = os.getenv("EMBED_MODEL", "text-embedding-3-small")
    use_embedded_weaviate: bool = os.getenv("WEAVIATE_EMBEDDED", "1") == "1"

def _weaviate_client(cfg: RAGConfig):
    if cfg.use_embedded_weaviate:
        return weaviate.Client(additional_config=weaviate_embedded.EmbeddedOptions().to_dict())
    return weaviate.Client(os.getenv("WEAVIATE_URL", "http://localhost:8080"))

def build_vector_store(texts: List[str], cfg: Optional[RAGConfig]=None):
    cfg = cfg or RAGConfig()
    _ = _weaviate_client(cfg)
    splitter = RecursiveCharacterTextSplitter(chunk_size=cfg.chunk_size, chunk_overlap=cfg.chunk_overlap)
    chunks = []
    for t in texts:
        t2 = clean_and_reduce_noise(normalize_text(t))
        chunks.extend(splitter.split_text(t2))
    embeddings = OpenAIEmbeddings(model=cfg.embed_model)
    vs = LCWeaviate.from_texts(chunks, embeddings, index_name=cfg.collection)
    return vs

def get_retriever(vector_store, k: int = 5):
    return vector_store.as_retriever(search_kwargs={"k": k})
