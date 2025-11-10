import os
from dataclasses import dataclass

@dataclass
class Settings:
    HF_API_TOKEN: str = os.getenv('HF_API_TOKEN', '')
    HF_API_URL: str = os.getenv('HF_API_URL', 'https://api-inference.huggingface.co/models/gpt2')
    AZURE_TENANT_ID: str = os.getenv('AZURE_TENANT_ID', '')
    AZURE_CLIENT_ID: str = os.getenv('AZURE_CLIENT_ID', '')
    AZURE_CLIENT_SECRET: str = os.getenv('AZURE_CLIENT_SECRET', '')
    AZURE_REDIRECT_URI: str = os.getenv('AZURE_REDIRECT_URI', 'http://localhost:8501')

settings = Settings()
