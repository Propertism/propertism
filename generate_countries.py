import urllib.request, json
import re

dial_url = 'https://raw.githubusercontent.com/mledoze/countries/master/countries.json'
req2 = urllib.request.Request(dial_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req2) as response:
        dial_data = json.loads(response.read().decode())
except:
    dial_data = []

options = []
for c in dial_data:
    if 'callingCode' in c and len(c['callingCode']) > 0:
        code = "+" + c['callingCode'][0]
        name = c['name']['common']
        iso = c['cca2'].lower()
        options.append((name, code, iso))
    
html = '<option value="">Select Country...</option>\n<option value="+91" data-iso="in">India (+91)</option>\n'
for name, code, iso in options:
    if iso != 'in':
        html += f'<option value="{code}" data-iso="{iso}">{name} ({code})</option>\n'
        
with open('countries.html', 'w', encoding='utf-8') as f:
    f.write(html)
