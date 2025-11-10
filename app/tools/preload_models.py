from huggingface_hub import snapshot_download

MODELS = [
    'facebook/bart-large-mnli',
    'philschmid/bart-large-cnn-samsum',
    'deepset/roberta-base-squad2',
    'sentence-transformers/all-MiniLM-L6-v2'
]

if __name__ == '__main__':
    for m in MODELS:
        print('Downloading', m)
        snapshot_download(repo_id=m)
    print('Done')
