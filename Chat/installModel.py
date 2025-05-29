from huggingface_hub import hf_hub_download
hf_hub_download(repo_id="oskarraszkiewicz/Bielik-1.5B-v3.0-Instruct-Q4_K_M-GGUF", 
                filename="bielik-1.5b-v3.0-instruct-q4_k_m-imat.gguf", 
                local_dir=".")