$ports = 8000,8001,8002
foreach ($p in $ports) {
    Write-Host "=== PORT $p ==="
    try {
        $h = Invoke-RestMethod -Uri "http://127.0.0.1:$p/health" -Method Get -TimeoutSec 5
        Write-Host "HEALTH:" ($h | ConvertTo-Json -Compress)
    } catch {
        Write-Host "HEALTH_ERROR:" $_.Exception.Message
    }

    try {
        $o = Invoke-RestMethod -Uri "http://127.0.0.1:$p/openapi.json" -Method Get -TimeoutSec 5
        Write-Host "OPENAPI KEYS:"
        $o.paths.Keys | ForEach-Object { Write-Host "  $_" }
    } catch {
        Write-Host "OPENAPI_ERROR:" $_.Exception.Message
    }

    try {
        $body = @{ topic='Math'; num_questions=1 } | ConvertTo-Json
        $r = Invoke-RestMethod -Uri "http://127.0.0.1:$p/api/mcq/generate" -Method Post -Body $body -ContentType 'application/json' -TimeoutSec 30
        Write-Host "MCQ_RESPONSE:" ($r | ConvertTo-Json -Compress)
    } catch {
        Write-Host "MCQ_ERROR:" $_.Exception.Message
    }

    Write-Host ""
}
