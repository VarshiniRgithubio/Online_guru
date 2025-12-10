"""
Data ingestion module for building the vector database.
Loads PDF and TXT files, creates embeddings, and stores in FAISS.
"""

import os
from pathlib import Path
from typing import List, Optional
import pickle

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from loguru import logger

from config import settings


class DataIngestionPipeline:
    """Handles data loading, chunking, and vector database creation."""
    
    def __init__(self):
        """Initialize the data ingestion pipeline."""
        self.embeddings = self._load_embeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        logger.info("Data ingestion pipeline initialized")
    
    @staticmethod
    def _load_embeddings() -> HuggingFaceEmbeddings:
        """
        Load multilingual sentence-transformers embeddings model.
        Supports English, Hindi, Telugu, and Kannada.
        
        Returns:
            HuggingFaceEmbeddings instance
        """
        logger.info("Loading multilingual sentence-transformers embeddings model")
        logger.info(f"Model: {settings.multilingual_embedding_model}")
        embeddings = HuggingFaceEmbeddings(
            model_name=settings.multilingual_embedding_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        logger.success("Multilingual embeddings model loaded successfully")
        logger.info(f"Supported languages: {', '.join(settings.supported_languages)}")
        return embeddings
    
    def load_pdf_files(self, folder_path: str) -> List[Document]:
        """
        Load all PDF files from a folder.
        
        Args:
            folder_path: Path to folder containing PDF files
        
        Returns:
            List of Document objects
        """
        try:
            logger.info(f"Loading PDF files from: {folder_path}")
            loader = DirectoryLoader(
                folder_path,
                glob="**/*.pdf",
                loader_cls=PyPDFLoader,
                show_progress=True,
                use_multithreading=True
            )
            documents = loader.load()
            logger.success(f"Loaded {len(documents)} PDF documents")
            return documents
        except Exception as e:
            logger.error(f"Error loading PDF files: {str(e)}")
            return []
    
    def load_txt_files(self, folder_path: str) -> List[Document]:
        """
        Load all TXT files from a folder with UTF-8 encoding for multilingual support.
        
        Args:
            folder_path: Path to folder containing TXT files
        
        Returns:
            List of Document objects
        """
        try:
            logger.info(f"Loading TXT files from: {folder_path}")
            
            # Custom loader to ensure UTF-8 encoding
            txt_files = list(Path(folder_path).rglob("*.txt"))
            documents = []
            
            for txt_file in txt_files:
                try:
                    with open(txt_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    doc = Document(
                        page_content=content,
                        metadata={"source": str(txt_file)}
                    )
                    documents.append(doc)
                except Exception as e:
                    logger.warning(f"Failed to load {txt_file}: {str(e)}")
                    continue
            
            logger.success(f"Loaded {len(documents)} TXT documents with UTF-8 encoding")
            return documents
        except Exception as e:
            logger.error(f"Error loading TXT files: {str(e)}")
            return []
    
    def load_all_documents(self, data_folder: Optional[str] = None) -> List[Document]:
        """
        Load all PDF and TXT files from the data folder with multilingual support.
        
        Args:
            data_folder: Path to data folder (uses config default if None)
        
        Returns:
            List of all loaded Document objects
        """
        data_folder = data_folder or settings.data_folder
        logger.info(f"Loading all multilingual documents from: {data_folder}")
        
        # Check if folder exists
        if not Path(data_folder).exists():
            logger.warning(f"Data folder does not exist: {data_folder}")
            Path(data_folder).mkdir(parents=True, exist_ok=True)
            logger.info(f"Created data folder: {data_folder}")
            return []
        
        # Load PDFs
        pdf_docs = self.load_pdf_files(data_folder)
        
        # Load TXTs (including multilingual transcripts)
        txt_docs = self.load_txt_files(data_folder)
        
        # Combine all documents
        all_documents = pdf_docs + txt_docs
        logger.info(f"Total multilingual documents loaded: {len(all_documents)}")
        
        return all_documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks.
        
        Args:
            documents: List of Document objects
        
        Returns:
            List of chunked Document objects
        """
        if not documents:
            logger.warning("No documents to split")
            return []
        
        logger.info(f"Splitting {len(documents)} documents into chunks")
        chunks = self.text_splitter.split_documents(documents)
        logger.success(f"Created {len(chunks)} chunks")
        return chunks
    
    def create_vector_store(
        self,
        documents: List[Document],
        persist_path: Optional[str] = None
    ) -> FAISS:
        """
        Create FAISS vector store from documents.
        
        Args:
            documents: List of Document objects
            persist_path: Path to save the vector store
        
        Returns:
            FAISS vector store
        """
        if not documents:
            raise ValueError("No documents provided to create vector store")
        
        persist_path = persist_path or settings.vector_db_path
        
        logger.info(f"Creating FAISS vector store with {len(documents)} documents")
        vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        logger.success("Vector store created successfully")
        
        # Save vector store
        self.save_vector_store(vector_store, persist_path)
        
        return vector_store
    
    @staticmethod
    def save_vector_store(vector_store: FAISS, path: str) -> None:
        """
        Save FAISS vector store to disk.
        
        Args:
            vector_store: FAISS vector store instance
            path: Directory path to save the vector store
        """
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            vector_store.save_local(path)
            logger.success(f"Vector store saved to: {path}")
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")
            raise
    
    def load_vector_store(self, path: Optional[str] = None) -> Optional[FAISS]:
        """
        Load FAISS vector store from disk.
        
        Args:
            path: Directory path containing the vector store
        
        Returns:
            FAISS vector store or None if not found
        """
        path = path or settings.vector_db_path
        
        try:
            if not Path(path).exists():
                logger.warning(f"Vector store not found at: {path}")
                return None
            
            logger.info(f"Loading vector store from: {path}")
            vector_store = FAISS.load_local(
                path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            logger.success("Vector store loaded successfully")
            return vector_store
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            return None
    
    def build_vector_db(
        self,
        data_folder: Optional[str] = None,
        force_rebuild: bool = False
    ) -> FAISS:
        """
        Complete pipeline: load documents, chunk, and create vector store.
        
        Args:
            data_folder: Path to data folder
            force_rebuild: If True, rebuild even if vector store exists
        
        Returns:
            FAISS vector store
        """
        # Check if vector store already exists
        if not force_rebuild:
            existing_store = self.load_vector_store()
            if existing_store:
                logger.info("Using existing vector store")
                return existing_store
        
        logger.info("Building vector database from scratch")
        
        # Load all documents
        documents = self.load_all_documents(data_folder)
        
        if not documents:
            raise ValueError(
                f"No documents found in {data_folder or settings.data_folder}. "
                "Please add PDF or TXT files to the data folder."
            )
        
        # Split into chunks
        chunks = self.split_documents(documents)
        
        # Create and save vector store
        vector_store = self.create_vector_store(chunks)
        
        logger.success("Vector database built successfully")
        return vector_store


def main():
    """CLI entry point for data ingestion."""
    import sys
    
    logger.info("Starting data ingestion pipeline")
    
    # Check for force rebuild flag
    force_rebuild = "--rebuild" in sys.argv
    
    try:
        pipeline = DataIngestionPipeline()
        vector_store = pipeline.build_vector_db(force_rebuild=force_rebuild)
        
        # Display statistics
        logger.info(f"Vector store contains {vector_store.index.ntotal} vectors")
        logger.success("Data ingestion completed successfully")
        
    except Exception as e:
        logger.error(f"Data ingestion failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
