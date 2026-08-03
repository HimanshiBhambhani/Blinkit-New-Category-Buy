# Buy Smart MVP (Link B) + Trust API

Graduation project — **Discovery Engine (Link A)** finds trust friction; **Buy Smart (Link B)** surfaces deterministic trust scores from a dual corpus (CORPUS A friction + CORPUS B favorable supplement).

## Live demo links

| Link | URL |
|------|-----|
| **Link A** — Discovery Engine (Streamlit) | https://grad-project-2ublqkxwzyxtpeczjt8zxi.streamlit.app/ |
| **Link B** — Buy Smart UI (Vercel) | https://ai-native-mvp.vercel.app |
| **Link B** — Trust API (Render) | https://buy-smart-api.onrender.com |

## Repo layout

```
AI-Native-MVP/
├── backend/          # FastAPI trust API (Render)
├── frontend/         # Next.js Buy Smart UI (Vercel)
├── data/
│   ├── friction_corpus.csv      # CORPUS A (1,504 rows)
│   └── mvp_trust_corpus.csv     # CORPUS B (~210 rows)
├── scripts/
│   ├── build_mvp_corpus.py      # Rebuild CORPUS B
│   ├── prewarm-render.sh        # Wake Render before eval
│   └── verify-deploy.sh         # Post-deploy smoke tests
└── docs/                        # Deck, demo script, architecture
```

Link A (Streamlit) lives in the sibling **`Data-Extraction/`** folder at repo root (`app.py`).

## Local development

### API

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### UI

```bash
cd frontend
npm ci
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

Open http://localhost:3000

### Link A (Discovery Engine)

From repo root (`Data-Extraction/`):

```bash
streamlit run app.py
```

## Before an evaluation (Render cold start)

Render free tier sleeps after ~15 min. Pre-warm the API **2–3 minutes** before demo:

```bash
./scripts/prewarm-render.sh
# or with custom URL:
./scripts/prewarm-render.sh https://buy-smart-api.onrender.com
```

Full smoke test (API + UI + Streamlit):

```bash
./scripts/verify-deploy.sh \
  https://buy-smart-api.onrender.com \
  https://ai-native-mvp.vercel.app \
  https://grad-project-2ublqkxwzyxtpeczjt8zxi.streamlit.app
```

## Deploy notes

- **Streamlit Cloud** — deploy from `HimanshiBhambhani/Grad-Project` branch `main`, app path `Data-Extraction/app.py`
- **Render** — `render.yaml` at this folder root; rootDir `backend`
- **Vercel** — project root `frontend/`; set `NEXT_PUBLIC_API_URL` to Render URL

## Data

| Corpus | File | Role |
|--------|------|------|
| A | `data/friction_corpus.csv` | Friction / risk leg (Link A + Link B) |
| B | `data/mvp_trust_corpus.csv` | Favorable supplement (Link B only) |

Rebuild CORPUS B:

```bash
python scripts/build_mvp_corpus.py --max-positive 300 --min-rows 200
```

Never merge CORPUS B into Link A's Discovery CSV.
