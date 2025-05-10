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
    Settings.embed_model = OllamaEmbedding(model_name=RagConfigFile.EmbeddingModelName)
    Settings.llm = Ollama(
        model=RagConfigFile.ModelName,
        request_timeout=RagConfigFile.Timeout
    )

    documents = SimpleDirectoryReader(input_dir=RagConfigFile.DataDirectory).load_data()
    
    db = chromadb.PersistentClient(path=RagConfigFile.ChromaDirectory)    
    chroma_collection = db.get_or_create_collection(RagConfigFile.ChromaCollection)

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    vector_index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        transformations=[SentenceSplitter
                            (chunk_size=RagConfigFile.ChunkSize, 
                            chunk_overlap=RagConfigFile.ChunkOverlap)
                        ],
    )
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