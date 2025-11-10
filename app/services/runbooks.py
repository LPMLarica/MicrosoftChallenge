RUNBOOKS = {
    'reset_password': {
        'id': 'reset_password',
        'title': 'Reset Password',
        'description': 'Generate temporary token after identity confirmation.',
        'inputs': ['user_id', 'validation_method'],
        'safety_checks': ['identity_confirmed', 'not_high_privilege'],
        'steps': ['Generate token', 'Store hashed token', 'Notify user']
    }
}

def evaluate_runbook_safety(runbook_id, ticket):
    runbook = RUNBOOKS.get(runbook_id)
    if not runbook:
        return False, ['runbook_not_found']
    reasons = []
    for c in runbook['safety_checks']:
        if c == 'identity_confirmed' and not ticket.metadata.get('identity_confirmed'):
            reasons.append('identity_not_confirmed')
        if c == 'not_high_privilege' and ticket.metadata.get('user_role') == 'admin':
            reasons.append('target_high_privilege')
    return (len(reasons) == 0), reasons

def execute_runbook(runbook_id, ticket, inputs):
    ok, reasons = evaluate_runbook_safety(runbook_id, ticket)
    record = {'exec_id': 'exec-'+ticket.ticket_id, 'runbook_id': runbook_id, 'ok': ok, 'reasons': reasons, 'log': []}
    if not ok:
        record['outcome'] = 'blocked'
        record['log'].append({'msg': 'safety_failed', 'details': reasons})
    else:
        for s in runbook['steps']:
            record['log'].append({'msg': f'executed: {s}'})
        record['outcome'] = 'success'
    ticket.runbook_executions.append(record)
    ticket.steps.append({'actor': 'runbook', 'note': f'executed {runbook_id}', 'meta': record})
    return record
