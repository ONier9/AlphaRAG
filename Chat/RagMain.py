__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import PromptTemplates
import chromadb
import RagConfigFile
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import PromptTemplate
import streamlit as st
from llama_index.llms.llama_cpp import LlamaCPP 


@st.cache_resource
def initialize():

    #Ustawienia dla modelu
 
    Settings.llm = LlamaCPP(
        model_url=None, 
        model_path="/workspaces/AlphaRAG/Chat/bielik-1.5b-v3.0-instruct-q4_k_m-imat.gguf",
        temperature=0.7,
        max_new_tokens=200,
        context_window=2048,
        generate_kwargs={},
        model_kwargs={"n_gpu_layers": 0},
        verbose=False,
    )
    Settings.embed_model = HuggingFaceEmbedding(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
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
    
    if chroma_collection.count() == 0: 
        vector_index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            transformations=[SentenceSplitter
                                (chunk_size=RagConfigFile.DBChunkSize, 
                                chunk_overlap=RagConfigFile.DBChunkOverlap)
                            ],
        )
    else:
        vector_index = VectorStoreIndex.from_vector_store(vector_store)
        query_engine = vector_index.as_query_engine(
        response_mode="compact", 
        similarity_top_k=1,
        )
        
    qa_template = PromptTemplate(PromptTemplates.FirstPrompt)

    query_engine.update_prompts({
        "response_synthesizer:text_qa_template": qa_template
    })
    return query_engine 

