[CmdletBinding()]
param(
    [string]$EnvironmentName = "propertism-prod",
    [string]$Region = "us-west-2",
    [string]$CertificateArn = "arn:aws:acm:us-west-2:977916686136:certificate/7d12638f-6d78-4f16-8e82-08695f4b891c",
    [string]$SslPolicy = "ELBSecurityPolicy-TLS13-1-2-2021-06"
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

$certificate = & $aws acm describe-certificate `
    --certificate-arn $CertificateArn `
    --region $Region `
    --output json | ConvertFrom-Json

$certificateStatus = $certificate.Certificate.Status
if ($certificateStatus -ne "ISSUED") {
    throw "Certificate $CertificateArn is $certificateStatus. Complete DNS validation before enabling HTTPS."
}

$environmentResources = & $aws elasticbeanstalk describe-environment-resources `
    --environment-name $EnvironmentName `
    --region $Region `
    --output json | ConvertFrom-Json

$loadBalancerName = $environmentResources.EnvironmentResources.LoadBalancers[0].Name
if (-not $loadBalancerName) {
    throw "Could not resolve the Elastic Beanstalk load balancer for environment $EnvironmentName."
}

$loadBalancer = & $aws elbv2 describe-load-balancers `
    --names $loadBalancerName `
    --region $Region `
    --output json | ConvertFrom-Json

$loadBalancerArn = $loadBalancer.LoadBalancers[0].LoadBalancerArn
$listeners = & $aws elbv2 describe-listeners `
    --load-balancer-arn $loadBalancerArn `
    --region $Region `
    --output json | ConvertFrom-Json

$httpListener = $listeners.Listeners | Where-Object { $_.Port -eq 80 } | Select-Object -First 1
if (-not $httpListener) {
    throw "The load balancer does not have an HTTP:80 listener."
}

$httpsListener = $listeners.Listeners | Where-Object { $_.Port -eq 443 } | Select-Object -First 1
$targetGroupArn = @(
    $listeners.Listeners |
        ForEach-Object { $_.DefaultActions } |
        Where-Object { $_.Type -eq "forward" } |
        Select-Object -ExpandProperty TargetGroupArn -First 1
)[0]

if (-not $targetGroupArn) {
    throw "Could not determine the default target group for the load balancer."
}

$forwardActions = @(
    @{
        Type = "forward"
        TargetGroupArn = $targetGroupArn
    }
) | ConvertTo-Json -Compress

$redirectActions = @(
    @{
        Type = "redirect"
        RedirectConfig = @{
            Protocol = "HTTPS"
            Port = "443"
            Host = "#{host}"
            Path = "/#{path}"
            Query = "#{query}"
            StatusCode = "HTTP_301"
        }
    }
) | ConvertTo-Json -Compress

if ($httpsListener) {
    & $aws elbv2 modify-listener `
        --listener-arn $httpsListener.ListenerArn `
        --certificates "CertificateArn=$CertificateArn" `
        --ssl-policy $SslPolicy `
        --default-actions $forwardActions `
        --region $Region | Out-Null
}
else {
    $created = & $aws elbv2 create-listener `
        --load-balancer-arn $loadBalancerArn `
        --protocol HTTPS `
        --port 443 `
        --certificates "CertificateArn=$CertificateArn" `
        --ssl-policy $SslPolicy `
        --default-actions $forwardActions `
        --region $Region `
        --output json | ConvertFrom-Json

    $httpsListener = $created.Listeners[0]
}

& $aws elbv2 modify-listener `
    --listener-arn $httpListener.ListenerArn `
    --default-actions $redirectActions `
    --region $Region | Out-Null

$finalListeners = & $aws elbv2 describe-listeners `
    --load-balancer-arn $loadBalancerArn `
    --region $Region `
    --output json | ConvertFrom-Json

[ordered]@{
    EnvironmentName = $EnvironmentName
    LoadBalancerArn = $loadBalancerArn
    CertificateArn = $CertificateArn
    CertificateStatus = $certificateStatus
    Listeners = $finalListeners.Listeners | Select-Object Port, Protocol, ListenerArn, DefaultActions
} | ConvertTo-Json -Depth 10
