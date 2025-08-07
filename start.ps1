# StreamBlur Pro - Avvio Automatico
# Esegui questo script per avviare tutto

Write-Host "🚀 Avvio StreamBlur Pro..." -ForegroundColor Green

# Avvia server Python in background
Write-Host "📦 Avvio server Python..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\chris\Documents\StreamBlur-Pro\StreamBlur-Python-Core'; .\streamblur_env\Scripts\python.exe streamblur_server.py"

# Aspetta un momento per il server
Start-Sleep -Seconds 3

# Avvia app Tauri
Write-Host "🎨 Avvio app Tauri..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\chris\Documents\StreamBlur-Pro\streamblur-pro'; npm run tauri dev"

Write-Host "✅ StreamBlur Pro avviato!" -ForegroundColor Green
Write-Host "📱 App: http://localhost:1420" -ForegroundColor Cyan
Write-Host "🔗 API: http://127.0.0.1:8080" -ForegroundColor Cyan
Write-Host "🎥 Ora puoi usare la Virtual Camera in OBS!" -ForegroundColor Magenta
