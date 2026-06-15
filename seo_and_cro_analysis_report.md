# Technical SEO & Conversion Rate Optimization (CRO) Audit Report

This report presents a thorough, expert-level audit of the technical SEO and conversion funnel performance of [propertism.in](https://www.propertism.in). It diagnoses the key issues preventing search indexation, explains why organic traffic is not converting into inquiries, and provides concrete, step-by-step technical and content-led recommendations.

---

## Executive Summary

While Propertism has a robust, modern design and a well-engineered programmatic landing page architecture, **several high-priority technical configuration errors completely block search engines (like Googlebot) from crawling and indexing the website's dynamic pages.**

Additionally, the lead acquisition funnel suffers from **conversion friction and a lack of visual proof points**, which discourages visiting overseas owners from submitting inquiries.

```mermaid
graph TD
    A[Googlebot Crawls Robots.txt] --> B{Sitemap URL Protocol}
    B -- http://www.propertism.in/sitemap.xml --> C[Fetch sitemap.xml]
    C --> D{Inspect loc URLs}
    D -- http://example.com/... --> E[CRITICAL FAILURE: Crawlers ignore sitemap]
    D -- http://www.propertism.in/... --> F[Index pages (Target State)]
```

---

## Part 1: Critical Technical SEO Diagnostics ("The Smoking Guns")

### 1. The `example.com` Sitemap Domain Bug
The most critical issue discovered is that `sitemap.xml` on the live production site is currently generating links pointing to **`http://example.com/`** instead of **`https://www.propertism.in/`**.

> [!CAUTION]
> **Impact:** Googlebot and other crawlers fetch the sitemap, see `example.com` in every `<loc>` tag, and immediately reject the sitemap. None of the dynamically generated landing pages (the core organic SEO traffic driver) are indexed.

**Root Cause:**
Django's sitemap framework relies on `django.contrib.sites`. By default, Django initializes a site record with `domain="example.com"` and `name="example.com"`. If this record (Site ID = 1) is not updated in the production database, Django will output all URLs in sitemaps prefixed with `http://example.com/`.

---

### 2. Missing SSL Header Configuration in Production
In `realtor_project/settings_production.py`, the setting `SECURE_PROXY_SSL_HEADER` is completely missing.

> [!WARNING]
> **Impact:** When Gunicorn/Django runs behind an SSL-terminating load balancer (like AWS ALB or Cloudfront), Django is unaware that requests are secure (`https`). Thus, `request.is_secure()` returns `False`.
>
> This forces `robots.txt` to render sitemap links using the insecure `http` protocol:
> `Sitemap: http://www.propertism.in/sitemap.xml`
> It also breaks canonical link resolution by defaulting templates to `http`.

**Required Settings Fix:**
```python
# settings_production.py
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
```

---

### 3. Programmatic SEO (pSEO) Indexation Risk & Duplicate Content
The site programmatically multiplies **3 Cities** $\times$ **10 Intents** $\times$ **14 NRI Locations** to generate **420 dynamic landing pages** (e.g., `/singapore/chennai-nri-sell-property/`).

Google’s Helpful Content System penalizes sites generating massive matrices of landing pages using "thin, template-swapped" content. Because the descriptions, intros, and FAQs are highly similar across different country paths (only swapping keywords like "Singapore" or "Dallas, TX"), Google's deduplication algorithm will flag them as duplicates.

---

### 4. The Orphan Page Problem (No Crawl Path)
Even if the sitemap is fixed, search engines need a natural internal linking structure (crawl path) to discover and value these pages.
* Currently, none of the 420 landing pages are linked internally from the homepage or main menu.
* Pages that are *only* referenced in sitemaps and have no internal link context are classified as **orphan pages** and are rarely indexed or given ranking authority.

---

## Part 2: Conversion Rate Optimization (CRO) & Lead Funnel Blocker

Even when visitors reach the site, they are not converting into inquiries. Here are the key conversion friction points:

### 1. High Friction Call-to-Actions (CTAs)
* **Book Free NRI Consultation** and the mid-page form are "static" forms requiring the user to fill out a description and wait for a response.
* For overseas property owners who are busy and dealing with time zone differences, waiting for email replies is a slow friction point.
* **Solution:** Integrate a direct scheduling tool (like Calendly) on the primary gold CTA so HNIs can immediately book a Zoom call during their convenient timezone hours, alongside the standard WhatsApp chat.

### 2. Lack of Visual Trust & Proof Points
NRIs managing high-value assets from 10,000 km away are highly risk-averse. 
* The site lists stats and reviews, but lacks visual validation.
* **Solution:** Display mockups of the "NRI Owner Portal / Reporting Dashboard" (e.g., showing a timeline of regular inspect reports, tenant payouts, and document lists). Showing *how* execution transparency works on-ground will instantly boost trust and double form conversion.

---

## Part 3: Step-by-Step Recovery Action Plan (No Code Changes Yet)

### Step 1: Database Fix (Resolve Sitemap Domain)
We must update the Site domain in the production database. This can be done via the Django Admin panel or a quick command shell.
1. Log into the Django Admin at `https://www.propertism.in/admin/`.
2. Locate the **Sites** model section.
3. Click on the record with ID 1 (domain `example.com`).
4. Change the **Domain name** to `www.propertism.in` and **Display name** to `Propertism`.
5. Click **Save**.

---

### Step 2: Code Configuration Update
Add the secure header variables in `settings_production.py` to ensure all dynamic links and canonicals render as `https`.
```python
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
```

---

### Step 3: Crawlability and Linking Architecture
Create an index page or linking matrix in the footer called **"Global Coverage"** or **"Our NRI Network"**. 
* This provides a directory of links (e.g., by location/city combinations) so Googlebot has a clean, natural crawl path to discover every landing page from the home page.

---

### Step 4: Page Speed Optimization (Core Web Vitals)
* Ensure that the large hero backgrounds are compressed and optimized (WebP format instead of raw png/jpg) to maintain a fast First Contentful Paint (FCP) on mobile devices, which directly affects mobile SEO ranking.
