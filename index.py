"""Vercel WSGI entry point for the interactive Kate demo."""
import json
from urllib.parse import parse_qs

from app import main
from web_ui import WebUI

MAX_BODY = 32_768


def read_state(raw):
    """Only accept the state shape produced by the fictional demo."""
    state = json.loads(raw)
    if not isinstance(state, dict):
        raise ValueError('Invalid demo state')
    if state.get('view', 'KATE') not in ('KATE', 'MY CONTEXT', 'WHAT IF?', 'WHY?'):
        raise ValueError('Invalid view')
    for key in ('demo_customer', 'active_customer'):
        if key in state and state[key] not in ('Emma', 'Lucas', 'Sophie'):
            raise ValueError('Invalid customer')
    profiles = state.get('profiles', {})
    if not isinstance(profiles, dict):
        raise ValueError('Invalid profiles')
    for name, profile in profiles.items():
        if name not in ('Emma', 'Lucas', 'Sophie') or not isinstance(profile, dict):
            raise ValueError('Invalid profile')
        manual = profile.get('manual')
        if manual is not None:
            if not isinstance(manual, dict) or set(manual) != {'external_income', 'external_expenses', 'external_savings'}:
                raise ValueError('Invalid manual context')
            if any(type(v) not in (int, float) or not 0 <= v <= 1_000_000_000 for v in manual.values()):
                raise ValueError('Invalid amount')
        simulated = profile.get('simulated_savings')
        if simulated is not None and (type(simulated) not in (int, float) or not 0 <= simulated <= 1_000_000_000):
            raise ValueError('Invalid savings')
        for key in ('transfer_purpose', 'context_choice', 'emma_stage'):
            if profile.get(key) is not None and not isinstance(profile[key], str):
                raise ValueError('Invalid choice')
    return state


def app(environ, start_response):
    method = environ.get('REQUEST_METHOD', 'GET')
    if method not in ('GET', 'HEAD', 'POST'):
        start_response('405 Method Not Allowed', [('Allow', 'GET, HEAD, POST')])
        return [b'']
    try:
        length = int(environ.get('CONTENT_LENGTH') or 0)
        if not 0 <= length <= MAX_BODY:
            start_response('413 Content Too Large', [('Content-Type', 'text/plain')])
            return [b'Request too large']
        fields = {}
        if method == 'POST':
            fields = {key: values[-1] for key, values in parse_qs(environ['wsgi.input'].read(length).decode('utf-8'), keep_blank_values=True).items()}
        state = read_state(fields.pop('state', '{}'))
        body = WebUI(state, fields, fields.pop('action', None)).render(main).encode('utf-8')
    except (ValueError, TypeError, KeyError):
        start_response('400 Bad Request', [('Content-Type', 'text/plain; charset=utf-8')])
        return [b'Invalid demo input. Reload the page to reset.']
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'), ('Content-Length', str(len(body))), ('Cache-Control', 'no-store'), ('X-Content-Type-Options', 'nosniff')])
    return [b'' if method == 'HEAD' else body]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    with make_server('127.0.0.1', 8000, app) as server:
        print('Kate demo: http://127.0.0.1:8000', flush=True)
        server.serve_forever()
