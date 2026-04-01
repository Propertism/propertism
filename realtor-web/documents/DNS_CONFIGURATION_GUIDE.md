# DNS Configuration Guide for `propertism.in`

**Domain**: `propertism.in`  
**Registrar**: GoDaddy  
**App**: AWS Elastic Beanstalk (`propertism-prod`)  
**Last Updated**: April 1, 2026

## Important

Do **not** point the apex/root domain `@` at old hard-coded Elastic Beanstalk IPs.

Elastic Beanstalk sits behind AWS-managed infrastructure, and those IPs are not a stable long-term contract for your root domain. If GoDaddy still has old parking, forwarding, or stale A records for `@`, users can intermittently land on the wrong page before the browser reaches `www.propertism.in`.

## Recommended Setup

Use `www` as the canonical public hostname:

- `www.propertism.in` -> `CNAME` -> `propertism-prod.eba-rzpshqvp.us-west-2.elasticbeanstalk.com`
- `propertism.in` -> permanent redirect/forward -> `https://www.propertism.in`

The Django app already enforces the canonical redirect once the request reaches the application.

## GoDaddy Records

### Keep

```text
Type:  CNAME
Name:  www
Value: propertism-prod.eba-rzpshqvp.us-west-2.elasticbeanstalk.com
TTL:   1 hour
```

### Remove conflicting root-domain records

Remove any conflicting records for `@` such as:

- old `A` records pointing to AWS IPs
- GoDaddy parking defaults
- any duplicate root forwarding entries

Keep unrelated MX/TXT/email verification records.

## Root Domain Fix Options

### Option 1: GoDaddy Forwarding

If DNS stays on GoDaddy, set the root domain to a **301 permanent redirect**:

```text
Forward: propertism.in -> https://www.propertism.in
Type: Permanent (301)
Masking: Off
```

Use this when you want the simplest fix and `www` is your canonical hostname.

### Option 2: Move DNS To Route 53 Or Cloudflare

If you want the cleanest long-term setup for both `@` and `www`, move authoritative DNS to a provider that supports apex aliasing/flattening.

Then configure:

- `@` -> alias/flattening -> your AWS load balancer / target
- `www` -> CNAME/alias -> the same application target

This is the more robust setup if you want AWS-native DNS management.

## Why the first visit can hit GoDaddy

If a user sees GoDaddy only on the first visit to `propertism.in`, but `www.propertism.in` works:

1. the browser is hitting the naked domain first
2. GoDaddy/root DNS is answering before the request ever reaches Django
3. after `www` loads once, browser cache/HSTS/redirect memory can make later visits seem correct

That means this symptom is almost always **DNS or registrar forwarding**, not an app-template issue.

## Quick Verification Checklist

After updating GoDaddy:

1. Open a fresh private/incognito window.
2. Visit `http://propertism.in`.
3. Confirm it lands on `https://www.propertism.in/`.
4. Visit `https://www.propertism.in/` directly.
5. Confirm there is no GoDaddy landing page in either case.

## Current App Behavior

The app redirects alternate public hosts to `www.propertism.in` in:

- [content/middleware.py](/d:/viji/viji-olivine/03rolledout/01propertism/realtor-web/content/middleware.py)

That redirect only helps **after** DNS sends the request to the app.
