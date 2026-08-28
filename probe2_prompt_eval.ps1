# probe2_prompt_eval.ps1
# Measures prompt-processing cost for Templates A, B and C on the slowest cell.
# Also settles whether gemma3 splits digits (5c item 12) for free, via eval_count on C.
# Run from the calibration_lab repo root. No other GPU consumers.

$ErrorActionPreference = 'Stop'
$ProgressPreference    = 'SilentlyContinue'

$Url    = 'http://127.0.0.1:11434/api/chat'
$Model  = 'gemma3:12b-it-q8_0'
$OutDir = Join-Path (Get-Location) 'probe_out'
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir | Out-Null }

# Same hand-written pairs as probe 1. Not TriviaQA items.
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
)

# Templates transcribed verbatim from prereg section 6, so the measured
# prompt_eval_count is the sweep's actual number, not an approximation.
function New-TemplateA {
    param([string]$Question)
    "$Question Answer with only the answer, no explanation, in 10 words or fewer. If unsure, give your single best guess."
}
function New-TemplateB {
    param([string]$Question, [string]$Answer)
    "Question: $Question`n`nAnswer: $Answer`n`nIs the Answer correct? Respond with only True or False."
}
function New-TemplateC {
    param([string]$Question, [string]$Answer)
    "Question: $Question`n`nAnswer: $Answer`n`nHow confident are you that the answer is correct? Respond with any integer between 0 and 100 where 0 is not confident and 100 is certain that the answer is correct. Respond with only that integer and nothing else."
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

    $total = if ($r.total_duration)       { $r.total_duration / 1e6 }       else { 0 }
    $load  = if ($r.load_duration)        { $r.load_duration / 1e6 }        else { 0 }
    $peval = if ($r.prompt_eval_duration) { $r.prompt_eval_duration / 1e6 } else { 0 }
    $eval  = if ($r.eval_duration)        { $r.eval_duration / 1e6 }        else { 0 }
    $ptok  = if ($r.prompt_eval_count)    { $r.prompt_eval_count }          else { 0 }
    $etok  = if ($r.eval_count)           { $r.eval_count }                 else { 0 }

    [pscustomobject]@{
        wall_ms         = [math]::Round($sw.Elapsed.TotalMilliseconds, 2)
        total_ms        = [math]::Round($total, 2)
        load_ms         = [math]::Round($load, 2)
        prompt_eval_ms  = [math]::Round($peval, 2)
        eval_ms         = [math]::Round($eval, 2)
        prompt_tokens   = $ptok
        eval_tokens     = $etok
        client_ms       = [math]::Round($sw.Elapsed.TotalMilliseconds - $total, 2)
        done            = $r.done
        done_reason     = $r.done_reason
        response        = ($r.message.content -replace '\s+', ' ').Trim()
    }
}

Write-Host "=== $Model : prompt-eval by template ===" -ForegroundColor Cyan
Write-Host "  priming (3 discarded calls, includes cold load)..."
for ($i = 0; $i -lt 3; $i++) {
    Invoke-Probe -Model $Model -Prompt (New-TemplateB $Pairs[$i].q $Pairs[$i].a) -NumPredict 5 -Logprobs | Out-Null
}

$rows = @()

foreach ($t in @('A', 'B', 'C')) {
    Write-Host "  Template $t ..."
    for ($i = 0; $i -lt $Pairs.Count; $i++) {
        switch ($t) {
            'A' { $prompt = New-TemplateA $Pairs[$i].q;                 $np = 25; $lp = $false }
            'B' { $prompt = New-TemplateB $Pairs[$i].q $Pairs[$i].a;    $np = 5;  $lp = $true  }
            'C' { $prompt = New-TemplateC $Pairs[$i].q $Pairs[$i].a;    $np = 10; $lp = $false }
        }
        if ($lp) { $row = Invoke-Probe -Model $Model -Prompt $prompt -NumPredict $np -Logprobs }
        else     { $row = Invoke-Probe -Model $Model -Prompt $prompt -NumPredict $np }
        $row | Add-Member -NotePropertyName template -NotePropertyValue $t
        $rows += $row
    }
}

$csv = Join-Path $OutDir 'probe2_prompt_eval.csv'
$rows | Export-Csv -Path $csv -NoTypeInformation
Write-Host "  rows -> $csv"

Write-Host ""
$rows | Group-Object template | ForEach-Object {
    $g = $_.Group
    [pscustomobject]@{
        template          = $_.Name
        n                 = $g.Count
        mean_prompt_tok   = [math]::Round(($g.prompt_tokens  | Measure-Object -Average).Average, 1)
        mean_prompt_ms    = [math]::Round(($g.prompt_eval_ms | Measure-Object -Average).Average, 2)
        mean_eval_tok     = [math]::Round(($g.eval_tokens    | Measure-Object -Average).Average, 1)
        mean_eval_ms      = [math]::Round(($g.eval_ms        | Measure-Object -Average).Average, 2)
        mean_client_ms    = [math]::Round(($g.client_ms      | Measure-Object -Average).Average, 2)
        mean_wall_ms      = [math]::Round(($g.wall_ms        | Measure-Object -Average).Average, 2)
    }
} | Format-Table -AutoSize

Write-Host "Template C responses and eval_count (digit-splitting check):" -ForegroundColor Yellow
$rows | Where-Object { $_.template -eq 'C' } |
    Select-Object response, eval_tokens, done_reason | Format-Table -AutoSize

# Per-item total across all three templates on this cell
$perItem = ($rows.wall_ms | Measure-Object -Sum).Sum / $Pairs.Count
Write-Host ("Mean wall-clock for one item's full A+B+C on {0}: {1} ms" -f $Model, [math]::Round($perItem, 1)) -ForegroundColor Green

# release VRAM
Invoke-Probe -Model $Model -Prompt (New-TemplateB $Pairs[0].q $Pairs[0].a) -NumPredict 5 -KeepAlive '0' | Out-Null
Write-Host "Done." -ForegroundColor Green
