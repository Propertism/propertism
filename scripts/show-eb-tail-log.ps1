[CmdletBinding()]
param(
    [string]$EnvironmentName = "propertism-prod",
    [string]$Region = "us-west-2",
    [string[]]$Patterns = @(
        "bootstrap_admin_content",
        "container_command",
        "Traceback",
        "error",
        "activate",
        "python manage.py"
    )
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
$info = & $aws elasticbeanstalk retrieve-environment-info `
    --environment-name $EnvironmentName `
    --info-type tail `
    --region $Region `
    --output json | ConvertFrom-Json

$url = $info.EnvironmentInfo[0].Message
if (-not $url) {
    throw "No tail-log URL was returned."
}

$log = curl.exe -s $url
$log | Select-String -Pattern $Patterns -Context 2,4
