import re

# _mid_page_form.html
file1 = r'd:\viji\viji-olivine\03rolledout\01propertism\uilayers\templates\home\sections\_mid_page_form.html'
with open(file1, 'r', encoding='utf-8') as f:
    content1 = f.read()

replacements1 = {
    '<label class="hf-field-label">Name</label>': '<label class="hf-field-label">Name <span style="color: #ff4d4d;">*</span></label>',
    '<label class="hf-field-label">Country Code</label>': '<label class="hf-field-label">Country Code <span style="color: #ff4d4d;">*</span></label>',
    '<label class="hf-field-label">WhatsApp / Phone</label>': '<label class="hf-field-label">WhatsApp / Phone <span style="color: #ff4d4d;">*</span></label>',
    '<label class="hf-field-label" style="margin-bottom: 8px !important;">What do you want to do?</label>': '<label class="hf-field-label" style="margin-bottom: 8px !important;">What do you want to do? <span style="color: #ff4d4d;">*</span></label>'
}

for old, new in replacements1.items():
    content1 = content1.replace(old, new)

with open(file1, 'w', encoding='utf-8') as f:
    f.write(content1)


# _contact.html
file2 = r'd:\viji\viji-olivine\03rolledout\01propertism\uilayers\templates\home\sections\_contact.html'
with open(file2, 'r', encoding='utf-8') as f:
    content2 = f.read()

replacements2 = {
    '<label class="hf-field-label">Full Name</label>': '<label class="hf-field-label">Full Name <span style="color: #ff4d4d;">*</span></label>',
    '<label class="hf-field-label">Email Address</label>': '<label class="hf-field-label">Email Address <span style="color: #ff4d4d;">*</span></label>',
    '<label class="hf-field-label">Country Code</label>': '<label class="hf-field-label">Country Code <span style="color: #ff4d4d;">*</span></label>',
    '<label class="hf-field-label">Phone Number</label>': '<label class="hf-field-label">Phone Number <span style="color: #ff4d4d;">*</span></label>',
    '<label class="hf-field-label">Service Needed</label>': '<label class="hf-field-label">Service Needed <span style="color: #ff4d4d;">*</span></label>',
    '<label class="hf-field-label">Message</label>': '<label class="hf-field-label">Message <span style="color: #ff4d4d;">*</span></label>'
}

for old, new in replacements2.items():
    content2 = content2.replace(old, new)

with open(file2, 'w', encoding='utf-8') as f:
    f.write(content2)

print("SUCCESS")
