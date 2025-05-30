__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import chromadb
import RagConfigFile as Config
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
        model_path=Config.ModelPath,
        temperature=Config.Temperature,
        max_new_tokens=Config.MaxNewTokens,
        context_window=Config.ContextWindow,
        generate_kwargs={},
        model_kwargs={"n_gpu_layers": 0},
        verbose=False,
    )

    # Ustawenia dla modelu tworzącego embedy
    Settings.embed_model = HuggingFaceEmbedding(
            model_name=Config.ModelName
        )
    # Odczytywanie danych i przenoszenie ich do naszej bazy danych wektorowych
    # Aktualnie dla naszego systemu działają tylko pliki tekstowe
    documents = SimpleDirectoryReader(input_dir=Config.DataDirectory).load_data()
    db = chromadb.PersistentClient(
        path=Config.ChromaDirectory,
        settings=chromadb.Settings
            (
            anonymized_telemetry=False,
            allow_reset=False))    
    chroma_collection = db.get_or_create_collection(Config.ChromaCollection)

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    

    # Model sprawdza czy baza danych istnieje, jeśli tak to nie tworzy nowej i wyszukuje za pomocą prompta
    if chroma_collection.count() == 0: 
        vector_index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            transformations=[SentenceSplitter
                                (chunk_size=Config.DBChunkSize, 
                                chunk_overlap=Config.DBChunkOverlap)
                            ],
        )
    else:
        vector_index = VectorStoreIndex.from_vector_store(vector_store)
    # Stworzenie silnika dla promptów, w tym przypadku wykorzystujemy compact z małą ilością top_k, co może sprawiać 
    # że nasze dane są nieidealne - w tym przypadku działa dobrze, ponieważ model hallucynował zbyt dużą ilość odpowiedzi
        query_engine = vector_index.as_query_engine(
        response_mode="compact", 
        similarity_top_k=1,
        )
        
    qa_template = PromptTemplate(Config.FirstPrompt)

    query_engine.update_prompts({
        "response_synthesizer:text_qa_template": qa_template
    })
    return query_engine 

