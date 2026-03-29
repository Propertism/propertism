# DNS Configuration Guide for Propertism.in

**Domain**: propertism.in  
**Registrar**: GoDaddy  
**Target**: AWS Elastic Beanstalk (propertism-prod)  
**Date**: March 7, 2026

---

## Overview

This guide will help you configure DNS records in GoDaddy to point your custom domain `propertism.in` to your AWS Elastic Beanstalk application.

---

## Step 1: Access GoDaddy DNS Management

1. Log in to your GoDaddy account at https://www.godaddy.com
2. Go to **My Products** → **Domains**
3. Find `propertism.in` and click **DNS** or **Manage DNS**

---

## Step 2: Configure DNS Records

You need to add **3 DNS records** total:

### Record 1: Root Domain A Record (Primary)

```
Type:     A
Name:     @
Value:    35.167.25.188
TTL:      600 seconds (10 minutes)
```

**What this does**: Points your root domain (propertism.in) to the primary AWS IP address.

### Record 2: Root Domain A Record (Secondary)

```
Type:     A
Name:     @
Value:    44.242.56.49
TTL:      600 seconds (10 minutes)
```

**What this does**: Provides redundancy by pointing to a secondary AWS IP address.

### Record 3: WWW Subdomain CNAME

```
Type:     CNAME
Name:     www
Value:    propertism-prod.eba-rzpshqvp.us-west-2.elasticbeanstalk.com
TTL:      3600 seconds (1 hour)
```

**What this does**: Points www.propertism.in to your Elastic Beanstalk environment.

---

## Step 3: Remove Conflicting Records (If Any)

Before adding the new records, check if there are any existing records that might conflict:

- **Remove** any existing A records for `@` (root domain)
- **Remove** any existing CNAME records for `www`
- **Keep** any MX records (for email) if you have email configured
- **Keep** any TXT records (for domain verification)

---

## Step 4: Add the Records in GoDaddy

### Adding A Records:

1. Click **Add** or **Add Record**
2. Select **Type**: A
3. Enter **Name**: @ (this represents the root domain)
4. Enter **Value**: 35.167.25.188
5. Set **TTL**: 600 seconds
6. Click **Save**
7. Repeat for the second A record with IP: 44.242.56.49

### Adding CNAME Record:

1. Click **Add** or **Add Record**
2. Select **Type**: CNAME
3. Enter **Name**: www
4. Enter **Value**: propertism-prod.eba-rzpshqvp.us-west-2.elasticbeanstalk.com
5. Set **TTL**: 3600 seconds
6. Click **Save**

---

## Step 5: Verify DNS Configuration

After adding the records, your DNS management page should show:

| Type  | Name | Value                                                      | TTL  |
|-------|------|------------------------------------------------------------|------|
| A     | @    | 35.167.25.188                                              | 600  |
| A     | @    | 44.242.56.49                                               | 600  |
| CNAME | www  | propertism-prod.eba-rzpshqvp.us-west-2.elasticbeanstalk.com | 3600 |

---

## Step 6: Wait for DNS Propagation

DNS changes take time to propagate across the internet:

- **Minimum**: 10 minutes (based on TTL)
- **Typical**: 1-4 hours
- **Maximum**: 24-48 hours (rare)

### Check DNS Propagation:

You can check if DNS has propagated using these tools:

1. **Online Tools**:
   - https://www.whatsmydns.net/#A/propertism.in
   - https://dnschecker.org/#A/propertism.in

2. **Command Line** (Windows PowerShell):
   ```powershell
   nslookup propertism.in
   nslookup www.propertism.in
   ```

3. **Expected Results**:
   - `propertism.in` should resolve to 35.167.25.188 or 44.242.56.49
   - `www.propertism.in` should resolve to the Elastic Beanstalk CNAME

---

## Step 7: Test Your Domain

Once DNS has propagated, test these URLs in your browser:

1. **Root Domain**: http://propertism.in/en/
2. **WWW Subdomain**: http://www.propertism.in/en/
3. **Admin Panel**: http://propertism.in/en/admin/

**Note**: These will be HTTP (not HTTPS) until you set up SSL certificates in the next step.

---

## Troubleshooting

### Issue: "This site can't be reached" or "DNS_PROBE_FINISHED_NXDOMAIN"

**Solution**: DNS hasn't propagated yet. Wait longer and try again.

### Issue: "Connection timed out"

**Solution**: 
1. Check that you entered the IP addresses correctly
2. Verify the Elastic Beanstalk environment is running (Health: Green)
3. Check AWS security groups allow HTTP traffic on port 80

### Issue: WWW subdomain not working

**Solution**:
1. Verify the CNAME record value doesn't have "http://" or trailing "/"
2. Make sure you entered the full Elastic Beanstalk domain name
3. Wait for DNS propagation

### Issue: Root domain works but WWW doesn't (or vice versa)

**Solution**: This is normal during DNS propagation. Different records can propagate at different speeds.

---

## Next Steps After DNS Configuration

Once your domain is working on HTTP:

### 1. Set Up SSL Certificate (HTTPS)

1. Go to AWS Certificate Manager (ACM) in us-west-2 region
2. Request a public certificate for:
   - `propertism.in`
   - `www.propertism.in`
3. Choose DNS validation
4. Add the CNAME records provided by ACM to GoDaddy
5. Wait for certificate validation (5-30 minutes)
6. Configure Elastic Beanstalk load balancer to use the certificate
7. Enable HTTP to HTTPS redirect

### 2. Update Django Settings

The Django application is already configured to accept your custom domain:
- `ALLOWED_HOSTS` includes: `propertism.in`, `www.propertism.in`

### 3. Test Everything

After SSL is configured, test:
- https://propertism.in/en/
- https://www.propertism.in/en/
- https://propertism.in/en/admin/

---

## Summary Checklist

- [ ] Log in to GoDaddy DNS management
- [ ] Remove any conflicting A or CNAME records
- [ ] Add A record: @ → 35.167.25.188 (TTL: 600)
- [ ] Add A record: @ → 44.242.56.49 (TTL: 600)
- [ ] Add CNAME record: www → propertism-prod.eba-rzpshqvp.us-west-2.elasticbeanstalk.com (TTL: 3600)
- [ ] Save all changes
- [ ] Wait for DNS propagation (1-4 hours typically)
- [ ] Test http://propertism.in/en/
- [ ] Test http://www.propertism.in/en/
- [ ] Proceed to SSL certificate setup

---

## Support Information

**AWS Environment**: propertism-prod  
**Region**: us-west-2 (Oregon)  
**Elastic Beanstalk CNAME**: propertism-prod.eba-rzpshqvp.us-west-2.elasticbeanstalk.com  
**Current Working URL**: http://propertism-prod.eba-rzpshqvp.us-west-2.elasticbeanstalk.com/en/

---

## GoDaddy AI Agent (Airo) Prompt

If you prefer to use GoDaddy's AI assistant, copy and paste this prompt:

```
I need to configure DNS for my domain propertism.in to point to my AWS Elastic Beanstalk application.

Please set up these DNS records:

1. Root domain (@):
   - Type: A Record
   - Name: @
   - Value: 35.167.25.188
   - TTL: 600 seconds

2. Root domain (secondary):
   - Type: A Record
   - Name: @
   - Value: 44.242.56.49
   - TTL: 600 seconds

3. WWW subdomain:
   - Type: CNAME
   - Name: www
   - Value: propertism-prod.eba-rzpshqvp.us-west-2.elasticbeanstalk.com
   - TTL: 3600 seconds

Please remove any existing conflicting A or CNAME records for @ and www before adding these new records.

Confirm when the records are active.
```

---

**Document Version**: 1.0  
**Last Updated**: March 7, 2026  
**Status**: Ready for DNS configuration
