# TitleSpark AI — Live Deployment Starter

A Streamlit app for YouTube title ideas. It works without a key using demo templates, or with an OpenAI API key for real AI generation.

## Run locally on Windows

From this folder, open a terminal and run:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local URL printed in the terminal, normally `http://localhost:8501`.

## Publish free using Streamlit Community Cloud

1. Make a GitHub account at https://github.com/ if you don't already have one.
2. Create a new repository named `titlespark-ai`. For a public repository, do not put API keys or private information in the files.
3. Upload these project files to the repository root: `app.py`, `title_engine.py`, `requirements.txt`, `.gitignore`, `README.md`, and `.streamlit/config.toml`.
4. Open https://share.streamlit.io/ and sign in with GitHub.
5. Choose **Create app**, select your repository, branch (usually `main`), and main file path `app.py`.
6. Deploy. Wait for the build to finish, then open the URL provided by Streamlit.
7. Test the live app with several topics. Without an API key, it will work in demo/template mode.

## Turn on real AI (optional)

1. Create an API account at https://platform.openai.com/ and set up API billing if required. ChatGPT subscription billing and API billing are separate.
2. Create an API key in your provider dashboard.
3. In the Streamlit app management page, open **Settings / Secrets** (wording may vary).
4. Add this secret, replacing the placeholder with your own key:

```toml
OPENAI_API_KEY = "your-secret-api-key"
```

5. Save/reboot the app, then test title generation again.

Do not put the API key in `app.py`, GitHub, a screenshot, or a chat. Keep provider spending limits enabled. If a key is exposed, revoke it immediately.

## Important: MVP vs complete commercial SaaS

This project can be published online as a public MVP. It does **not** yet have:
- user signup/login,
- database and saved history,
- per-user quotas or abuse protection,
- subscription checkout/payment verification,
- privacy/terms pages or production monitoring.

Do not charge customers or collect sensitive user information until those features are implemented and tested. To become a commercial SaaS, the next stage is to add authentication, database access controls, rate limits, billing integration supported in your country, and production deployment/security checks.

## Costs

Streamlit Community Cloud has its own availability/usage policies that may change. The app can be tested without an AI API key. Real AI API calls may incur usage charges. A custom domain is optional and may cost extra.
