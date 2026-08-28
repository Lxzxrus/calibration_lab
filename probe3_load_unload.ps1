# probe3_load_unload.ps1
# Times a cold load and an unload for each of the nine roster models.
# Run LAST -- it thrashes VRAM and the page cache. No other GPU consumers.

$ErrorActionPreference = 'Stop'
$ProgressPreference    = 'SilentlyContinue'

$ChatUrl = 'http://127.0.0.1:11434/api/chat'
$PsUrl   = 'http://127.0.0.1:11434/api/ps'
$OutDir  = Join-Path (Get-Location) 'probe_out'
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir | Out-Null }

# Section 4 roster, smallest to largest.
$Models = @(
    'gemma3:1b-it-q4_K_M'
    'gemma3:1b-it-q8_0'
    'gemma3:1b-it-fp16'
    'gemma3:4b'
    'gemma3:4b-it-qat'
    'gemma3:4b-it-q8_0'
    'gemma3:4b-it-fp16'
    'gemma3:12b'
    'gemma3:12b-it-q8_0'
)

$PollMs = 25   # resolution floor on the unload measurement -- record it

function Invoke-Call {
    param([string]$Model, [string]$Prompt, [int]$NumPredict, [string]$KeepAlive)
    $body = @{
        model      = $Model
        messages   = @( @{ role = 'user'; content = $Prompt } )
        stream     = $false
        keep_alive = $KeepAlive
        options    = @{
            temperature = 0
            top_k       = 64
            top_p       = 0.95
            seed        = 42
            num_ctx     = 2048
            num_predict = $NumPredict
        }
    } | ConvertTo-Json -Depth 8

    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $r  = Invoke-RestMethod -Uri $ChatUrl -Method Post -Body $body -ContentType 'application/json'
    $sw.Stop()
    [pscustomobject]@{
        wall_ms  = $sw.Elapsed.TotalMilliseconds
        load_ms  = if ($r.load_duration)  { $r.load_duration / 1e6 }  else { 0 }
        total_ms = if ($r.total_duration) { $r.total_duration / 1e6 } else { 0 }
        eval_ms  = if ($r.eval_duration)  { $r.eval_duration / 1e6 }  else { 0 }
    }
}

function Test-Resident {
    param([string]$Model)
    try {
        $ps = Invoke-RestMethod -Uri $PsUrl -Method Get
        if (-not $ps.models) { return $false }
        return [bool]($ps.models | Where-Object { $_.name -eq $Model -or $_.model -eq $Model })
    } catch { return $false }
}

function Get-ResidentBytes {
    param([string]$Model)
    try {
        $ps = Invoke-RestMethod -Uri $PsUrl -Method Get
        $m  = $ps.models | Where-Object { $_.name -eq $Model -or $_.model -eq $Model }
        if ($m) { return $m.size_vram } else { return 0 }
    } catch { return 0 }
}

function Wait-Unloaded {
    param([string]$Model, [int]$TimeoutSec = 60)
    $sw    = [System.Diagnostics.Stopwatch]::StartNew()
    $polls = 0
    while ($sw.Elapsed.TotalSeconds -lt $TimeoutSec) {
        if (-not (Test-Resident -Model $Model)) { break }
        Start-Sleep -Milliseconds $PollMs
        $polls++
    }
    $sw.Stop()
    [pscustomobject]@{ ms = $sw.Elapsed.TotalMilliseconds; polls = $polls }
}

$Prompt = 'Question: What is the capital of Mongolia?

Answer: Ulaanbaatar

Is the Answer correct? Respond with only True or False.'

$rows = @()

foreach ($model in $Models) {

    Write-Host ""
    Write-Host "=== $model ===" -ForegroundColor Cyan

    # Ensure not resident before timing the load.
    if (Test-Resident -Model $model) {
        Write-Host "  already resident -- unloading first"
        Invoke-Call -Model $model -Prompt $Prompt -NumPredict 1 -KeepAlive '0' | Out-Null
        Wait-Unloaded -Model $model | Out-Null
        Start-Sleep -Seconds 1
    }

    # --- COLD LOAD ---
    Write-Host "  cold load..."
    $c = Invoke-Call -Model $model -Prompt $Prompt -NumPredict 1 -KeepAlive '10m'
    $vram = Get-ResidentBytes -Model $model

    # --- UNLOAD ---
    Write-Host "  unload..."
    $u0 = Invoke-Call -Model $model -Prompt $Prompt -NumPredict 1 -KeepAlive '0'
    $u  = Wait-Unloaded -Model $model

    $row = [pscustomobject]@{
        model                 = $model
        cold_load_ms_server   = [math]::Round($c.load_ms, 1)
        cold_call_wall_ms     = [math]::Round($c.wall_ms, 1)
        vram_mb               = [math]::Round($vram / 1MB, 0)
        unload_ms             = [math]::Round($u.ms, 1)
        unload_polls          = $u.polls
        unload_below_floor    = ($u.polls -eq 0)
        poll_interval_ms      = $PollMs
    }
    $rows += $row
    $row | Format-List | Out-String | Write-Host

    Start-Sleep -Seconds 2
}

$csv = Join-Path $OutDir 'probe3_load_unload.csv'
$rows | Export-Csv -Path $csv -NoTypeInformation

Write-Host ""
$rows | Format-Table -AutoSize
Write-Host ""
Write-Host ("Sum of nine cold loads: {0:N1} s" -f (($rows.cold_load_ms_server | Measure-Object -Sum).Sum / 1000)) -ForegroundColor Green
Write-Host ("Sum of nine unloads:    {0:N1} s" -f (($rows.unload_ms           | Measure-Object -Sum).Sum / 1000)) -ForegroundColor Green
Write-Host "rows -> $csv"
