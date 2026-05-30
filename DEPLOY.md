# World Cup 2026 Predictor - Deployment Configuration

## Deployment Options

### Option 1: Railway (Recommended - Fixed URL)

1. **Push to GitHub**
   ```bash
   cd d:\My_Code_Projects\Harnessing\projects\world-2026
   git init
   git add .
   git commit -m "World Cup 2026 Predictor - Initial deployment"
   git remote add origin https://github.com/YOUR_USERNAME/worldcup-2026-predictor.git
   git push -u origin main
   ```

2. **Deploy to Railway**
   - Visit https://railway.app
   - Login with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect Streamlit and deploy

3. **Get Fixed URL**
   - Railway provides: `https://worldcup-2026-predictor.up.railway.app`
   - Or connect your custom domain

### Option 2: Render (Free Tier)

1. **Push to GitHub** (same as above)

2. **Deploy to Render**
   - Visit https://render.com
   - Login with GitHub
   - Click "New" → "Web Service"
   - Connect your GitHub repo
   - Settings:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`

3. **Get URL**: `https://your-app.onrender.com`

### Option 3: Streamlit Cloud (Simplest)

1. **Push to GitHub** (same as above)

2. **Deploy to Streamlit Cloud**
   - Visit https://share.streamlit.io
   - Login with GitHub
   - Click "New app"
   - Select repo, branch, and main file path

3. **Get URL**: `https://username-appname.streamlit.app`

## File Structure

```
world-2026/
├── streamlit_app.py      # Main Streamlit app
├── formula_v9_ultimate.py # Core prediction engine
├── tournament_model.py    # Tournament simulation
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── railway.toml          # Railway deployment config
```

## Environment Variables (if needed)

- `PORT` - Auto-set by hosting platform
- `DATABASE_PATH` - Path to player data (default: `data/wc2026_player_database.json`)

## Troubleshooting

### Common Issues

1. **Missing data file**: Ensure `data/wc2026_player_database.json` is in the repo
2. **Port error**: Ensure `--server.port $PORT` is used
3. **Memory error**: Reduce sample size or use smaller datasets

### Health Check

After deployment, visit:
- `/` - Main page
- `/health` - Health check (if implemented)
