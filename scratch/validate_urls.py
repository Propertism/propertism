import urllib.request
import urllib.error
import ssl

slugs = [
    'capital-gains-tax-property-sale-nris',
    'common-mistakes-nri-property-buyers-chennai',
    'encumbrance-certificate-guide-for-nris',
    'end-to-end-nri-property-services-chennai',
    'how-nris-can-sell-property-in-india-from-abroad',
    'how-propertism-simplifies-nri-property-ownership',
    'how-to-verify-property-documents-chennai',
    'nri-property-buying-process-chennai',
    'nri-property-checklist-chennai',
    'nri-property-checklist-chennai-owners-abroad',
    'nri-property-legal-compliance-chennai',
    'nri-property-maintenance-checklist',
    'nri-property-management-chennai-complete-guide',
    'nri-property-management-company-chennai',
    'nri-property-management-guide-chennai',
    'nri-property-ownership-challenges-chennai',
    'nri-property-services-chennai-guide',
    'nri-property-tax-chennai-guide',
    'nri-real-estate-investment-chennai-guide',
    'patta-transfer-process-explained',
    'power-of-attorney-for-nris-complete-guide',
    'property-tax-guide-chennai-nris',
    'rental-readiness-for-absentee-owners',
    'tenant-management-guide-overseas-property-owners',
    'why-reporting-matters-for-nri-property-management'
]

base_url = "https://www.propertism.in"

# Ignore SSL verification issues if any
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

results = []
all_200 = True

print("Validating URLs on production...")
for i, slug in enumerate(slugs, 1):
    url = f"{base_url}/blog/{slug}/"
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            status = response.status
            print(f"[{i:02d}/25] {status} OK - {url}")
            results.append((slug, url, status, "OK"))
    except urllib.error.HTTPError as e:
        print(f"[{i:02d}/25] {e.code} ERROR - {url}")
        results.append((slug, url, e.code, "Error"))
        all_200 = False
    except Exception as e:
        print(f"[{i:02d}/25] FAILED - {url} ({e})")
        results.append((slug, url, "FAILED", str(e)))
        all_200 = False

print("\nValidation Complete!")
print(f"All 200 OK: {all_200}")
