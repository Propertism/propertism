# SSL/HTTPS Setup Guide for propertism.in

## Current Status
- ✅ Site working on HTTP: http://propertism.in
- ⚠️ No HTTPS certificate configured
- 🎯 Goal: Enable HTTPS with automatic HTTP→HTTPS redirect

---

## Step 1: Request SSL Certificate in AWS Certificate Manager

### 1.1 Open AWS Certificate Manager
1. Go to AWS Console: https://console.aws.amazon.com/
2. Search for "Certificate Manager" or go directly to:
   https://us-west-2.console.aws.amazon.com/acm/home?region=us-west-2
3. Make sure you're in **us-west-2 (Oregon)** region (same as your EB environment)

### 1.2 Request Certificate
1. Click **"Request a certificate"**
2. Choose **"Request a public certificate"**
3. Click **"Next"**

### 1.3 Add Domain Names
Add both domains:
```
propertism.in
www.propertism.in
```

Or use wildcard (recommended):
```
propertism.in
*.propertism.in
```

### 1.4 Choose Validation Method
- Select **"DNS validation"** (recommended)
- Click **"Request"**

### 1.5 DNS Validation Records
AWS will provide CNAME records to add to GoDaddy:

**Example format:**
```
Name: _abc123def456.propertism.in
Type: CNAME
Value: _xyz789ghi012.acm-validations.aws.
```

---

## Step 2: Add DNS Validation Records to GoDaddy

### 2.1 Copy the CNAME Records
From AWS Certificate Manager, copy:
- CNAME Name
- CNAME Value

### 2.2 Add to GoDaddy DNS
1. Log in to GoDaddy: https://dcc.godaddy.com/
2. Go to: My Products → Domains → propertism.in → Manage DNS
3. Click **"Add"** button
4. Select **"CNAME"** record type
5. Add the validation records:
   - **Name**: (the part before .propertism.in from AWS)
   - **Value**: (the full CNAME value from AWS)
   - **TTL**: 600 seconds

### 2.3 Wait for Validation
- Validation usually takes 5-30 minutes
- AWS will automatically detect the DNS records
- Certificate status will change from "Pending validation" to "Issued"

---

## Step 3: Configure HTTPS Listener in Elastic Beanstalk

### 3.1 Open Elastic Beanstalk Console
1. Go to: https://us-west-2.console.aws.amazon.com/elasticbeanstalk/home?region=us-west-2
2. Click on **"propertism-prod"** environment

### 3.2 Configure Load Balancer
1. In left sidebar, click **"Configuration"**
2. Find **"Load balancer"** category
3. Click **"Edit"**

### 3.3 Add HTTPS Listener
1. Scroll to **"Listeners"** section
2. Click **"Add listener"**
3. Configure:
   - **Port**: 443
   - **Protocol**: HTTPS
   - **SSL certificate**: Select your certificate (propertism.in)
4. Click **"Add"**

### 3.4 Configure HTTP Listener (Optional - for redirect)
1. Find the existing HTTP listener (port 80)
2. You can either:
   - **Option A**: Keep it as-is (allows both HTTP and HTTPS)
   - **Option B**: Configure redirect (forces HTTPS)

For redirect:
- Edit port 80 listener
- Change to redirect to port 443

### 3.5 Save Configuration
1. Click **"Apply"** at bottom
2. Wait for environment update (2-3 minutes)

---

## Step 4: Enable HTTPS Settings in Django

Once HTTPS is working, update Django settings to enforce HTTPS:

### 4.1 Uncomment HTTPS Settings
In `realtor-web/realtor_project/settings.py`, uncomment these lines:

```python
if not DEBUG:
    SECURE_SSL_REDIRECT = True  # Enable this
    SESSION_COOKIE_SECURE = True  # Enable this
    CSRF_COOKIE_SECURE = True  # Enable this
    SECURE_HSTS_SECONDS = 31536000  # Enable this
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Enable this
    SECURE_HSTS_PRELOAD = True  # Enable this
```

### 4.2 Deploy Changes
```bash
cd realtor-web
git add -A
git commit -m "Enable HTTPS security settings"
eb deploy propertism-prod
```

---

## Step 5: Verify HTTPS is Working

### 5.1 Test URLs
1. **HTTPS**: https://propertism.in/ (should work with green padlock)
2. **HTTPS WWW**: https://www.propertism.in/ (should work)
3. **HTTP Redirect**: http://propertism.in/ (should redirect to HTTPS)

### 5.2 Check Certificate
1. Click the padlock icon in browser
2. Verify certificate is valid
3. Check it's issued by Amazon

### 5.3 Test Admin Panel
- https://propertism.in/admin/ (should work securely)

---

## Troubleshooting

### Certificate Validation Stuck
- **Issue**: Certificate stays in "Pending validation"
- **Solution**: 
  - Verify CNAME records are correct in GoDaddy
  - Wait up to 30 minutes
  - Check DNS propagation: https://dnschecker.org/

### HTTPS Not Working After Setup
- **Issue**: Site doesn't load on HTTPS
- **Solution**:
  - Verify listener is on port 443
  - Check security group allows port 443
  - Verify certificate is "Issued" status

### Mixed Content Warnings
- **Issue**: Some resources load over HTTP
- **Solution**:
  - Check all static files use relative URLs
  - Verify STATIC_URL doesn't have http://
  - Check external resources (fonts, CDNs) use HTTPS

### Redirect Loop
- **Issue**: Page keeps redirecting
- **Solution**:
  - Verify `SECURE_PROXY_SSL_HEADER` is set correctly
  - Check load balancer is forwarding X-Forwarded-Proto header

---

## Current DNS Configuration

Your current GoDaddy DNS records:
```
Type: A
Name: @
Value: 35.167.25.188
TTL: 600

Type: A
Name: @
Value: 44.242.56.49
TTL: 600

Type: CNAME
Name: www
Value: propertism-prod.eba-rzpshqvp.us-west-2.elasticbeanstalk.com
TTL: 3600
```

After SSL setup, you'll add:
```
Type: CNAME
Name: _abc123def456 (from AWS)
Value: _xyz789ghi012.acm-validations.aws. (from AWS)
TTL: 600
```

---

## Summary Checklist

- [ ] Request SSL certificate in AWS Certificate Manager
- [ ] Add DNS validation CNAME records to GoDaddy
- [ ] Wait for certificate to be issued (5-30 minutes)
- [ ] Add HTTPS listener (port 443) in Elastic Beanstalk
- [ ] Test https://propertism.in/ works
- [ ] Enable HTTPS settings in Django settings.py
- [ ] Deploy Django changes
- [ ] Verify HTTP redirects to HTTPS
- [ ] Test admin panel on HTTPS

---

## Need Help?

If you encounter any issues:
1. Check AWS Certificate Manager for certificate status
2. Verify DNS records in GoDaddy
3. Check Elastic Beanstalk environment health
4. Review application logs: `eb logs`

---

**Estimated Total Time**: 30-60 minutes (mostly waiting for DNS validation)

**Next Step**: Go to AWS Certificate Manager and request the certificate!
