class VectorKnowledge:
    def __init__(self):
        self.docs = []

    def load_synthetic(self):
        self.docs = [
            {'id':'doc1','title':'Password reset','text':'Confirm identity and generate token.'},
            {'id':'doc2','title':'Leave policy','text':'Maternity leave 120 days.'}
        ]

    def search(self, q, top_k=3):
        if not isinstance(q, str) or not q.strip():
            return []
        
        ql = q.lower()
        res = [d for d in self.docs if ql in d['text'].lower() or ql in d['title'].lower()]
        
        return res[:top_k]
