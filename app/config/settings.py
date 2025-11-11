import os
from dataclasses import dataclass
import dotenv


dotenv.load_dotenv()

@dataclass
class Settings:
    AZURE_TENANT_ID: str = os.getenv('AZURE_TENANT_ID', '')
    AZURE_CLIENT_ID: str = os.getenv('AZURE_CLIENT_ID', '')
    AZURE_CLIENT_SECRET: str = os.getenv('AZURE_CLIENT_SECRET', '')
    AZURE_REDIRECT_URI: str = os.getenv('AZURE_REDIRECT_URI', 'http://localhost:8501')

settings = Settings()
