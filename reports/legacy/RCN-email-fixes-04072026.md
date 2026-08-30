<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra (Platform Owner-Propertism)
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Astra
Created On: 2026-07-04 15:15:00
Last Updated By: Astra
Last Updated On: 2026-07-04 15:15:00
Searchtag: RCN-EMAIL-FIXES-04072026
-->

# Root Cause Analysis (RCN)
## Production Email Delivery & Spam Refactoring

**Document ID:** RCN-email-fixes-04072026  
**Date:** July 04, 2026  
**Status:** RESOLVED & DEPLOYED  
**Architect:** Astra (Integration Architect)  

---

## 1. Problem Statement

Following the production deployment of the Propertism platform, two critical email delivery defects were observed:
1. **Spam Routing:** Outbound lead notification alerts sent to `info@propertism.in` were routed to the GoDaddy/Titan **Spam** folder.
2. **Missing CC Delivery:** No carbon-copy lead notification emails were delivered to `tamil@propertism.in`'s inbox.

---

## 2. Root Cause Analysis

### A. SPF Alignment & SMTP Domain Mismatch (Spam Cause)
The production system was configured to use Google's SMTP relay (`smtp.gmail.com`) authenticated under the email account `propertism.tamil@gmail.com`. The application's display sender (`DEFAULT_FROM_EMAIL`) was set to `info@propertism.in`. 
When GoDaddy/Titan's mail servers received the incoming alert:
- It saw an email claiming to be from `@propertism.in` but arriving from Google IP addresses.
- Because the domain `propertism.in` is hosted on GoDaddy Titan and did not explicitly authorize Google's SMTP servers to send emails on its behalf, the message failed **SPF/DMARC alignment checks** and was flagged as spoofed spam.

### B. SMTP Server Host Mismatch (Titan Auth Failures)
Attempting to connect directly to `smtp.titan.email` on port 587 returned `535 5.7.8 Error: authentication failed`. Although webmail access worked, Flockmail/Titan SMTP authentication requires GoDaddy's dedicated outbound server address: **`smtpout.secureserver.net`**.

### C. AWS Console Overrides
The environment properties defined in the AWS Elastic Beanstalk dashboard (`DEFAULT_FROM_EMAIL`, `EMAIL_HOST`, `EXTRA_NOTIFICATION_EMAIL`) were overriding the default fallback configurations in `settings_production.py`.

---

## 3. Corrective Actions Implemented

1. **Hardcoded SMTP Configuration:** Hardcoded GoDaddy's direct SMTP host (`smtpout.secureserver.net`), port (`587`), and username (`tamil@propertism.in`) in both `settings.py` and `settings_production.py` to bypass any AWS Beanstalk environment overrides.
2. **Authentic Sender Mapping:** Fixed `DEFAULT_FROM_EMAIL` to match the SMTP login account (`tamil@propertism.in`) to align sender headers and satisfy SPF/DKIM verification.
3. **Hardcoded Recipients List:** Enforced `ADMIN_EMAILS = ['info@propertism.in', 'propertism.tamil@gmail.com', 'tamil@propertism.in']` directly in code to ensure all three recipients receive copy delivery regardless of environment properties.
4. **AWS Properties Alignment:** Updated `EMAIL_HOST_PASSWORD` to the correct Titan password (`PropTami@4`) in the AWS console properties.

---

***
*Maintained by Astra | 2026-07-04 15:15 IST*
