[CmdletBinding()]
param(
    [string]$ApplicationName = "propertism-2026",
    [string]$EnvironmentName = "propertism-prod-2026",
    [string]$Region = "us-east-1",
    [string]$ExpectedVersionLabel = "",
    [int]$TimeoutMinutes = 15
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
$deadline = (Get-Date).AddMinutes($TimeoutMinutes)

do {
    $envResponse = & $aws elasticbeanstalk describe-environments `
        --application-name $ApplicationName `
        --environment-names $EnvironmentName `
        --region $Region `
        --output json | ConvertFrom-Json

    $environment = $envResponse.Environments[0]
    $statusLine = "{0} status={1} health={2} version={3}" -f (
        Get-Date -Format s
    ), $environment.Status, $environment.Health, $environment.VersionLabel

    Write-Output $statusLine

    $versionMatches = [string]::IsNullOrWhiteSpace($ExpectedVersionLabel) -or $environment.VersionLabel -eq $ExpectedVersionLabel
    if ($environment.Status -eq "Ready" -and $environment.Health -eq "Green" -and $versionMatches) {
        break
    }

    Start-Sleep -Seconds 15
} while ((Get-Date) -lt $deadline)

& $aws elasticbeanstalk describe-events `
    --environment-name $EnvironmentName `
    --region $Region `
    --max-items 10
