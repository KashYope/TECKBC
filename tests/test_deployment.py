"""Exercise the actual WSGI entry point across independent requests."""
import io
import json
import unittest
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urlencode

from index import app


class StateParser(HTMLParser):
    state = None

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'input' and values.get('name') == 'state':
            self.state = json.loads(values['value'])


def request(state=None, action=None, **fields):
    if state is not None:
        fields['state'] = json.dumps(state)
    if action:
        fields['action'] = action
    payload = urlencode(fields).encode()
    response = []
    body = b''.join(app({
        'REQUEST_METHOD': 'POST' if fields else 'GET',
        'CONTENT_LENGTH': str(len(payload)),
        'wsgi.input': io.BytesIO(payload),
    }, lambda status, headers: response.append((status, dict(headers))))).decode()
    parser = StateParser()
    parser.feed(body)
    return response[0], unescape(body), parser.state


class DeploymentTests(unittest.TestCase):
    def test_home_is_interface_not_placeholder(self):
        (status, headers), body, state = request()
        self.assertEqual(status, '200 OK')
        self.assertIn('text/html', headers['Content-Type'])
        self.assertIn('Explore savings goals', body)
        self.assertEqual(state['demo_customer'], 'Emma')

    def test_customer_navigation_and_goal_survive_requests(self):
        _, _, state = request()
        _, _, state = request(state, 'emma_explore')
        _, body, state = request(state, 'emma_set_goal')
        self.assertIn("doesn't create a product", body)
        _, _, state = request(state, demo_customer='Lucas')
        _, body, state = request(state, demo_customer='Emma')
        self.assertTrue(state['profiles']['Emma']['savings_goal'])
        _, body, state = request(state, 'nav_MY CONTEXT')
        self.assertIn('✓ Created a savings goal', body)

    def test_manual_context_and_simulation_stay_separate(self):
        _, _, state = request(demo_customer='Lucas')
        _, _, state = request(state, 'transfer_Savings')
        _, _, state = request(state, 'choose_manual')
        _, body, state = request(state, 'update_context', Lucas_ext_income='3000', Lucas_ext_expenses='1000', Lucas_ext_savings='20000')
        self.assertIn('€1,870', body)
        manual = state['profiles']['Lucas']['manual'].copy()
        _, _, state = request(state, 'nav_WHAT IF?')
        _, body, state = request(state, Lucas_whatif_savings='40000', Lucas_whatif_only_present='1', Lucas_whatif_only='1')
        self.assertIn('€55,000', body)
        self.assertEqual(state['profiles']['Lucas']['manual'], manual)
        _, body, state = request(state, 'reset_demo')
        self.assertIsNone(state['profiles']['Lucas']['manual'])
        self.assertIn('What is this transfer mainly for?', body)

    def test_simulated_connection(self):
        _, _, state = request(demo_customer='Lucas')
        for action in ('transfer_Investment', 'choose_connect', 'simulate_connection'):
            _, body, state = request(state, action)
        self.assertIn('€25,000', body)
        self.assertEqual(state['profiles']['Lucas']['simulated_savings'], 25000)

    def test_every_customer_and_view_renders(self):
        for customer in ('Emma', 'Lucas', 'Sophie'):
            _, _, state = request(demo_customer=customer)
            for view in ('MY CONTEXT', 'WHAT IF?', 'WHY?', 'KATE'):
                (status, _), body, state = request(state, 'nav_' + view)
                self.assertEqual(status, '200 OK', (customer, view))
                self.assertIn('Hackathon prototype', body)

    def test_malformed_state_is_rejected(self):
        for state in ([], {'profiles': []}, {'profiles': {'Lucas': {'manual': {}}}}, {'view': '<script>'}):
            (status, _), _, _ = request(state)
            self.assertEqual(status, '400 Bad Request')


if __name__ == '__main__':
    unittest.main()
