import re

with open('countries.html', 'r', encoding='utf-8') as f:
    countries_html = f.read().strip()

with open(r'd:\viji\viji-olivine\03rolledout\01propertism\uilayers\templates\home\sections\_mid_page_form.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the select options
start_marker = r"<select class=\"hf-field-input\" name=\"country_code\" required>"
end_marker = r"</select>"
# Note: the previous patch removed the style="height..." stuff and left it as `<select ... required>` if TomSelect took over? 
# Let's just find the select block
pattern = re.compile(r"(<select class=\"hf-field-input\" name=\"country_code\" required.*?>).*?(</select>)", re.DOTALL)
new_content = pattern.sub(f"\\1\n{countries_html}\n\\2", content)

# Now swap Phone and Country Code.
# They are inside <div class="hf-field-row">
field_row_pattern = re.compile(
    r'(<div class="hf-field-group" style="margin-bottom: 0 !important;">\s*<label class="hf-field-label">Name</label>.*?</div>)\s*'
    r'(<div class="hf-field-group" style="margin-bottom: 0 !important;">\s*<label class="hf-field-label">WhatsApp / Phone</label>.*?</div>)\s*'
    r'(<div class="hf-field-group" style="margin-bottom: 0 !important;">\s*<label class="hf-field-label">Country Code</label>.*?</div>)',
    re.DOTALL
)

new_content = field_row_pattern.sub(r'\1\n\n\3\n\n\2', new_content)

# Update the Tom Select JS code to include the render function
old_ts_code = """        new TomSelect(el, {
            create: false,
            sortField: {
                field: "text",
                direction: "asc"
            }
        });"""

new_ts_code = """        new TomSelect(el, {
            create: false,
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
        });"""

new_content = new_content.replace(old_ts_code, new_ts_code)

with open(r'd:\viji\viji-olivine\03rolledout\01propertism\uilayers\templates\home\sections\_mid_page_form.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
