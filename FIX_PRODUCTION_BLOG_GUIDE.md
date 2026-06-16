# FIX PRODUCTION BLOG ARTICLES - STEP BY STEP

## Your Production Setup
- **AWS Elastic Beanstalk Environment:** `propertism-prod-2026`
- **Region:** `us-east-1`
- **Application:** `propertism-2026`

---

## STEP 1: Connect to Production via EB CLI

You have EB CLI installed (from `.elasticbeanstalk/config.yml`).

### Option A: Using EB CLI (Easiest)

```bash
# From your local machine, in the project root:
eb ssh
```

This will automatically SSH you into the running EB instance.

**Expected output:**
```
Entering EC2 instance "i-xxxxxxxx"
ec2-user@ip-xxx-xxx-xxx-xxx ~$
```

### Option B: Manual SSH (If EB CLI doesn't work)

```bash
# Get instance details
eb status

# Find the instance ID, then SSH directly
ssh -i your-key.pem ec2-user@<instance-public-ip>
```

---

## STEP 2: Once Connected, Run Diagnostic

```bash
# Navigate to app directory
cd /var/app/current

# Activate virtual environment
source /var/app/venv/*/bin/activate

# Run diagnostic script
python manage.py shell << 'EOF'
from content.models import BlogPost

# Check how many articles exist
count = BlogPost.objects.filter(is_published=True).count()
print(f"Published articles in production: {count}")

# Check if specific article exists
article = BlogPost.objects.filter(slug='nri-property-management-chennai-complete-guide').first()
if article:
    print(f"✓ Sample article found: {article.title}")
else:
    print("✗ Sample article NOT found")
EOF
```

**Expected output (if articles missing):**
```
Published articles in production: 0
✗ Sample article NOT found
```

---

## STEP 3: Seed Articles If Missing

If the diagnostic shows **0 articles**, run:

```bash
# Still in /var/app/current with venv activated
python manage.py seed_knowledge_hub_phase_a --publish
```

**Expected output:**
```
10 PUBLISHED: nri-property-management-chennai-complete-guide
10 PUBLISHED: how-nris-can-sell-property-in-india-from-abroad
...
(all 10 articles seeded)
Done. Created: 10  Skipped: 0
```

---

## STEP 4: Run Migrations

```bash
python manage.py migrate --no-input
```

**Expected output:**
```
Operations to perform:
  Apply all migrations: content, ...
Running migrations:
  Applying ... OK
```

---

## STEP 5: Restart Application

Exit the SSH session first:

```bash
exit
```

Then from your **local machine** (project root):

```bash
# Restart the EB environment
eb appversion -e propertism-prod-2026
```

Or force a full restart:

```bash
eb restart
```

**Wait 1-2 minutes for the environment to restart.**

---

## STEP 6: Verify URLs are Now Working

Test the URLs from your **local machine**:

```bash
# Test homepage
curl -I https://www.propertism.in/

# Test one blog article
curl -I https://www.propertism.in/blog/nri-property-management-chennai-complete-guide/

# Test all 10 articles
for slug in \
  "nri-property-management-chennai-complete-guide" \
  "how-nris-can-sell-property-in-india-from-abroad" \
  "power-of-attorney-for-nris-complete-guide" \
  "how-to-verify-property-documents-chennai" \
  "patta-transfer-process-explained" \
  "encumbrance-certificate-guide-for-nris" \
  "property-tax-guide-chennai-nris" \
  "capital-gains-tax-property-sale-nris" \
  "tenant-management-guide-overseas-property-owners" \
  "nri-property-maintenance-checklist"; do
  echo "Testing: $slug"
  curl -s -o /dev/null -w "Status: %{http_code}\n" https://www.propertism.in/blog/$slug/
done
```

**Expected output (all should be 200 OK):**
```
Testing: nri-property-management-chennai-complete-guide
Status: 200
Testing: how-nris-can-sell-property-in-india-from-abroad
Status: 200
... (all 10 should be 200)
```

---

## COMPLETE COMMAND SEQUENCE

For quick copy-paste (do this all at once):

```bash
# 1. SSH to production
eb ssh

# 2. Once connected (you'll see: ec2-user@...)
cd /var/app/current
source /var/app/venv/*/bin/activate

# 3. Check current status
python manage.py shell << 'DIAGNOSTIC'
from content.models import BlogPost
print(f"Current articles: {BlogPost.objects.filter(is_published=True).count()}")
DIAGNOSTIC

# 4. If count is 0, seed articles
python manage.py seed_knowledge_hub_phase_a --publish

# 5. Run migrations
python manage.py migrate --no-input

# 6. Exit SSH
exit

# 7. From your LOCAL machine, restart EB
eb restart
```

---

## TROUBLESHOOTING

### If "eb ssh" doesn't work:

```bash
# Try these alternatives:

# Option 1: Use EB CLI to get instance ID
eb instances -o

# Option 2: Use AWS CLI directly
aws ec2 describe-instances \
  --filters "Name=tag:aws:elasticbeanstalk:environment-name,Values=propertism-prod-2026" \
  --query "Reservations[0].Instances[0].PublicIpAddress" \
  --region us-east-1
```

### If venv activation fails:

```bash
# Find the correct venv path
ls -la /var/app/venv/

# Then activate with full path
source /var/app/venv/staging-*/bin/activate
```

### If database connection fails:

```bash
# Check RDS connection details in EB environment
eb config

# Look for RDS_* variables
```

### If seeding takes too long:

```bash
# It can take 30-60 seconds. Let it complete.
# You should see "Done. Created: 10" at the end.

# If it hangs, Ctrl+C and run again
```

---

## QUICK CHECKLIST

```
[ ] Run: eb ssh
[ ] Inside EB instance, run diagnostic (should show 0 articles initially)
[ ] Run: python manage.py seed_knowledge_hub_phase_a --publish
[ ] Run: python manage.py migrate --no-input
[ ] Exit SSH: exit
[ ] From local machine: eb restart
[ ] Wait 1-2 minutes for restart
[ ] Test URLs with curl (should all be 200 OK)
[ ] Ready for GSC submission!
```

---

## After This Is Done

Once all URLs return **200 OK**, you're ready to:
1. Submit sitemap to GSC
2. Request indexing for 13 priority URLs
3. Monitor indexing progress

**Next phase:** We move to Priority 2 (GSC submission)

---
