import datetime
import re

file_path = r'd:\viji\viji-olivine\03rolledout\01propertism\.session-tracker\SESSION_TRACKER.md'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add Session 46
session_46 = "| 46 | June 29 | **QUICK INQUIRY & CONTACT FORM REFINEMENTS.** Refactored country selection to use Tom Select with FlagCDN integration for 240+ countries. Reordered form fields for logical flow (Name -> Country -> Phone) in Quick Inquiry and consolidated Country/Phone/Service in Contact form. Added dynamic auto-focus triggers for all anchor-based CTAs and highlighted mandatory fields. | ✅ |\n"

content = content.replace("19:\n", "19:\n" + session_46)

# Update metadata
now = datetime.datetime.now()
date_str = now.strftime("%B %d, %Y (%H:%M IST)")

content = re.sub(r'\*\*Last Updated On\*\*: .*', f'**Last Updated On**: {date_str}', content)
content = re.sub(r'\*\*Last Update\*\*: .*', '**Last Update**: SESSION 46 - QUICK INQUIRY & CONTACT FORM REFINEMENTS. Improved country selection dropdown UX, added custom autofocus, reorganized field layout, and marked mandatory fields.', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS")
