param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$DjangoArgs
)

$pythonHome = "C:\Python"
$pythonExe = Join-Path $pythonHome "python.exe"
$pythonDllDir = Join-Path $pythonHome "django"

if (-not (Test-Path $pythonExe)) {
    throw "Expected Python interpreter was not found at $pythonExe."
}

if (-not (Test-Path $pythonDllDir)) {
    throw "Expected Python DLL directory was not found at $pythonDllDir."
}

if ($env:PATH -notlike "$pythonDllDir*") {
    $env:PATH = "$pythonDllDir;$env:PATH"
}

if (-not $DjangoArgs -or $DjangoArgs.Count -eq 0) {
    $DjangoArgs = @("check")
}

& $pythonExe "manage.py" @DjangoArgs
exit $LASTEXITCODE
