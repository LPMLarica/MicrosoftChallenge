from services.runbooks import evaluate_runbook_safety, execute_runbook

class RunbookAgent:
    def __init__(self, name, knowledge):
        self.name = name
        self.knowledge = knowledge

    def log(self, ticket, action, detail):
        ticket.steps.append({'actor':self.name,'ts':None,'action':action,'detail':detail})

    def consider_and_run(self, ticket, runbook_id, auto_approve=False):
        self.log(ticket, 'consider_runbook', runbook_id)
        safe, reasons = evaluate_runbook_safety(runbook_id, ticket)
        if not safe:
            self.log(ticket, 'runbook_blocked', str(reasons))
            return {'status':'blocked','reasons':reasons}
        inputs = {k: ticket.metadata.get(k, 'AUTO') for k in []}
        result = execute_runbook(runbook_id, ticket, inputs)
        self.log(ticket, 'runbook_executed', result.get('outcome'))
        return result
