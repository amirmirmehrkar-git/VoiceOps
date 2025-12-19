# PowerShell Script to Update PR #1 Description
# Usage: .\scripts\update_pr_description.ps1 -Token "YOUR_GITHUB_TOKEN"

param(
    [Parameter(Mandatory=$true)]
    [string]$Token
)

$repo = "amirmirmehrkar-git/VoiceOps"
$prNumber = 1

# Read PR body from file
$prBodyPath = Join-Path $PSScriptRoot "..\PR_BODY_FINAL.md"
if (Test-Path $prBodyPath) {
    $body = Get-Content $prBodyPath -Raw
} else {
    Write-Host "❌ Error: PR_BODY_FINAL.md not found!" -ForegroundColor Red
    exit 1
}

# Prepare headers
$headers = @{
    "Authorization" = "Bearer $Token"
    "Accept" = "application/vnd.github.v3+json"
    "Content-Type" = "application/json"
}

# Prepare JSON body
$jsonBody = @{
    body = $body
} | ConvertTo-Json

# Update PR
try {
    Write-Host "🔄 Updating PR #$prNumber description..." -ForegroundColor Yellow
    
    $response = Invoke-RestMethod `
        -Uri "https://api.github.com/repos/$repo/pulls/$prNumber" `
        -Method PATCH `
        -Headers $headers `
        -Body $jsonBody
    
    Write-Host "✅ PR description updated successfully!" -ForegroundColor Green
    Write-Host "📝 PR URL: $($response.html_url)" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ Error updating PR:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response: $responseBody" -ForegroundColor Red
    }
    
    exit 1
}

