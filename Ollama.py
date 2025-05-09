from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage
def get_ollama_response(user_input):
    llm = Ollama(model="SpeakLeash/bielik-7b-instruct-v0.1-gguf:Q4_K_S", request_timeout=120.0,  system_prompt="Odpowiadaj zawsze w języku polskim. Bądź precyzyjny i użyj formalnego stylu.")
    response = llm.chat([ChatMessage(role="user", content=user_input)])
    return response.message.content
