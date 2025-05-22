__import__('pysqlite3')
import PromptTemplates
import chromadb
import RagConfigFile
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import PromptTemplate
from llama_index.core.llms import ChatMessage
from llama_index.core import PromptTemplate

def initialize():

    #Ustawienia dla modelu
    Settings.embed_model = OllamaEmbedding(model_name=RagConfigFile.EmbeddingModelName)
    Settings.llm = Ollama(
        model=RagConfigFile.LLMModelName,
        request_timeout=RagConfigFile.AIQueryTimeout,
        num_ctx=RagConfigFile.AIContextSize
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
    query_engine = vector_index.as_query_engine(response_mode="refine", similarity_top_k=3)
    
    qa_template = PromptTemplate(PromptTemplates.FirstPrompt)
    refine_template = PromptTemplate(PromptTemplates.RefinePrompt)
    
    query_engine.update_prompts(
        {
            "response_synthesizer:text_qa_template": qa_template,
            "response_synthesizer:refine_template": refine_template
        }
    )
    
    return query_engine