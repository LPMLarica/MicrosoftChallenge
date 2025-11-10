"""Streamlit entry for Service Central - Free HF edition"""
import streamlit as st
from agents.intake_agent import IntakeAgent
from agents.triage_agent import TriageAgent
from agents.runbook_agent import RunbookAgent
from agents.human_agent import HumanAgent
from services.vector_knowledge import VectorKnowledge
from dataclasses import asdict
import json

st.set_page_config(page_title='Service Central', layout='wide')

if 'store' not in st.session_state:
    st.session_state['store'] = {}

if 'knowledge' not in st.session_state:
    k = VectorKnowledge(); k.load_synthetic(); st.session_state['knowledge'] = k

if 'agents' not in st.session_state:
    st.session_state['agents'] = {
        'intake': IntakeAgent('IntakeAgent', st.session_state['knowledge']),
        'triage': TriageAgent('TriageAgent', st.session_state['knowledge']),
        'runbook_id': RunbookAgent('RunbookAgent', st.session_state['knowledge']),
        'human': HumanAgent('HumanAgent', st.session_state['knowledge'])
    }

st.sidebar.title('Service Central — Free HF')
view = st.sidebar.radio('View', ['New Ticket', 'Ticket Queue', 'Agent View', 'Admin'])

if view == 'New Ticket':
    st.header('Open a new ticket')
    with st.form('ticket_form'):
        name = st.text_input('Your name', value='Example User')
        subject = st.text_input('Subject', value='Password issue')
        description = st.text_area('Description', value='I cannot access my email. Please reset my password.')
        identity_confirmed = st.checkbox('Identity confirmed?')
        role = st.selectbox('Role', ['employee','manager','admin'])
        submitted = st.form_submit_button('Open ticket')
    if submitted:
        intake = st.session_state['agents']['intake']
        ticket = intake.process(name, subject, description, channel='web')
        ticket.metadata['identity_confirmed'] = identity_confirmed
        ticket.metadata['user_role'] = role
        st.session_state['store'][ticket.ticket_id] = ticket
        st.success(f'Ticket created: {ticket.ticket_id}')

elif view == 'Ticket Queue':
    st.header('Ticket queue')
    for tid, ticket in list(st.session_state['store'].items()):
        with st.expander(f"{tid} - {ticket.subject} - {ticket.user_display}"):
            st.write(ticket.description)
            col1, col2, col3 = st.columns(3)
            if col1.button('Automatic triage', key=f'triage-{tid}'):
                triage = st.session_state['agents']['triage']
                decision = triage.triage(ticket)
                st.json(decision)
            if col2.button('Execute suggested runbook', key=f'run-{tid}'):
                triage = st.session_state['agents']['triage']
                decision = triage.triage(ticket)
                if decision.get('suggested_runbook'):
                    rb = st.session_state['agents']['runbook_id']
                    res = rb.consider_and_run(ticket, decision['suggested_runbook'], auto_approve=True)
                    st.json(res)
                else:
                    st.warning('No runbook suggested')
            if col3.button('Escalate to human', key=f'escalate-{tid}'):
                human = st.session_state['agents']['human']
                human.handle(ticket, 'Escalated for human review')
                st.success('Escalated')
            st.markdown('**Trace**')
            st.json([s for s in ticket.steps])
            st.markdown('**Runbook executions**')
            st.json(ticket.runbook_executions)

elif view == 'Agent View':
    st.header('Agent dashboard')
    ids = list(st.session_state['store'].keys())
    sel = st.selectbox('Select ticket', ['- none -'] + ids)
    if sel and sel != '- none -':
        t = st.session_state['store'][sel]
        st.subheader(t.subject)
        st.write(t.description)
        if st.button('Execute reset_password', key=f'exec-{sel}'):
            rb = st.session_state['agents']['runbook_id']
            res = rb.consider_and_run(t, 'reset_password')
            st.json(res)
        note = st.text_area('Add note')
        if st.button('Send note and close', key=f'close-{sel}'):
            human = st.session_state['agents']['human']
            human.handle(t, note)
            t.status = 'closed'
            st.success('Closed')

elif view == 'Admin':
    st.header('Admin')
    st.download_button('Export tickets JSON', data=json.dumps({k:v.__dict__ for k,v in st.session_state['store'].items()}, default=str), file_name='tickets.json')
