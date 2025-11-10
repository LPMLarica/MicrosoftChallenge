class HumanAgent:
    def __init__(self, name, knowledge=None):
        self.name = name
        self.knowledge = knowledge

    def handle(self, ticket, note):
        ticket.steps.append({'actor':self.name,'ts':None,'action':'human_response','detail':note})
        ticket.assigned = self.name
        ticket.status = 'in_progress'
