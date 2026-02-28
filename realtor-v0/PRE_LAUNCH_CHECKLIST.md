# Pre-Launch Checklist

**Project**: Propertism Realty Advisors LLP  
**SCCB**: SCCB-47 Compliance  
**Date**: February 25, 2026

---

## Critical Items (Must Complete Before Launch)

### 🔴 Security

- [ ] DEBUG=False in production
- [ ] SECRET_KEY moved to environment variable
- [ ] ALLOWED_HOSTS configured with production domain
- [ ] HTTPS enforced (SSL certificate active)
- [ ] Security headers enabled (HSTS, XSS, Content-Type)
- [ ] Admin URL changed from /admin/
- [ ] Strong passwords for all accounts
- [ ] Database not publicly accessible
- [ ] Firewall configured (if using VPS)
- [ ] No secrets in Git repository

### 🔴 Infrastructure

- [ ] Hosting platform selected and configured
- [ ] Domain name purchased and configured
- [ ] DNS records pointing to server
- [ ] SSL certificate installed and verified
- [ ] Email service configured (SendGrid/Mailgun)
- [ ] Database set up (PostgreSQL or SQLite)
- [ ] Static files collected and serving
- [ ] Media files directory configured
- [ ] Backup system configured

### 🔴 Application

- [ ] All migrations applied
- [ ] Superuser account created
- [ ] Company information added in admin
- [ ] At least 3 sample properties added
- [ ] Hero image uploaded and optimized
- [ ] Team member information added
- [ ] Contact form tested and working
- [ ] Email notifications working
- [ ] All pages load without errors
- [ ] No broken links

---

## High Priority Items

### 🟡 Testing

- [ ] All automated tests passing
- [ ] Manual browser testing complete (Chrome, Safari, Firefox)
- [ ] Mobile testing complete (iOS, Android)
- [ ] Contact form submissions working
- [ ] Newsletter subscription working
- [ ] Admin panel fully functional
- [ ] Performance tests passing (Lighthouse > 80)
- [ ] SEO validation complete

### 🟡 Content

- [ ] All pages have unique meta descriptions
- [ ] All images have alt text
- [ ] Company contact information correct
- [ ] Office addresses correct (Chennai, Hackensack)
- [ ] Phone numbers correct
- [ ] Email addresses correct
- [ ] Social media links (if applicable)
- [ ] Privacy policy page (if required)
- [ ] Terms of service page (if required)

### 🟡 SEO

- [ ] Google Search Console set up
- [ ] Sitemap.xml accessible
- [ ] Robots.txt configured
- [ ] Open Graph tags on all pages
- [ ] Twitter Card tags on all pages
- [ ] Structured data (Schema.org) implemented
- [ ] Canonical URLs on all pages
- [ ] Google Analytics configured (optional)

---

## Medium Priority Items

### 🟢 Documentation

- [ ] DEPLOYMENT_GUIDE.md complete
- [ ] README.md updated
- [ ] Environment variables documented
- [ ] Backup procedure documented
- [ ] Update procedure documented
- [ ] Troubleshooting guide available

### 🟢 Monitoring

- [ ] Error logging configured
- [ ] Log rotation set up
- [ ] Uptime monitoring (optional)
- [ ] Performance monitoring (optional)
- [ ] Email alerts configured (optional)

### 🟢 Legal & Compliance

- [ ] Privacy policy reviewed
- [ ] GDPR compliance (if applicable)
- [ ] Cookie consent (if applicable)
- [ ] Terms of service reviewed
- [ ] Contact information accurate

---

## Pre-Launch Testing Protocol

### 1. Functional Testing

```bash
cd realtor-web/tests
python run_all_tests.py
```

Expected: All tests pass ✅

### 2. Manual Testing

**Pages to Test:**
- [ ] Home page (EN/TA/HI)
- [ ] Services page
- [ ] About page
- [ ] Management page
- [ ] Contact page
- [ ] Blog page
- [ ] Property listings
- [ ] Property detail pages

**Forms to Test:**
- [ ] Contact form submission
- [ ] Newsletter subscription
- [ ] Admin login
- [ ] Property creation in admin

**Languages to Test:**
- [ ] English (EN)
- [ ] Tamil (TA)
- [ ] Hindi (HI)

### 3. Performance Testing

Visit: https://pagespeed.web.dev/

Test URLs:
- [ ] Home page
- [ ] Services page
- [ ] Contact page

Target: Performance score > 80

### 4. Security Testing

```bash
cd realtor-web
python manage.py check --deploy
```

Expected: No critical issues

Visit: https://www.ssllabs.com/ssltest/

Target: A or A+ rating

### 5. Mobile Testing

Test on:
- [ ] iPhone (Safari)
- [ ] Android (Chrome)
- [ ] Tablet

Verify:
- [ ] Navigation works
- [ ] Forms are usable
- [ ] No horizontal scroll
- [ ] Images load correctly

---

## Launch Day Checklist

### Morning (Before DNS Switch)

- [ ] Final backup of current site (if migrating)
- [ ] Database backup
- [ ] Media files backup
- [ ] Verify all tests passing
- [ ] Verify SSL certificate valid
- [ ] Verify email sending works
- [ ] Verify admin panel accessible

### DNS Switch

- [ ] Update DNS A records
- [ ] Update www CNAME record
- [ ] Wait for DNS propagation (15-60 minutes)
- [ ] Verify domain resolves to new server

### After DNS Switch

- [ ] Test website at https://yourdomain.com
- [ ] Test all pages load correctly
- [ ] Test contact form
- [ ] Test admin panel
- [ ] Monitor error logs
- [ ] Monitor server resources

### First 24 Hours

- [ ] Monitor error logs every 2 hours
- [ ] Check email notifications working
- [ ] Verify analytics tracking (if configured)
- [ ] Test from different locations/devices
- [ ] Monitor server performance
- [ ] Be available for quick fixes

---

## Rollback Plan

If critical issues occur:

### Immediate Actions

1. **Revert DNS** (if migrating from old site)
   - Change DNS back to old server
   - Wait for propagation

2. **Take Site Offline** (if new site)
   - Display maintenance page
   - Fix issues
   - Redeploy

3. **Database Rollback**
   - Restore from backup
   - Verify data integrity

### Communication

- [ ] Notify stakeholders
- [ ] Post status update (if applicable)
- [ ] Document issues found
- [ ] Plan fix and relaunch

---

## Post-Launch Monitoring (First Week)

### Daily Checks

- [ ] Check error logs
- [ ] Monitor server resources (CPU, RAM, disk)
- [ ] Verify backups running
- [ ] Check email deliverability
- [ ] Monitor page load times
- [ ] Check for broken links

### Weekly Checks

- [ ] Review analytics (if configured)
- [ ] Check Google Search Console
- [ ] Review user feedback
- [ ] Update content as needed
- [ ] Plan improvements

---

## Sign-Off

### Development Team

**Developer**: _________________  
**Date**: _________________  
**Signature**: _________________

### Product Owner

**Name**: Viji  
**Date**: _________________  
**Signature**: _________________

### Final Approval

- [ ] All critical items complete
- [ ] All high priority items complete
- [ ] Testing complete
- [ ] Documentation complete
- [ ] Ready for production launch

**Launch Approved**: [ ] YES  [ ] NO

**Launch Date**: _________________

---

## Emergency Contacts

**Developer**: [Your Phone]  
**Hosting Support**: [Provider Support]  
**Domain Registrar**: [Registrar Support]  
**Email Service**: [SendGrid/Mailgun Support]

---

**Document Version**: 1.0  
**Last Updated**: February 25, 2026  
**SCCB Compliance**: SCCB-47 ✅
