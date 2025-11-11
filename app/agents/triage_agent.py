from core.hf_client import get_hf_client
from agents.intake_agent import now_iso
import json

class TriageAgent:
    def __init__(self, name, knowledge):
        self.name = name
        self.knowledge = knowledge
        self.hf = get_hf_client()

    def log(self, ticket, action, detail, confidence=0.0):
        ticket.steps.append({'actor':self.name,'ts':now_iso(),'action':action,'detail':detail,'confidence':confidence})

    def triage(self, ticket):
        labels = ['Password Reset','HR Request','Finance Issue','Access Problem','Other']
        try:
            resp = self.hf.classify(ticket.description, labels)
            confidence = max(resp.get('scores', [0])) if resp.get('scores') else 0.0
            explanation = resp.get('labels', [])
        except Exception:
            resp = {'labels': [], 'scores': []}
            confidence = 0.0
            explanation = []
        docs = self.knowledge.search(ticket.subject+' '+ticket.description)
        suggestion = {'suggested_runbook': None, 'escalate': False, 'explanation': explanation, 'confidence': confidence, 'relevant_docs': docs}
        if 'password' in ticket.subject.lower() or 'reset' in ticket.subject.lower():
            suggestion['suggested_runbook'] = 'reset_password'
        if suggestion['confidence'] < 0.7:
            suggestion['escalate'] = True
        self.log(ticket, 'triage', json.dumps(suggestion), suggestion['confidence'])
        return suggestion
