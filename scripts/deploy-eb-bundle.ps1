[CmdletBinding()]
param(
    [string]$VersionLabel = ("app-safe-" + (Get-Date -Format "yyMMdd-HHmmss")),
    [string]$BundlePath = "",
    [string]$ApplicationName = "propertism-2026",
    [string]$EnvironmentName = "propertism-prod-2026",
    [string]$Region = "us-east-1",
    [switch]$SkipCollectstatic
)

$ErrorActionPreference = "Stop"
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

function Get-AwsCommand {
    foreach ($candidate in @("aws", "aws.cmd", "aws.exe")) {
        $command = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($command) {
            return $command.Source
        }
    }

    foreach ($path in @(
        "C:\Program Files\Amazon\AWSCLIV2\aws.exe",
        "C:\Program Files (x86)\Amazon\AWSCLIV2\aws.exe"
    )) {
        if (Test-Path $path) {
            return $path
        }
    }

    throw "AWS CLI was not found on PATH or in the standard AWS CLI install locations."
}

$aws = Get-AwsCommand

if (-not $BundlePath) {
    $BundlePath = & (Join-Path $PSScriptRoot "build-eb-bundle.ps1") -VersionLabel $VersionLabel -SkipCollectstatic:$SkipCollectstatic
}

$identity = & $aws sts get-caller-identity --output json | ConvertFrom-Json
$bucket = "elasticbeanstalk-$Region-$($identity.Account)"
$key = "$ApplicationName/$VersionLabel.zip"

& $aws s3 cp $BundlePath "s3://$bucket/$key" --region $Region

& $aws elasticbeanstalk create-application-version `
    --application-name $ApplicationName `
    --version-label $VersionLabel `
    --source-bundle "S3Bucket=$bucket,S3Key=$key" `
    --process `
    --region $Region

& $aws elasticbeanstalk update-environment `
    --environment-name $EnvironmentName `
    --version-label $VersionLabel `
    --region $Region

Write-Output $VersionLabel
