# probe1_per_call_overhead.ps1
# Measures the gap between client wall-clock and server-side reported duration.
# Run from the calibration_lab repo root. No other GPU consumers.

$ErrorActionPreference = 'Stop'
$ProgressPreference    = 'SilentlyContinue'   # PS progress bar adds real latency to web cmdlets

$Url    = 'http://127.0.0.1:11434/api/chat'
$OutDir = Join-Path (Get-Location) 'probe_out'
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir | Out-Null }

# 20 hand-written Q/A pairs. NOT drawn from TriviaQA -- the draw pool stays clean.
# Distinct questions on purpose: identical prompts would hit Ollama's prompt cache
# and collapse prompt_eval_count, which is the opposite of the sweep's behaviour.
$Pairs = @(
    @{ q = 'What is the capital of Mongolia?';                  a = 'Ulaanbaatar' }
    @{ q = 'Which planet has the shortest day?';                a = 'Jupiter' }
    @{ q = 'What is the chemical symbol for tungsten?';         a = 'W' }
    @{ q = 'Who composed The Rite of Spring?';                  a = 'Igor Stravinsky' }
    @{ q = 'What is the largest island in the Mediterranean?';  a = 'Sicily' }
    @{ q = 'In what year did the Berlin Wall fall?';            a = '1989' }
    @{ q = 'What is the deepest lake in the world?';            a = 'Lake Baikal' }
    @{ q = 'Which element has atomic number 79?';               a = 'Gold' }
    @{ q = 'What is the currency of Poland?';                   a = 'Zloty' }
    @{ q = 'Who wrote The Left Hand of Darkness?';              a = 'Ursula K. Le Guin' }
    @{ q = 'What is the tallest mountain in Africa?';           a = 'Kilimanjaro' }
    @{ q = 'Which sea separates Italy and Albania?';            a = 'Adriatic Sea' }
    @{ q = 'What is the smallest bone in the human body?';      a = 'Stapes' }
    @{ q = 'Who painted The Garden of Earthly Delights?';       a = 'Hieronymus Bosch' }
    @{ q = 'What is the capital of Kazakhstan?';                a = 'Astana' }
    @{ q = "Which gas makes up most of Earth's atmosphere?";    a = 'Nitrogen' }
    @{ q = 'What is the longest river in Asia?';                a = 'Yangtze' }
    @{ q = 'Who discovered penicillin?';                        a = 'Alexander Fleming' }
    @{ q = 'What is the hardest naturally occurring mineral?';  a = 'Diamond' }
    @{ q = 'Which country has the most time zones?';            a = 'France' }
)

function New-TemplateB {
    param([string]$Question, [string]$Answer)
    "Question: $Question`n`nAnswer: $Answer`n`nIs the Answer correct? Respond with only True or False."
}

function Invoke-Probe {
    param(
        [string]$Model,
        [string]$Prompt,
        [int]$NumPredict,
        [switch]$Logprobs,
        [string]$KeepAlive = '10m'
    )
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
    }
    if ($Logprobs) {
        $body.logprobs     = $true
        $body.top_logprobs = 10
    }
    $json = $body | ConvertTo-Json -Depth 8

    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $r  = Invoke-RestMethod -Uri $Url -Method Post -Body $json -ContentType 'application/json'
    $sw.Stop()

    $total  = if ($r.total_duration)        { $r.total_duration / 1e6 }        else { 0 }
    $load   = if ($r.load_duration)         { $r.load_duration / 1e6 }         else { 0 }
    $peval  = if ($r.prompt_eval_duration)  { $r.prompt_eval_duration / 1e6 }  else { 0 }
    $eval   = if ($r.eval_duration)         { $r.eval_duration / 1e6 }         else { 0 }
    $ptok   = if ($r.prompt_eval_count)     { $r.prompt_eval_count }           else { 0 }
    $etok   = if ($r.eval_count)            { $r.eval_count }                  else { 0 }

    [pscustomobject]@{
        model          = $Model
        wall_ms        = [math]::Round($sw.Elapsed.TotalMilliseconds, 2)
        total_ms       = [math]::Round($total, 2)
        load_ms        = [math]::Round($load, 2)
        prompt_eval_ms = [math]::Round($peval, 2)
        eval_ms        = [math]::Round($eval, 2)
        prompt_tokens  = $ptok
        eval_tokens    = $etok
        client_ms      = [math]::Round($sw.Elapsed.TotalMilliseconds - $total, 2)
        server_slack_ms= [math]::Round($total - ($load + $peval + $eval), 2)
        done           = $r.done
        done_reason    = $r.done_reason
        response       = ($r.message.content -replace '\s+', ' ').Trim()
    }
}

function Get-Stats {
    param([double[]]$Values, [string]$Label)
    $s = @($Values | Sort-Object)
    $n = $s.Count
    if ($n % 2 -eq 1) { $median = $s[[int](($n - 1) / 2)] }
    else              { $median = ($s[[int]($n / 2) - 1] + $s[[int]($n / 2)]) / 2 }
    [pscustomobject]@{
        metric = $Label
        n      = $n
        mean   = [math]::Round(($Values | Measure-Object -Average).Average, 2)
        median = [math]::Round($median, 2)
        min    = [math]::Round($s[0], 2)
        max    = [math]::Round($s[-1], 2)
    }
}

$Models = @('gemma3:12b-it-q8_0', 'gemma3:1b-it-q4_K_M')
$All    = @()

foreach ($model in $Models) {

    Write-Host ""
    Write-Host "=== $model ===" -ForegroundColor Cyan

    # Model warm-up (his cold != warm rule) AND client warm-up (.NET JIT + HttpClient init).
    # Both discarded.
    Write-Host "  priming (3 discarded calls, includes cold load)..."
    for ($i = 0; $i -lt 3; $i++) {
        $p = New-TemplateB -Question $Pairs[$i].q -Answer $Pairs[$i].a
        Invoke-Probe -Model $model -Prompt $p -NumPredict 5 -Logprobs | Out-Null
    }

    Write-Host "  measuring 20 calls..."
    $rows = @()
    for ($i = 0; $i -lt 20; $i++) {
        $p = New-TemplateB -Question $Pairs[$i].q -Answer $Pairs[$i].a
        $rows += Invoke-Probe -Model $model -Prompt $p -NumPredict 5 -Logprobs
    }

    $tag = ($model -replace '[:\\/]', '_')
    $csv = Join-Path $OutDir "probe1_$tag.csv"
    $rows | Export-Csv -Path $csv -NoTypeInformation
    Write-Host "  rows -> $csv"

    Write-Host ""
    @(
        Get-Stats -Values ($rows.wall_ms)         -Label 'wall_ms'
        Get-Stats -Values ($rows.total_ms)        -Label 'total_ms (server)'
        Get-Stats -Values ($rows.client_ms)       -Label 'client_ms (wall - total)'
        Get-Stats -Values ($rows.server_slack_ms) -Label 'server_slack_ms'
        Get-Stats -Values ($rows.load_ms)         -Label 'load_ms (warm)'
        Get-Stats -Values ($rows.prompt_eval_ms)  -Label 'prompt_eval_ms'
        Get-Stats -Values ($rows.eval_ms)         -Label 'eval_ms'
        Get-Stats -Values ([double[]]$rows.prompt_tokens) -Label 'prompt_tokens'
        Get-Stats -Values ([double[]]$rows.eval_tokens)   -Label 'eval_tokens'
    ) | Format-Table -AutoSize

    $All += $rows

    # release VRAM before the next model
    $p = New-TemplateB -Question $Pairs[0].q -Answer $Pairs[0].a
    Invoke-Probe -Model $model -Prompt $p -NumPredict 5 -KeepAlive '0' | Out-Null
    Start-Sleep -Seconds 2
}

$All | Export-Csv -Path (Join-Path $OutDir 'probe1_all.csv') -NoTypeInformation
Write-Host ""
Write-Host "Done. Combined CSV: $(Join-Path $OutDir 'probe1_all.csv')" -ForegroundColor Green
