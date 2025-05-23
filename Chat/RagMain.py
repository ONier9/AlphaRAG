import sys
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import PromptTemplates
import chromadb
import RagConfigFile
import torch
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from transformers import AutoTokenizer, AutoModel, pipeline
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core import PromptTemplate
from llama_index.core.llms import ChatMessage
from llama_index.core import PromptTemplate
from llama_index.core.postprocessor import LongContextReorder 
from llama_index.core.postprocessor import SimilarityPostprocessor
from transformers import AutoModel 
import streamlit as st

@st.cache_resource
def initialize():

    #Ustawienia dla modelu
    Settings.embed_model = HuggingFaceEmbedding(
            model_name="sdadas/mmlw-retrieval-roberta-base"
    )
    Settings.llm = HuggingFaceLLM(
        model_name="eryk-mazus/polka-1.1b-chat",
        tokenizer_name="eryk-mazus/polka-1.1b-chat",
        context_window=1024,
        max_new_tokens=75,
        device_map="cpu"
    )
    #Odczytywanie danych i przenoszenie ich do naszej bazy danych wektorowych - aktualnie dla naszego systemu działają tylko pliki tekstowe
    documents = SimpleDirectoryReader(input_dir=RagConfigFile.DataDirectory).load_data()
    db = chromadb.PersistentClient(
        path=RagConfigFile.ChromaDirectory,
        settings=chromadb.Settings
            (
            anonymized_telemetry=False,
            allow_reset=False))    
    chroma_collection = db.get_or_create_collection(RagConfigFile.ChromaCollection)

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    vector_index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        transformations=[SentenceSplitter
                            (chunk_size=RagConfigFile.DBChunkSize, 
                            chunk_overlap=RagConfigFile.DBChunkOverlap)
                        ],
    )

    #Tworzenie zapytań oraz ich poprawa za pomocą bazy danych
    query_engine = vector_index.as_query_engine(
    response_mode="compact", 
    similarity_top_k=2
    )
    
    qa_template = PromptTemplate(PromptTemplates.FirstPrompt)
    refine_template = PromptTemplate(PromptTemplates.RefinePrompt)
    
    query_engine.update_prompts(
        {
            "response_synthesizer:text_qa_template": qa_template,
            "response_synthesizer:refine_template": refine_template
        }
    )
    
    return query_engine 