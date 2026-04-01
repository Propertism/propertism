[CmdletBinding()]
param(
    [string]$VersionLabel = ("app-safe-" + (Get-Date -Format "yyMMdd-HHmmss")),
    [string]$OutputDir = "",
    [switch]$SkipCollectstatic
)

$ErrorActionPreference = "Stop"

function Get-PythonCommand {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) {
        return @{ Command = $python.Source; Arguments = @() }
    }

    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($py) {
        return @{ Command = $py.Source; Arguments = @("-3") }
    }

    throw "Python was not found on PATH."
}

function Test-ExcludedPath {
    param(
        [string]$RelativePath
    )

    $normalized = $RelativePath -replace "\\", "/"
    $segments = $normalized.Split("/", [System.StringSplitOptions]::RemoveEmptyEntries)

    $excludedDirectories = @(
        ".git",
        ".elasticbeanstalk",
        ".archive",
        ".kiro",
        ".seed",
        ".session-tracker",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "node_modules",
        "documents",
        "logs",
        "tests",
        "dist",
        "build",
        "staticfiles"
    )

    foreach ($segment in $segments[0..([Math]::Max(0, $segments.Length - 2))]) {
        if ($excludedDirectories -contains $segment) {
            return $true
        }
    }

    $leaf = $segments[-1]
    if ($leaf -in @(".env", "db.sqlite3", "db.sqlite3-journal")) {
        return $true
    }

    if ($leaf.EndsWith(".pyc") -or $leaf.EndsWith(".pyo") -or $leaf.EndsWith(".zip")) {
        return $true
    }

    return $false
}

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$distRoot = if ($OutputDir) {
    if ([System.IO.Path]::IsPathRooted($OutputDir)) {
        [System.IO.Path]::GetFullPath($OutputDir)
    }
    else {
        [System.IO.Path]::GetFullPath((Join-Path $projectRoot $OutputDir))
    }
} else {
    [System.IO.Path]::Combine($projectRoot, "dist")
}

New-Item -ItemType Directory -Force -Path $distRoot | Out-Null

Push-Location $projectRoot
try {
    if (-not $SkipCollectstatic) {
        $python = Get-PythonCommand
        $previousDebug = $env:DEBUG
        try {
            $env:DEBUG = "False"
            & $python.Command @($python.Arguments + @("manage.py", "collectstatic", "--noinput", "--clear"))
        }
        finally {
            if ($null -eq $previousDebug) {
                Remove-Item Env:DEBUG -ErrorAction SilentlyContinue
            }
            else {
                $env:DEBUG = $previousDebug
            }
        }
    }

    $bundlePath = Join-Path $distRoot ($VersionLabel + ".zip")
    if (Test-Path $bundlePath) {
        Remove-Item $bundlePath -Force
    }

    Add-Type -AssemblyName System.IO.Compression
    Add-Type -AssemblyName System.IO.Compression.FileSystem

    $baseUri = [System.Uri]::new(($projectRoot.TrimEnd("\") + "\"))
    $fileStream = [System.IO.File]::Open($bundlePath, [System.IO.FileMode]::CreateNew)
    $archive = [System.IO.Compression.ZipArchive]::new($fileStream, [System.IO.Compression.ZipArchiveMode]::Create, $false)

    try {
        $files = Get-ChildItem -LiteralPath $projectRoot -Recurse -Force -File | Where-Object {
            $relative = [System.Uri]::UnescapeDataString($baseUri.MakeRelativeUri([System.Uri]::new($_.FullName)).ToString())
            -not (Test-ExcludedPath -RelativePath $relative)
        }

        foreach ($file in $files) {
            $relative = [System.Uri]::UnescapeDataString($baseUri.MakeRelativeUri([System.Uri]::new($file.FullName)).ToString())
            [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
                $archive,
                $file.FullName,
                $relative,
                [System.IO.Compression.CompressionLevel]::Optimal
            ) | Out-Null
        }
    }
    finally {
        $archive.Dispose()
        $fileStream.Dispose()
    }

    Write-Output $bundlePath
}
finally {
    Pop-Location
}
