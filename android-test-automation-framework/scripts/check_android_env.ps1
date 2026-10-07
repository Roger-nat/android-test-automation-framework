Write-Host "=== Android environment check ===" -ForegroundColor Cyan

$commands = @("python", "adb", "node", "appium")

foreach ($command in $commands) {
    if (Get-Command $command -ErrorAction SilentlyContinue) {
        Write-Host "[OK] $command" -ForegroundColor Green
    } else {
        Write-Host "[MISSING] $command" -ForegroundColor Red
    }
}

Write-Host "`nConnected Android devices:" -ForegroundColor Cyan
adb devices

Write-Host "`nAppium UiAutomator2 driver:" -ForegroundColor Cyan
appium driver list --installed

Write-Host "`nEnvironment check complete." -ForegroundColor Cyan
