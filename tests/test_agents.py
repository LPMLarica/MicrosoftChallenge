from app.agents.intake_agent import IntakeAgent
from app.services.vector_knowledge import VectorKnowledge

def test_intake_creates_ticket():
    k = VectorKnowledge(); k.load_synthetic()
    intake = IntakeAgent('I', k)
    t = intake.process('u','subject','desc')
    assert t.user_display == 'u'
    assert t.subject == 'subject'
    assert hasattr(t, 'ticket_id')
