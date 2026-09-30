# TECKBC

KBC confidence-aware personalisation prototype, using fictional customer data.

## Vercel

The Python entry point is `index:app`, configured in `pyproject.toml`.
It renders the Kate interface over ordinary HTTP, using the same UI and
financial engine as the local Streamlit demo. No Streamlit server needs to
run inside a Vercel Function.

Deploy the updated repository with the existing Vercel project. Keep the
project root at this directory and use the Python/Other framework preset;
no custom build command or output directory is needed.

## Local preview

```sh
python3 index.py
```

Open http://127.0.0.1:8000.

The original Streamlit preview is also available:

```sh
pip install -r requirements.txt
streamlit run app.py
```

The demo preserves state in the current page's form, across button presses
and customer switches. A fresh visit resets it. State is client-editable and
intended only for fictional prototype data; it is not an authenticated bank
session. Customer data is never written back to disk. What-if values remain
separate from confirmed context.

## Regression checks

```sh
python3 -m unittest discover -s tests
```
