# Blinkit Discovery Engine (Link A)

Streamlit dashboard for cross-shopping friction analysis — **1,504** classified public reviews (CORPUS A).

## Live demo — three links

| Link | URL |
|------|-----|
| **Link A** — Discovery Engine (this app) | https://grad-project-2ublqkxwzyxtpeczjt8zxi.streamlit.app/ |
| **Link B** — Buy Smart UI | https://ai-native-mvp.vercel.app |
| **Link B** — Trust API | https://buy-smart-api.onrender.com/api/health |

The sidebar in the running app also lists all three links.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

For scraping / pipeline (local or CI only):

```bash
pip install -r requirements-scrape.txt
python main.py
```

## Streamlit Cloud

- **Repo:** `HimanshiBhambhani/Grad-Project`
- **Branch:** `main`
- **Main file:** `app.py` (this directory)
- **Python:** 3.12 (see `.python-version`)

## Buy Smart MVP (Link B)

Implementation, API, and UI live in [`AI-Native-MVP/`](./AI-Native-MVP/README.md).

Before eval, pre-warm the Render API:

```bash
./AI-Native-MVP/scripts/prewarm-render.sh
```
