def test_hf_client_basic_import():
    from app.core.hf_client import get_hf_client
    hf = get_hf_client()
    assert hasattr(hf, 'classify')
    assert hasattr(hf, 'summarize')
    assert hasattr(hf, 'embed')
