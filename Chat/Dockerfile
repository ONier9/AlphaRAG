FROM nvidia/cuda:12.2.2-base-ubuntu22.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://ollama.ai/install.sh | sh

ENV PATH="/usr/local/cuda/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"

COPY requirements.txt .
COPY ollama-start.sh .

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x ollama-start.sh

COPY . .

EXPOSE 8501
EXPOSE 11434
ENTRYPOINT ["./ollama-start.sh"]