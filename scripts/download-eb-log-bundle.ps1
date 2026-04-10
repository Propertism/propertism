[CmdletBinding()]
param(
    [string]$EnvironmentName = "propertism-prod-2026",
    [string]$Region = "us-east-1",
    [string]$OutputPath = ".\dist\eb-log-bundle.zip"
)

$ErrorActionPreference = "Stop"

function Get-AwsCommand {
    foreach ($candidate in @("aws", "aws.cmd", "aws.exe")) {
        $command = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($command) {
            return $command.Source
        }
    }

    foreach ($candidate in @("aws", "aws.cmd", "aws.exe")) {
        $resolved = @(where.exe $candidate 2>$null | Select-Object -First 1)
        if ($resolved) {
            return $resolved[0].Trim()
        }
    }

    throw "AWS CLI was not found on PATH."
}

$aws = Get-AwsCommand
& $aws elasticbeanstalk request-environment-info `
    --environment-name $EnvironmentName `
    --info-type bundle `
    --region $Region | Out-Null

Start-Sleep -Seconds 20

$info = & $aws elasticbeanstalk retrieve-environment-info `
    --environment-name $EnvironmentName `
    --info-type bundle `
    --region $Region `
    --output json | ConvertFrom-Json

$url = $info.EnvironmentInfo[0].Message
if (-not $url) {
    throw "No bundle-log URL was returned."
}

$resolvedOutput = [System.IO.Path]::GetFullPath($OutputPath)
$outputDir = Split-Path -Parent $resolvedOutput
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
curl.exe -L -o $resolvedOutput $url | Out-Null

Write-Output $resolvedOutput
