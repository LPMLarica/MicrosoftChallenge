from dataclasses import dataclass, field
import uuid, datetime
from app.services.vector_knowledge import VectorKnowledge

def now_iso(): return datetime.datetime.utcnow().isoformat()+'Z'

@dataclass
class Ticket:
    ticket_id: str
    created_at: str
    user_display: str
    channel: str
    subject: str
    description: str
    status: str = 'open'
    assigned: str = None
    steps: list = field(default_factory=list)
    runbook_executions: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

class IntakeAgent:
    def __init__(self, name, knowledge: VectorKnowledge):
        self.name = name
        self.knowledge = knowledge

    def process(self, user, subject, description, channel='web'):
        t = Ticket(ticket_id='T-'+uuid.uuid4().hex[:8], created_at=now_iso(), user_display=user, channel=channel, subject=subject, description=description)
        t.steps.append({'actor':self.name,'ts':now_iso(),'action':'intake','detail':f'captured from {user}'})
        t.metadata['keywords'] = (subject+' '+description)[:200]
        return t
