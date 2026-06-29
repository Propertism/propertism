import re

# Read countries html
with open('countries.html', 'r', encoding='utf-8') as f:
    countries_html = f.read().strip()

# Read contact form
file_path = r'd:\viji\viji-olivine\03rolledout\01propertism\uilayers\templates\home\sections\_contact.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The target block
target_block = """                        <div class="hf-field-group">
                            <label class="hf-field-label">Service Needed</label>
                            <select class="hf-field-select" name="service" required>
                                <option value="" disabled selected>Select Service Needed</option>
                                {% for value, label in contact_service_choices %}
                                <option value="{{ value }}">{{ label }}</option>
                                {% endfor %}
                            </select>
                        </div>"""

new_block = f"""                        <div class="hf-field-row" style="display: grid; grid-template-columns: 1fr 1.5fr 1.5fr; gap: 16px;">
                            <div class="hf-field-group" style="position: relative; z-index: 9999;">
                                <label class="hf-field-label">Country Code</label>
                                <select class="hf-field-input" name="contact_country_code" id="contact_country_code" required style="height: 48px !important;">
{countries_html}
                                </select>
                            </div>
                            <div class="hf-field-group">
                                <label class="hf-field-label">Phone Number</label>
                                <input class="hf-field-input" name="phone" type="tel" placeholder="Phone Number" required pattern="^[0-9\-\+\s]{7,15}$" title="Please enter a valid phone number (7-15 digits)" style="height: 48px !important;" />
                            </div>
                            <div class="hf-field-group">
                                <label class="hf-field-label">Service Needed</label>
                                <select class="hf-field-select" name="service" required style="height: 48px !important;">
                                    <option value="" disabled selected>Select Service Needed</option>
                                    {{% for value, label in contact_service_choices %}}
                                    <option value="{{{{ value }}}}">{{{{ label }}}}</option>
                                    {{% endfor %}}
                                </select>
                            </div>
                        </div>"""

# Replace in content
if target_block in content:
    content = content.replace(target_block, new_block)
else:
    print("Could not find target block!")

# Add Javascript to handle form submission and TomSelect
js_to_add = """<script>
    document.addEventListener("DOMContentLoaded", function() {
        var el = document.getElementById('contact_country_code');
        if (el && typeof TomSelect !== 'undefined') {
            new TomSelect(el, {
                create: false,
                dropdownParent: "body",
                sortField: { field: "text", direction: "asc" },
                render: {
                    option: function(data, escape) {
                        var iso = data.$option.getAttribute('data-iso');
                        var flagHtml = iso ? '<img src="https://flagcdn.com/w20/' + escape(iso) + '.png" style="width:20px; margin-right:8px; vertical-align:middle;">' : '';
                        return '<div>' + flagHtml + escape(data.text) + '</div>';
                    },
                    item: function(data, escape) {
                        var iso = data.$option.getAttribute('data-iso');
                        var flagHtml = iso ? '<img src="https://flagcdn.com/w20/' + escape(iso) + '.png" style="width:20px; margin-right:8px; vertical-align:middle;">' : '';
                        return '<div>' + flagHtml + escape(data.text) + '</div>';
                    }
                }
            });
        }

        const contactForm = document.getElementById('propertism-hf-form');
        if (contactForm) {
            contactForm.addEventListener('submit', function(e) {
                const phoneInput = this.querySelector('input[name="phone"]');
                const countrySelect = this.querySelector('select[name="contact_country_code"]');
                if (phoneInput && countrySelect) {
                    const countryCode = countrySelect.value;
                    let rawPhone = phoneInput.value;
                    if (!rawPhone.startsWith('+')) {
                        phoneInput.value = countryCode + " " + rawPhone;
                    }
                }
            });
        }
    });
</script>"""

if "contact_country_code" not in content and "TomSelect(el" not in content.split("</div>")[-1]:
    content = content + "\n" + js_to_add

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS")
