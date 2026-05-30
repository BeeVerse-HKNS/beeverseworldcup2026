# Cloudflare Tunnel 永久固定 URL 設置腳本

Write-Host "=== World Cup 2026 - Cloudflare Tunnel 設置 ===" -ForegroundColor Green

# 檢查 cloudflared 是否已安裝
Write-Host "`n[1/5] 檢查 cloudflared..." -ForegroundColor Yellow
try {
    $version = cloudflared --version
    Write-Host "✅ cloudflared 已安裝: $version" -ForegroundColor Green
} catch {
    Write-Host "❌ cloudflared 未安裝，請先運行: winget install cloudflare.cloudflared" -ForegroundColor Red
    exit 1
}

# 檢查登錄狀態
Write-Host "`n[2/5] 檢查 Cloudflare 登錄狀態..." -ForegroundColor Yellow
$certPath = "$env:USERPROFILE\.cloudflared\cert.pem"
if (Test-Path $certPath) {
    Write-Host "✅ 已登錄 Cloudflare" -ForegroundColor Green
} else {
    Write-Host "⚠️ 未登錄，請在瀏覽器中完成登錄..." -ForegroundColor Yellow
    cloudflared tunnel login
}

# 創建 Tunnel
Write-Host "`n[3/5] 創建 Named Tunnel..." -ForegroundColor Yellow
$tunnelName = "wc2026-predictor"
try {
    $tunnelId = cloudflared tunnel create $tunnelName 2>&1
    if ($tunnelId -match "Created tunnel") {
        Write-Host "✅ Tunnel 創建成功: $tunnelName" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Tunnel 可能已存在，繼續..." -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ Tunnel 創建失敗，嘗試使用現有 Tunnel..." -ForegroundColor Yellow
}

# 列出所有 Tunnel
Write-Host "`n[4/5] 列出所有 Tunnel..." -ForegroundColor Yellow
cloudflared tunnel list

# 創建配置文件
Write-Host "`n[5/5] 創建配置文件..." -ForegroundColor Yellow
$configDir = "$env:USERPROFILE\.cloudflared"
$configPath = "$configDir\config.yml"

$configContent = @"
tunnel: $tunnelName
credentials-file: $configDir\$tunnelName.json

ingress:
  - hostname: wc2026-predictor.trycloudflare.com
    service: http://localhost:8502
  - service: http_status:404
"@

$configContent | Out-File -FilePath $configPath -Encoding UTF8
Write-Host "✅ 配置文件已創建: $configPath" -ForegroundColor Green

Write-Host "`n=== 設置完成 ===" -ForegroundColor Green
Write-Host "啟動 Tunnel: cloudflared tunnel run $tunnelName" -ForegroundColor Cyan
Write-Host "或使用快速模式: cloudflared tunnel --url http://localhost:8502" -ForegroundColor Cyan
