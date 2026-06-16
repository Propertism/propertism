#!/bin/bash

# SCCB-PROP-KNOWLEDGE-HUB-SQLITE-ACTIVATION-1606
# Test all 10 Phase-A blog URLs for HTTP 200 response

echo "========================================"
echo "Testing all 10 Phase-A Blog URLs"
echo "========================================"
echo ""

# Define all 10 article URLs
urls=(
  "https://www.propertism.in/en/blog/nri-property-management-basics/"
  "https://www.propertism.in/en/blog/nri-property-purchase-guide/"
  "https://www.propertism.in/en/blog/nri-property-investment-strategy/"
  "https://www.propertism.in/en/blog/nri-property-financing-options/"
  "https://www.propertism.in/en/blog/nri-property-legal-compliance/"
  "https://www.propertism.in/en/blog/nri-property-tax-planning/"
  "https://www.propertism.in/en/blog/nri-property-management-during-covid/"
  "https://www.propertism.in/en/blog/nri-rental-income-optimization/"
  "https://www.propertism.in/en/blog/nri-property-dispute-resolution/"
  "https://www.propertism.in/en/blog/nri-property-disposal-guide/"
)

# Test each URL
pass=0
fail=0

for url in "${urls[@]}"; do
  status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  slug=$(echo "$url" | grep -o 'blog/[^/]*' | cut -d'/' -f2)
  
  if [ "$status" = "200" ]; then
    echo "✅ 200 — $slug"
    ((pass++))
  else
    echo "❌ $status — $slug"
    ((fail++))
  fi
done

echo ""
echo "========================================"
echo "Results: $pass passed, $fail failed"
echo "========================================"

if [ $fail -eq 0 ]; then
  echo "✅ All 10 blog URLs returning 200 OK"
  exit 0
else
  echo "❌ Some URLs failed — check production database initialization"
  exit 1
fi
