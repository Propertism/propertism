# ⚠️ CRITICAL ISSUE: Blog URLs Returning 404

## Situation Summary

**Database Status:** ✓ All 10 Knowledge Hub articles are **PUBLISHED** in the database  
**Code Status:** ✓ URL routing is **CONFIGURED** correctly  
**Production Status:** ✗ Blog URLs are returning **404 NOT FOUND**

---

## What We Know

### Articles ARE Published
- Verified via Django shell query
- All 10 articles have `is_published=True`
- All articles have `published_date` set
- All article slugs are unique and correct

### URL Routing IS Configured
- File: `/content/urls.py` contains:
  ```python
  path('blog/<slug:slug>/', views.blog_post, name='blog_post'),
  ```
- View exists: `views.blog_post()` is defined
- Blog sitemap is configured to generate: `/blog/{slug}/`

### But URLs Return 404
```
❌ https://www.propertism.in/blog/nri-property-management-chennai-complete-guide/
❌ https://www.propertism.in/blog/how-nris-can-sell-property-in-india-from-abroad/
❌ (all 10 Knowledge Hub article URLs return 404)
```

---

## Why This Might Be Happening

### Most Likely Causes (in order)

1. **Production Database ≠ Local Database**
   - Articles exist in local/development database
   - Production RDS doesn't have the articles
   - Solution: Run migrations and seed on production

2. **Old Code Deployed**
   - Latest code with working blog_post view not deployed
   - Production running older version
   - Solution: Redeploy latest code

3. **Database Migration Not Applied**
   - Migration files exist but not run on production
   - BlogPost table might be missing or corrupted
   - Solution: SSH to prod and run `python manage.py migrate`

4. **Deployment/Sync Issue**
   - Code deployed but static files/database not synced
   - Elastic Beanstalk restart needed
   - Solution: Restart application environment

---

## What NEEDS to Happen Before GSC Submission

### Critical Path to Fix

**STOP.** Do NOT submit to GSC until:

1. **✓ Verify Articles Exist on Production**
   ```bash
   # SSH into production
   ssh ec2-user@<prod-server>
   
   # Navigate to app
   cd /var/app/current
   source venv/bin/activate
   
   # Check database
   python manage.py shell
   ```
   
   ```python
   from content.models import BlogPost
   
   # Should return 10
   BlogPost.objects.filter(is_published=True).count()
   
   # Should return valid article
   post = BlogPost.objects.filter(slug='nri-property-management-chennai-complete-guide').first()
   print(post.title if post else "NOT FOUND")
   ```

2. **✓ Test URL Resolution**
   ```python
   from django.urls import reverse
   url = reverse('blog_post', kwargs={'slug': 'nri-property-management-chennai-complete-guide'})
   print(url)  # Should print: /blog/nri-property-management-chennai-complete-guide/
   ```

3. **✓ Test View Returns 200 OK**
   ```python
   from django.test import Client
   client = Client()
   response = client.get('/blog/nri-property-management-chennai-complete-guide/')
   print(f"Status: {response.status_code}")  # Should be 200
   ```

4. **✓ Test Production Website**
   ```bash
   curl -I https://www.propertism.in/blog/nri-property-management-chennai-complete-guide/
   # Should show: HTTP/2 200
   ```

### If Any Test Fails

**If articles don't exist:**
```bash
python manage.py seed_knowledge_hub_phase_a --publish
python manage.py migrate
# Restart app
```

**If URL doesn't resolve:**
```bash
# Check URL configuration
python manage.py show_urls | grep blog
```

**If view returns error:**
```bash
# Check Django logs
tail -f /var/log/django/*.log
tail -f /var/log/httpd/access_log
```

---

## ACTUAL URLs (When Fixed)

Once production is confirmed working:

### Blog Articles (10 URLs)
```
https://www.propertism.in/blog/nri-property-management-chennai-complete-guide/
https://www.propertism.in/blog/how-nris-can-sell-property-in-india-from-abroad/
https://www.propertism.in/blog/power-of-attorney-for-nris-complete-guide/
https://www.propertism.in/blog/how-to-verify-property-documents-chennai/
https://www.propertism.in/blog/patta-transfer-process-explained/
https://www.propertism.in/blog/encumbrance-certificate-guide-for-nris/
https://www.propertism.in/blog/property-tax-guide-chennai-nris/
https://www.propertism.in/blog/capital-gains-tax-property-sale-nris/
https://www.propertism.in/blog/tenant-management-guide-overseas-property-owners/
https://www.propertism.in/blog/nri-property-maintenance-checklist/
```

### Plus Homepage & Service Pages (3 URLs)
```
https://www.propertism.in/
https://www.propertism.in/chennai/nri-property-management/
https://www.propertism.in/chennai/nri-sell-property/
```

---

## TIMELINE ADJUSTMENT

### Previous Timeline (Assuming URLs Work)
- Week 1: Submit to GSC, indexing begins

### Actual Timeline (Until URLs Fixed)
- **TODAY:** Fix production blog URLs
- **After Fix:** Test URLs manually (30 min)
- **Then:** Submit sitemap to GSC
- **Then:** Start Week 1 monitoring

---

## PRIORITY CHECKLIST

Before GSC submission, COMPLETE:

```
[ ] SSH to production server
[ ] Query: BlogPost.objects.filter(is_published=True).count() → Should be 10
[ ] Query: BlogPost.objects.get(slug='nri-property-management-chennai-complete-guide')
[ ] Test URL in browser or curl
[ ] Confirm HTTP 200 status
[ ] Test all 10 URLs (quick spot check)
[ ] Only then: Proceed to GSC submission
```

---

## IF STUCK

**Troubleshooting Commands:**

```bash
# 1. Check if articles in DB
SELECT COUNT(*) FROM content_blogpost WHERE is_published=true;

# 2. Check Django URL routing
python manage.py show_urls | grep blog

# 3. Test Django view directly
python manage.py shell < test_blog.py

# 4. Check web server logs
tail -f /var/log/nginx/error.log
tail -f /var/log/apache2/error.log

# 5. Check Elastic Beanstalk logs (if on AWS EB)
eb logs | grep "blog\|404"

# 6. Force full redeploy
eb deploy --force
```

---

## STATUS FOR PHASE 5

| Item | Status | Issue |
|---|---|---|
| Knowledge Hub Articles (DB) | ✓ PUBLISHED | None - all in database |
| URL Routing (Code) | ✓ CONFIGURED | None - correctly set up |
| Blog View (Code) | ✓ EXISTS | None - view is implemented |
| Production Access | ✗ BROKEN | **404 errors on all blog URLs** |
| GSC Readiness | ✗ BLOCKED | **Cannot submit until URLs are accessible** |

**Action Required:** Fix production blog URL accessibility before proceeding to GSC submission

---

**Last Updated:** 2026-06-16 10:36 UTC  
**Status:** BLOCKED - Awaiting production debug & fix

---
