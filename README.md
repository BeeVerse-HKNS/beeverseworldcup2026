# World Cup 2026 Predictor

5-Factor Prediction Model for FIFA World Cup 2026.

## Features

- Tournament simulation with knockout brackets
- 5-factor prediction formula (Elo, Market Value, X-Factor, Form, Squad Depth)
- Multi-language support (EN/ZH/ES/AR/FR)
- Interactive Streamlit dashboard
- Dark/Light theme toggle
- **Stadium Gold** color scheme - warm gray dark theme, green primary, gold accent

## Local Development

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Streamlit Cloud Deployment

This app is designed for deployment on Streamlit Cloud at https://beeverseworldcup2026.streamlit.app.

### Deployment Steps (To Configure on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "New app"
3. Fill in the details:
   - **Repository**: `BeeVerse-HKNS/beeverseworldcup2026`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
4. Click "Deploy!"

### Production URL

https://beeverseworldcup2026.streamlit.app

### Configuration

- **Repository**: https://github.com/BeeVerse-HKNS/beeverseworldcup2026

### Theme

The app uses a custom "Stadium Gold" color scheme:
- Dark theme: `#121212` (bg), `#1E1E1E` (card), `#4CAF50` (primary green), `#FFB300` (accent gold)
- Light theme: `#FAFAFA` (bg), `#FFFFFF` (card), `#2E7D32` (primary), `#F57F17` (accent)
