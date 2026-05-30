@echo off
echo === World Cup 2026 - Cloudflare Tunnel 快速啟動 ===
echo.
echo [1] 啟動臨時 Tunnel（每次 URL 會改變）
echo [2] 啟動永久 Tunnel（需要先運行 setup-cloudflare-tunnel.ps1）
echo.
set /p choice="請選擇 (1/2): "

if "%choice%"=="1" (
    echo.
    echo 啟動臨時 Tunnel...
    cloudflared tunnel --url http://localhost:8502
) else if "%choice%"=="2" (
    echo.
    echo 啟動永久 Tunnel...
    cloudflared tunnel run wc2026-predictor
) else (
    echo 無效選擇
)
