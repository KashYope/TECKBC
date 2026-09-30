"""Small HTTP renderer for the widgets used by this fictional-data demo.

Each request carries its own demo state; no process-local user state or
persistent server is needed. The Streamlit entry point remains available.
"""
import json
from contextlib import contextmanager
from html import escape


class Rerun(Exception):
    pass


class WebUI:
    def __init__(self, state, fields=None, clicked=None):
        self.session_state = state
        self.fields = fields or {}
        self.clicked = clicked
        self.parts = []
        self.title = "Kate"

    def set_page_config(self, page_title, **kwargs):
        self.title = page_title

    def markdown(self, body, unsafe_allow_html=False):
        self.parts.append(body if unsafe_allow_html else escape(body))

    def caption(self, body):
        self.parts.append(f'<p class="note">{escape(body)}</p>')

    @contextmanager
    def container(self, key=None):
        self.parts.append(f'<div class="st-key-{escape(key or "container")}">')
        yield
        self.parts.append('</div>')

    @contextmanager
    def expander(self, label, expanded=False):
        self.parts.append('<div data-testid="stExpander"><details'+(' open' if expanded else '')+f'><summary>{escape(label)}</summary>')
        yield
        self.parts.append('</details></div>')

    def columns(self, count):
        # CSS grid also keeps the original two-column option groups compact.
        return [self.column(count) for _ in range(count)]

    @contextmanager
    def column(self, count):
        self.parts.append(f'<div class="web-column" style="--columns:{count}">')
        yield
        self.parts.append('</div>')

    def button(self, label, key, on_click=None, args=(), type="secondary", **kwargs):
        self.parts.append(f'<button data-testid="stBaseButton-{escape(type)}" name="action" value="{escape(key)}">{escape(label)}</button>')
        if self.clicked == key:
            self.clicked = None
            if on_click:
                on_click(*args)
                raise Rerun()
            return True
        return False

    def selectbox(self, label, options, key):
        value = self.fields.get(key, self.session_state.get(key, options[0]))
        if value not in options:
            value = options[0]
        self.session_state[key] = value
        options_html = ''.join(f'<option value="{escape(option)}"'+(' selected' if option == value else '')+f'>{escape(option)}</option>' for option in options)
        self.parts.append(f'<label>{escape(label)}<select name="{escape(key)}" onchange="this.form.requestSubmit()">{options_html}</select></label>')
        return value

    def number_input(self, label, min_value=0, step=1, key=None, **kwargs):
        return self.numeric(label, key, min_value, 1_000_000_000, step, 'number')

    def slider(self, label, min_value, max_value, step, key):
        return self.numeric(label, key, min_value, max_value, step, 'range')

    def numeric(self, label, key, minimum, maximum, step, kind):
        try:
            value = int(self.fields.get(key, self.session_state.get(key, minimum)))
        except (ValueError, TypeError):
            value = minimum
        value = max(minimum, min(maximum, value))
        self.session_state[key] = value
        self.parts.append(f'<label>{escape(label)}<input type="{kind}" name="{escape(key)}" value="{value}" min="{minimum}" max="{maximum}" step="{step}"'+(' onchange="this.form.requestSubmit()"' if kind == 'range' else '')+f'></label>')
        return value

    def checkbox(self, label, key):
        value = self.session_state.get(key, False)
        if key + '_present' in self.fields:
            value = key in self.fields
        self.session_state[key] = value
        self.parts.append(f'<input type="hidden" name="{escape(key)}_present" value="1"><label><input type="checkbox" name="{escape(key)}" value="1"'+(' checked' if value else '')+f' onchange="this.form.requestSubmit()">{escape(label)}</label>')
        return value

    def rerun(self):
        raise Rerun()

    def render(self, main):
        for _ in range(4):
            self.parts = []
            try:
                main(self)
                break
            except Rerun:
                # Submitted fields have now been consumed. Reset must not reapply them.
                self.fields = {}
        else:
            raise RuntimeError('Demo exceeded its render limit')
        state = escape(json.dumps(self.session_state), quote=True)
        return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(self.title)}</title>
<style>
* {{ box-sizing: border-box; }}
body {{ margin:0; background:#e6e7eb; color:#16324f; font-family:Arial,sans-serif; }}
form {{ max-width:480px; margin:20px auto; padding:0 10px; }}
button, input, select {{ font:inherit; }}
button {{ width:100%; margin:4px 0; cursor:pointer; }}
label {{ display:block; font-size:13px; margin:8px 0; }}
input[type=number], select {{ display:block; width:100%; padding:8px; border:1px solid #cbdbe5; border-radius:8px; background:white; color:#16324f; }}
input[type=range] {{ width:100%; }}
summary {{ cursor:pointer; padding:12px; }}
details[open] {{ padding:0 12px 12px; }}
.web-column {{ display:inline-block; width:calc(100% / var(--columns)); vertical-align:top; padding:0 3px; }}
button:focus-visible, input:focus-visible, select:focus-visible, summary:focus-visible {{ outline:3px solid #0077b6; outline-offset:2px; }}
</style></head><body><form method="post"><input type="hidden" name="state" value="{state}">{''.join(self.parts)}</form></body></html>'''
