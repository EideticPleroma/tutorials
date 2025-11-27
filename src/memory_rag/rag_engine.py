"""
RAG Engine for indexing and querying the tutorial codebase.

This is the main interface for RAG operations in Tutorial 3.
"""

import logging
from pathlib import Path
from typing import Optional

# TODO: Import LlamaIndex components
# from llama_index.core import (
#     VectorStoreIndex,
#     StorageContext,
#     load_index_from_storage,
# )

from .config import configure_for_project
from .document_loaders import load_all_project_files

logger = logging.getLogger(__name__)


class RAGEngine:
    """
    Main interface for RAG operations on the tutorial codebase.
    
    Provides methods to:
    - Build an index from project files
    - Load an existing index from storage
    - Query the index for relevant content
    - Retrieve raw chunks without generation
    
    Example:
        >>> engine = RAGEngine()
        >>> engine.build_index(".")
        >>> response = engine.query("How does the coordinator work?")
        >>> print(response)
    """
    
    def __init__(self, persist_dir: str = "./storage/project_index"):
        """
        Initialize RAG engine.
        
        Args:
            persist_dir: Directory to store/load the index.
        """
        self.persist_dir = persist_dir
        self.index = None
        logger.info("RAGEngine initialized with persist_dir: %s", persist_dir)
    
    def build_index(self, base_path: str = ".") -> None:
        """
        Build index from project files.
        
        Args:
            base_path: Root path of the project to index.
            
        Raises:
            RuntimeError: If indexing fails.
        
        Example:
            >>> engine = RAGEngine()
            >>> engine.build_index(".")
            >>> # Index is now ready for queries
        """
        # TODO: Implement index building
        # 1. Call configure_for_project()
        # 2. Load documents with load_all_project_files()
        # 3. Create VectorStoreIndex.from_documents()
        # 4. Persist to self.persist_dir
        # 5. Store index in self.index
        
        logger.info("Building index from %s", base_path)
        
        # Configure LlamaIndex
        configure_for_project()
        
        # Load documents
        documents = load_all_project_files(base_path)
        
        if not documents:
            raise RuntimeError("No documents loaded. Check your paths and filters.")
        
        logger.info("Creating index from %d documents...", len(documents))
        
        # TODO: Create index
        # self.index = VectorStoreIndex.from_documents(
        #     documents,
        #     show_progress=True,
        # )
        
        # TODO: Persist
        # Path(self.persist_dir).mkdir(parents=True, exist_ok=True)
        # self.index.storage_context.persist(persist_dir=self.persist_dir)
        
        logger.info("Index built and saved to %s", self.persist_dir)
    
    def load_index(self) -> None:
        """
        Load existing index from storage.
        
        Raises:
            FileNotFoundError: If index doesn't exist at persist_dir.
        
        Example:
            >>> engine = RAGEngine()
            >>> engine.load_index()
            >>> response = engine.query("test")
        """
        # TODO: Implement index loading
        # 1. Check persist_dir exists
        # 2. Load using StorageContext and load_index_from_storage
        # 3. Store in self.index
        
        if not Path(self.persist_dir).exists():
            raise FileNotFoundError(
                f"Index not found at {self.persist_dir}. "
                "Run build_index() first."
            )
        
        logger.info("Loading index from %s", self.persist_dir)
        
        # TODO: Load index
        # storage_context = StorageContext.from_defaults(persist_dir=self.persist_dir)
        # self.index = load_index_from_storage(storage_context)
        
        logger.info("Index loaded successfully")
    
    def query(self, question: str, top_k: int = 5) -> str:
        """
        Query the index and return a generated response.
        
        Args:
            question: Natural language question about the codebase.
            top_k: Number of chunks to retrieve for context.
            
        Returns:
            Generated response as a string.
            
        Raises:
            RuntimeError: If index not loaded.
        
        Example:
            >>> response = engine.query("What is the 7-step tool calling loop?")
            >>> print(response)
        """
        if self.index is None:
            raise RuntimeError("Index not loaded. Call build_index() or load_index() first.")
        
        # TODO: Implement query
        # 1. Create query engine with similarity_top_k
        # 2. Query and return response as string
        
        logger.info("Querying: %s", question[:100])
        
        # query_engine = self.index.as_query_engine(similarity_top_k=top_k)
        # response = query_engine.query(question)
        # return str(response)
        
        return "TODO: Implement query"
    
    def retrieve(self, question: str, top_k: int = 5) -> list:
        """
        Retrieve relevant chunks without generation.
        
        Args:
            question: Natural language question about the codebase.
            top_k: Number of chunks to retrieve.
            
        Returns:
            List of dicts with keys: text, score, metadata
        
        Example:
            >>> chunks = engine.retrieve("coordinator delegate", top_k=3)
            >>> for chunk in chunks:
            ...     print(f"{chunk['score']:.3f}: {chunk['metadata']['file_path']}")
        """
        if self.index is None:
            raise RuntimeError("Index not loaded. Call build_index() or load_index() first.")
        
        # TODO: Implement retrieval
        # 1. Create retriever with similarity_top_k
        # 2. Retrieve nodes
        # 3. Format as list of dicts
        
        logger.info("Retrieving for: %s", question[:100])
        
        # retriever = self.index.as_retriever(similarity_top_k=top_k)
        # nodes = retriever.retrieve(question)
        # 
        # return [
        #     {
        #         "text": node.text,
        #         "score": node.score,
        #         "metadata": node.metadata,
        #     }
        #     for node in nodes
        # ]
        
        return []

