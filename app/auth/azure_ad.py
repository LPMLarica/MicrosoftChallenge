# Minimal Azure AD MSAL helper (used by Streamlit app)
from msal import ConfidentialClientApplication
from app.config.settings import settings

def get_msal_app():
    if not settings.AZURE_CLIENT_ID or not settings.AZURE_TENANT_ID:
        raise RuntimeError('Azure AD not configured')
    return ConfidentialClientApplication(client_id=settings.AZURE_CLIENT_ID,
                                         client_credential=settings.AZURE_CLIENT_SECRET,
                                         authority=f'https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}')

def build_auth_url(state, scope=None, redirect_uri=None):
    app = get_msal_app()
    return app.get_authorization_request_url(scopes=scope or [], state=state, redirect_uri=redirect_uri or settings.AZURE_REDIRECT_URI)

def acquire_token_by_code(code, scopes=None, redirect_uri=None):
    app = get_msal_app()
    return app.acquire_token_by_authorization_code(code, scopes=scopes or [], redirect_uri=redirect_uri or settings.AZURE_REDIRECT_URI)
