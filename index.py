"""Vercel Python entry point.

Streamlit stays in app.py and is started with `streamlit run app.py`.
This module only exposes the WSGI callable Vercel loads.
"""


def app(environ, start_response):
    body = b"TECKBC"
    start_response(
        "200 OK",
        [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Content-Length", str(len(body))),
        ],
    )
    return [body]
