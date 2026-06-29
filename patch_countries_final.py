import json
import urllib.request
import re

url = 'https://raw.githubusercontent.com/mledoze/countries/master/countries.json'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    dial_data = json.loads(response.read().decode('utf-8'))

options = []
for c in dial_data:
    if 'idd' in c and 'root' in c['idd']:
        root = c['idd'].get('root', '')
        suffixes = c['idd'].get('suffixes', [])
        # Some countries have multiple suffixes, we'll just take the first one, or if empty just the root
        suffix = suffixes[0] if suffixes else ''
        code = root + suffix
        name = c['name']['common']
        iso = c['cca2'].lower()
        if code:
            options.append((name, code, iso))

options.sort(key=lambda x: x[0])

html = '<option value="">Select Country...</option>\n<option value="+91" data-iso="in">India (+91)</option>\n'
for name, code, iso in options:
    if iso != 'in':
        html += f'<option value="{code}" data-iso="{iso}">{name} ({code})</option>\n'

file_path = r'd:\viji\viji-olivine\03rolledout\01propertism\uilayers\templates\home\sections\_mid_page_form.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken select tag and inject html
fixed_select = r"""<select class="hf-field-input" name="country_code" required style="height: 48px !important;">"""
pattern = re.compile(r"<select class=\"hf-field-input\" name=\"country_code\" required.*?</select>", re.DOTALL)
new_content = pattern.sub(f"{fixed_select}\n{html}\n</select>", content)

# Remove the old buggy autofocus script block
old_autofocus = r"""    // Autofocus logic
    if (window.location.hash === '#mid-page-lead-section' || window.location.hash === '#contact') {
        const nameInput = document.querySelector('input[name="name"]');
        if (nameInput) {
            setTimeout(() => nameInput.focus(), 500);
        }
    }"""
new_content = new_content.replace(old_autofocus, "")

# Add robust autofocus logic
robust_autofocus = """
    function handleFocus() {
        if (['#mid-page-lead-section', '#contact', '#contact-section'].includes(window.location.hash)) {
            const nameInput = document.querySelector('#propertism-mid-page-form input[name="name"]');
            if (nameInput) setTimeout(() => nameInput.focus(), 500);
        }
    }
    window.addEventListener("hashchange", handleFocus);
    handleFocus();
"""
if "window.addEventListener(\"hashchange\", handleFocus);" not in new_content:
    new_content = new_content.replace('document.addEventListener("DOMContentLoaded", function() {', 'document.addEventListener("DOMContentLoaded", function() {' + robust_autofocus)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("SUCCESS")
