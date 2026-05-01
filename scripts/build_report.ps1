param(
    [string]$OutputName = "MS0240-CA3-Wages-Regression-Report.pdf"
)

$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$ReportDir = Join-Path $ProjectRoot "report"
$BuildDir = Join-Path $ProjectRoot ".dist\latex-build"
$SubmissionDir = Join-Path $ProjectRoot ".dist\submission"

New-Item -ItemType Directory -Force -Path $BuildDir | Out-Null
New-Item -ItemType Directory -Force -Path $SubmissionDir | Out-Null

Push-Location $ReportDir
try {
    latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$BuildDir" main.tex
}
finally {
    Pop-Location
}

$BuiltPdf = Join-Path $BuildDir "main.pdf"
if (-not (Test-Path -LiteralPath $BuiltPdf)) {
    throw "Expected report PDF was not generated: $BuiltPdf"
}

Copy-Item -LiteralPath $BuiltPdf -Destination (Join-Path $SubmissionDir $OutputName) -Force
Write-Host "Report built: $(Join-Path $SubmissionDir $OutputName)"
