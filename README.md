System RAG działający za pomocą streamlit i Ollama, używający Bielik (wersja Mistral AI skupiona na języku polskim) jako swojego LLM. Jest to system bazowany na podstawie architektury mojego komputera, który poiada kartę nvidia, na której go testowałam przez co może mieć problemy z działaniem na innych systemach. Aby sprawdzić działanie systemu można dodać do /chat/data dodatkowe pliki tekstowe z informacjami dla chatbota.


Aby włączyć poprawnie system należy użyć w folderze /chat
```
./docker-startup.sh build
```
A następnie użyć, aby działało na CPU
```
./docker-startup.sh deploy
```
Lub użyć tego, aby działało na GPU.
```
./docker-startup.sh deploy-gpu
```
