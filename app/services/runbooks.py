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

def evaluate_runbook_safety(runbook_id_or_obj, ticket):
    if isinstance(runbook_id_or_obj, str):
        runbook = RUNBOOKS.get(runbook_id_or_obj)
        if runbook is None:
            for k, v in RUNBOOKS.items():
                if k.lower() == runbook_id_or_obj.lower():
                    runbook = v
                    break
    elif isinstance(runbook_id_or_obj, dict):
        runbook = runbook_id_or_obj
    else:
        runbook = None

    if not runbook:
        return False, ['runbook_not_found']

    reasons = []
    safety_checks = runbook.get('safety_checks', [])
    metadata = getattr(ticket, 'metadata', {}) or {}

    for c in safety_checks:
        if c == 'identity_confirmed' and not metadata.get('identity_confirmed'):
            reasons.append('identity_not_confirmed')
        if c == 'not_high_privilege' and metadata.get('user_role') == 'admin':
            reasons.append('target_high_privilege')

    return (len(reasons) == 0), reasons

def execute_runbook(runbook_id_or_obj, ticket, inputs=None):
    if runbook_id_or_obj is None:
        raise ValueError("execute_runbook: no runbook specified (received None)")

    if isinstance(runbook_id_or_obj, str):
        runbook = RUNBOOKS.get(runbook_id_or_obj)
        if runbook is None:
            raise KeyError(f"execute_runbook: runbook id '{runbook_id_or_obj}' not found in RUNBOOKS.")
    elif isinstance(runbook_id_or_obj, dict):
        runbook = runbook_id_or_obj
    else:
        raise TypeError("execute_runbook: runbook must be either a runbook id (str) or a runbook dict.")

    if not isinstance(runbook, dict):
        raise TypeError("execute_runbook: resolved runbook is not a dict.")
    if 'steps' not in runbook or not isinstance(runbook['steps'], (list, tuple)):
        raise ValueError("execute_runbook: runbook must contain a 'steps' list.")

    results = []
    for s in runbook.get('steps', []):
        results.append({'step': s, 'status': 'skipped'})

    return results
