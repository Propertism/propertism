import csv
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

csv_path = r"D:\viji\viji-olivine\03rolledout\06propertism.deal.engine\inquiries_20260714_1326.csv"

# Potential keywords for selling
sell_keywords = ["sell", "sale", "selling", "dispose", "divest", "liquidate", "valuation", "buyer", "offer"]

print("Analyzing CSV for Sell-related leads...")
print("-" * 100)

qualified_leads = []

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        msg = row['Message']
        msg_lower = msg.lower()
        
        # Check if it contains sell keywords
        is_sell = False
        for kw in sell_keywords:
            if kw in msg_lower:
                is_sell = True
                break
                
        # Exclude obvious spam or rental requests
        is_spam = any(x in msg_lower for x in [".ru", "seo", "клининг", "асфальт", "доставка", "wikipedia", "dubai-based", "business consulting", "mklider.ru", "proffseo.ru", "ellman.ru", "analyztepla.ru"])
        is_rent = any(x in msg_lower for x in ["rent", "tenants", "rental", "lease", "roommate", "flatmate"])
        is_buy = any(x in msg_lower for x in ["looking for 1 bhk", "want to buy", "looking to buy"])
        
        # Let's print candidate rows that match sell or look like real inquiries
        if (is_sell or (not is_spam and not is_rent and not is_buy)) and not is_spam:
            qualified_leads.append(row)

print(f"Found {len(qualified_leads)} candidate sell-related leads:")
print("=" * 100)
for lead in qualified_leads:
    print(f"ID: {lead['ID']} | Name: {lead['Name']} | Phone: {lead['Phone']} | Status: {lead['Status']} | Submitted: {lead['Submitted']}")
    print(f"Message:")
    print(lead['Message'])
    print("-" * 100)
