import re

file_path = r'd:\viji\viji-olivine\03rolledout\01propertism\uilayers\templates\home\sections\_mid_page_form.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Z-Index for dropdown
css_target = ".ts-dropdown {\n    background-color: #0b0f1a !important;"
if "z-index: 9999" not in content:
    content = content.replace(css_target, ".ts-dropdown {\n    z-index: 9999 !important;\n    background-color: #0b0f1a !important;")

# Fix 2: Add focus after smooth scrolling in the data-select-intent click handler
scroll_target1 = "scrollToElementWithOffset('mid-page-lead-section');\n                        history.pushState(null, null, '#mid-page-lead-section');"
focus_injection = """scrollToElementWithOffset('mid-page-lead-section');
                        history.pushState(null, null, '#mid-page-lead-section');
                        setTimeout(() => {
                            const nameInput = document.querySelector('#propertism-mid-page-form input[name="name"]');
                            if (nameInput) nameInput.focus();
                        }, 600);"""

if "setTimeout(() => {\n                            const nameInput = document.querySelector('#propertism-mid-page-form input[name=\"name\"]');" not in content:
    content = content.replace(scroll_target1, focus_injection)

# Fix 3: Add focus inside checkUrlIntent()
scroll_target2 = """scrollToElementWithOffset('mid-page-lead-section');\n                        }, 300);"""
focus_injection2 = """scrollToElementWithOffset('mid-page-lead-section');\n                            setTimeout(() => {
                                const nameInput = document.querySelector('#propertism-mid-page-form input[name="name"]');
                                if (nameInput) nameInput.focus();
                            }, 300);\n                        }, 300);"""

if "setTimeout(() => {\n                                const nameInput" not in content:
    content = content.replace(scroll_target2, focus_injection2)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS")
