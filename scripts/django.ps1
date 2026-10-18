param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$DjangoArgs
)

$projectRoot = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$userPython = Join-Path $env:LOCALAPPDATA "Programs\Python\Python311\python.exe"
$legacyPython = "C:\Python\python.exe"

if (Test-Path $venvPython) {
    $pythonExe = $venvPython
} elseif (Test-Path $userPython) {
    $pythonExe = $userPython
} elseif (Test-Path $legacyPython) {
    $pythonExe = $legacyPython
    $legacyDll = "C:\Python\django"
    if ((Test-Path $legacyDll) -and ($env:PATH -notlike "*$legacyDll*")) {
        $env:PATH = "$legacyDll;$env:PATH"
    }
} else {
    $cmd = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($cmd) {
        $pythonExe = $cmd.Source
    } else {
        throw "No valid Python interpreter found. Looked in .venv, Python311, and C:\Python."
    }
}

if (-not $DjangoArgs -or $DjangoArgs.Count -eq 0) {
    $DjangoArgs = @("check")
}

& $pythonExe "manage.py" @DjangoArgs
exit $LASTEXITCODE
