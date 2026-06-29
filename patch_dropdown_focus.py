import re

file_path = r'd:\viji\viji-olivine\03rolledout\01propertism\uilayers\templates\home\sections\_mid_page_form.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Add dropdownParent to Tom Select config
old_ts_config = """        new TomSelect(el, {
            create: false,
            sortField: { field: "text", direction: "asc" },"""

new_ts_config = """        new TomSelect(el, {
            create: false,
            dropdownParent: "body",
            sortField: { field: "text", direction: "asc" },"""

if 'dropdownParent: "body",' not in content:
    content = content.replace(old_ts_config, new_ts_config)

# Fix 2: Add z-index and position relative to the hf-field-group containing the select
old_group = """<div class="hf-field-group" style="margin-bottom: 0 !important;">
                        <label class="hf-field-label">Country Code</label>
                        <select class="hf-field-input" name="country_code" required style="height: 48px !important;">"""
new_group = """<div class="hf-field-group" style="margin-bottom: 0 !important; position: relative; z-index: 9999;">
                        <label class="hf-field-label">Country Code</label>
                        <select class="hf-field-input" name="country_code" required style="height: 48px !important;">"""
if "z-index: 9999;" not in content:
    content = content.replace(old_group, new_group)

# Fix 3: Update handleFocus function to focus the correct form
old_focus = """    function handleFocus() {
        if (['#mid-page-lead-section', '#contact', '#contact-section'].includes(window.location.hash)) {
            const nameInput = document.querySelector('#propertism-mid-page-form input[name="name"]');
            if (nameInput) setTimeout(() => nameInput.focus(), 500);
        }
    }"""

new_focus = """    function handleFocus() {
        const hash = window.location.hash;
        if (hash === '#mid-page-lead-section') {
            const nameInput = document.querySelector('#propertism-mid-page-form input[name="name"]');
            if (nameInput) setTimeout(() => nameInput.focus(), 500);
        } else if (hash === '#contact' || hash === '#contact-section') {
            const contactInput = document.querySelector('#propertism-hf-form input[name="name"]');
            if (contactInput) setTimeout(() => contactInput.focus(), 500);
        }
    }"""
content = content.replace(old_focus, new_focus)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS")
