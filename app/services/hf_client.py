import requests, json
from app.config.settings import settings
import logging
LOG = logging.getLogger('hf_client')

def huggingface_infer(prompt: str, model_url: str = None, api_token: str = None, timeout: int = 10):
    model_url = model_url or settings.HF_API_URL
    api_token = api_token or settings.HF_API_TOKEN
    headers = {'Authorization': f'Bearer {api_token}'} if api_token else {}
    payload = {'inputs': prompt, 'options': {'wait_for_model': True}}
    try:
        r = requests.post(model_url, headers=headers, json=payload, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list):
            text = data[0].get('generated_text') or str(data[0])
        elif isinstance(data, dict):
            text = data.get('generated_text') or json.dumps(data)
        else:
            text = str(data)
        return {'text': text, 'confidence': 0.85, 'raw': data}
    except Exception as e:
        LOG.exception('HF inference error')
        return {'text': '', 'confidence': 0.0, 'error': str(e)}
