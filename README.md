# Health Companion

Health Companion is a Streamlit app for quick health assessments, AI analysis, and local report storage.

Live app: https://health-companion-2y86pmwck7b3pdsqserbyf.streamlit.app/

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your API key to a local `.env` file:

```env
GEMINI_API_KEY=your_key_here
```

## Run

```bash
streamlit run app.py
```

## Notes

- `.env` is ignored by git so secrets stay local.
- Reports are stored in the `reports/` folder.
