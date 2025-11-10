from app.services.hf_client import huggingface_infer
from app.services.vector_knowledge import VectorKnowledge
import json

class TriageAgent:
    def __init__(self, name, knowledge: VectorKnowledge):
        self.name = name
        self.knowledge = knowledge

    def log(self, ticket, action, detail, confidence=0.0):
        ticket.steps.append({'actor':self.name,'ts':None,'action':action,'detail':detail,'confidence':confidence})

    def triage(self, ticket):
        prompt = f'Triage ticket:\nSubject: {ticket.subject}\nDescription: {ticket.description}\n'
        resp = huggingface_infer(prompt)
        docs = self.knowledge.search(ticket.subject+' '+ticket.description)
        suggestion = {'suggested_runbook': None, 'escalate': False, 'explanation': resp.get('text',''), 'confidence': resp.get('confidence',0.0), 'relevant_docs': docs}
        if 'password' in ticket.subject.lower() or 'reset' in ticket.subject.lower():
            suggestion['suggested_runbook'] = 'reset_password'
        if suggestion['confidence'] < 0.7:
            suggestion['escalate'] = True
        self.log(ticket, 'triage', json.dumps(suggestion), suggestion['confidence'])
        return suggestion
