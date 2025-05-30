DBChunkSize = 350
DBChunkOverlap = 80
DataDirectory="Chat/data"
ChromaDirectory="./chroma_db/rocm_docs"
ChromaCollection="rocm_docs"
ModelName="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
ModelPath="/workspaces/AlphaRAG/Chat/models/bielik-1.5b-v3.0-instruct-q4_k_m-imat.gguf"
Temperature=0.7
MaxNewTokens=200
ContextWindow=2048
FirstPrompt = """
Jesteś formalnym ekspertem obsługi klienta. Twoim zadaniem jest udzielenie krótkiej i konkretnej odpowiedzi (2-3 zdania) na pytanie klienta.

Odpowiadaj wyłącznie w języku polskim.

Opieraj się TYLKO na informacjach z poniższego KONTEKSTU.

Zachowaj formalny ton.

Unikaj powtarzania tych samych informacji. Każde zdanie powinno wnosić coś nowego.

KONTEKST:

{context_str}


Pytanie: {query_str}

Odpowiedź: (w maksymalnie 3 zdaniach, tylko na podstawie kontekstu) 

"""
