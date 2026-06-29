import json
import urllib.request
import re

url = 'https://raw.githubusercontent.com/mledoze/countries/master/countries.json'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    dial_data = json.loads(response.read().decode('utf-8'))

options = []
for c in dial_data:
    if 'callingCode' in c and len(c['callingCode']) > 0:
        code = "+" + c['callingCode'][0]
        name = c['name']['common']
        iso = c['cca2'].lower()
        options.append((name, code, iso))

options.sort(key=lambda x: x[0])

html = '<option value="">Select Country...</option>\n<option value="+91" data-iso="in">India (+91)</option>\n'
for name, code, iso in options:
    if iso != 'in':
        html += f'<option value="{code}" data-iso="{iso}">{name} ({code})</option>\n'

with open(r'd:\viji\viji-olivine\03rolledout\01propertism\uilayers\templates\home\sections\_mid_page_form.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken select tag and inject html
fixed_select = r"""<select class="hf-field-input" name="country_code" required style="height: 48px !important;">"""
pattern = re.compile(r"<select class=\"hf-field-input\" name=\"country_code\" required.*?</select>", re.DOTALL)
new_content = pattern.sub(f"{fixed_select}\n{html}\n</select>", content)

# Add autofocus logic
autofocus_script = """
    // Autofocus logic
    if (window.location.hash === '#mid-page-lead-section' || window.location.hash === '#contact') {
        const nameInput = document.querySelector('input[name="name"]');
        if (nameInput) {
            setTimeout(() => nameInput.focus(), 500);
        }
    }
"""
if "// Autofocus logic" not in new_content:
    new_content = new_content.replace('document.addEventListener("DOMContentLoaded", function() {', 'document.addEventListener("DOMContentLoaded", function() {' + autofocus_script)

with open(r'd:\viji\viji-olivine\03rolledout\01propertism\uilayers\templates\home\sections\_mid_page_form.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("SUCCESS")
