[CmdletBinding()]
param(
    [string]$EnvironmentName = "propertism-prod",
    [string]$Region = "us-west-2",
    [string[]]$AllowedHosts = @(
        "propertism.in",
        "www.propertism.in",
        ".elasticbeanstalk.com"
    ),
    [string[]]$CsrfTrustedOrigins = @(
        "https://propertism.in",
        "https://www.propertism.in",
        "https://*.elasticbeanstalk.com"
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
$optionSettings = @(
    @{
        Namespace = "aws:elasticbeanstalk:application:environment"
        OptionName = "DEBUG"
        Value = "False"
    },
    @{
        Namespace = "aws:elasticbeanstalk:application:environment"
        OptionName = "DJANGO_ALLOWED_HOSTS"
        Value = ($AllowedHosts -join ",")
    },
    @{
        Namespace = "aws:elasticbeanstalk:application:environment"
        OptionName = "CSRF_TRUSTED_ORIGINS"
        Value = ($CsrfTrustedOrigins -join ",")
    }
) | ConvertTo-Json -Compress

& $aws elasticbeanstalk update-environment `
    --environment-name $EnvironmentName `
    --region $Region `
    --option-settings $optionSettings | Out-Null

& $aws elasticbeanstalk describe-configuration-settings `
    --application-name "propertism" `
    --environment-name $EnvironmentName `
    --region $Region `
    --query "ConfigurationSettings[0].OptionSettings[?Namespace=='aws:elasticbeanstalk:application:environment' && (OptionName=='DEBUG' || OptionName=='DJANGO_ALLOWED_HOSTS' || OptionName=='CSRF_TRUSTED_ORIGINS')].[OptionName,Value]"
