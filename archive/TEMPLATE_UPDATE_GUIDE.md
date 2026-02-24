# Template Update Guide for Viji

## ✅ Services Page - DONE (Example)

I've updated `services.html` as an example. You can see how it works now!

---

## 📝 Your Task: Update 3 Pages

You need to update these 3 templates:
1. `about.html`
2. `management.html`
3. `contact.html`

I'll update the `blog.html` after you're done.

---

## 🎯 How to Update Templates

### Step 1: Understand Django Template Syntax

**Display a variable**:
```django
{{ variable_name }}
```

**Loop through a list**:
```django
{% for item in items %}
    <p>{{ item.name }}</p>
{% endfor %}
```

**Check if variable exists**:
```django
{% if variable %}
    <p>{{ variable }}</p>
{% else %}
    <p>Default text</p>
{% endif %}
```

**Empty check in loop**:
```django
{% for item in items %}
    <p>{{ item }}</p>
{% empty %}
    <p>No items found</p>
{% endfor %}
```

---

## 📋 Page 1: about.html

### Variables Available in View
From `content/views.py` → `about()` function:
- `company` - CompanyInfo object
- `stats` - List of Statistic objects
- `values` - List of CoreValue objects

### What to Replace

#### 1. Mission Section
**Find this**:
```html
<p>At Propertism Realty Advisors LLP, we specialize in...</p>
<p>We manage your property and resources...</p>
```

**Replace with**:
```django
{% if company %}
<p>{{ company.about_mission }}</p>
<p>{{ company.about_description }}</p>
{% else %}
<p>At Propertism Realty Advisors LLP, we specialize in...</p>
<p>We manage your property and resources...</p>
{% endif %}
```

#### 2. Stats Section
**Find this**:
```html
<div class="stat-item">
    <h3>500+</h3>
    <p>Properties Managed</p>
</div>
<div class="stat-item">
    <h3>1200+</h3>
    <p>Satisfied Clients</p>
</div>
<div class="stat-item">
    <h3>15+</h3>
    <p>Years of Experience</p>
</div>
```

**Replace with**:
```django
{% for stat in stats %}
<div class="stat-item">
    <h3>{{ stat.value }}</h3>
    <p>{{ stat.label }}</p>
</div>
{% empty %}
<div class="stat-item">
    <h3>500+</h3>
    <p>Properties Managed</p>
</div>
{% endfor %}
```

#### 3. Values Section
**Find this**:
```html
<div class="value-card">
    <div class="value-icon">✓</div>
    <h3>Trust & Transparency</h3>
    <p>We believe in complete transparency...</p>
</div>
<!-- Repeat for other values -->
```

**Replace with**:
```django
{% for value in values %}
<div class="value-card">
    <div class="value-icon">{{ value.icon }}</div>
    <h3>{{ value.title }}</h3>
    <p>{{ value.description }}</p>
</div>
{% empty %}
<div class="value-card">
    <div class="value-icon">✓</div>
    <h3>Trust & Transparency</h3>
    <p>We believe in complete transparency...</p>
</div>
{% endfor %}
```

#### 4. Footer (Same as services.html)
Copy the footer from `services.html` (lines with `{% if company %}`)

---

## 📋 Page 2: management.html

### Variables Available in View
From `content/views.py` → `management()` function:
- `company` - CompanyInfo object
- `team_members` - List of TeamMember objects
- `expertise_areas` - List of ExpertiseArea objects

### What to Replace

#### 1. Team Members Section
**Find this**:
```html
<div class="team-member">
    <div class="member-photo">[Photo]</div>
    <div class="member-info">
        <h3>Managing Director</h3>
        <div class="member-role">Leadership & Strategy</div>
        <p>With over 15 years of experience...</p>
        <div class="member-expertise">
            <h4>EXPERTISE</h4>
            <div class="expertise-tags">
                <span class="expertise-tag">Real Estate Strategy</span>
                <span class="expertise-tag">NRI Services</span>
            </div>
        </div>
    </div>
</div>
<!-- Repeat for other members -->
```

**Replace with**:
```django
{% for member in team_members %}
<div class="team-member">
    <div class="member-photo">
        {% if member.photo %}
        <img src="{{ member.photo.url }}" alt="{{ member.name }}" style="width: 100%; height: 100%; object-fit: cover;">
        {% else %}
        [Photo]
        {% endif %}
    </div>
    <div class="member-info">
        <h3>{{ member.name }}</h3>
        <div class="member-role">{{ member.department }}</div>
        <p>{{ member.bio }}</p>
        {% if member.get_expertise_list %}
        <div class="member-expertise">
            <h4>EXPERTISE</h4>
            <div class="expertise-tags">
                {% for exp in member.get_expertise_list %}
                <span class="expertise-tag">{{ exp }}</span>
                {% endfor %}
            </div>
        </div>
        {% endif %}
    </div>
</div>
{% empty %}
<p style="text-align: center;">No team members available.</p>
{% endfor %}
```

#### 2. Expertise Areas Section
**Find this**:
```html
<div class="expertise-card">
    <h3>Real Estate Transactions</h3>
    <p>Comprehensive knowledge of Chennai real estate market...</p>
</div>
<!-- Repeat for other areas -->
```

**Replace with**:
```django
{% for area in expertise_areas %}
<div class="expertise-card">
    <h3>{{ area.title }}</h3>
    <p>{{ area.description }}</p>
</div>
{% empty %}
<div class="expertise-card">
    <h3>Real Estate Transactions</h3>
    <p>Comprehensive knowledge of Chennai real estate market...</p>
</div>
{% endfor %}
```

#### 3. Footer
Copy the footer from `services.html`

---

## 📋 Page 3: contact.html

### Variables Available in View
From `content/views.py` → `contact()` function:
- `company` - CompanyInfo object

### What to Replace

#### 1. Contact Form
**Find this**:
```html
<form action="#" method="POST">
```

**Replace with**:
```django
<form action="{% url 'contact' %}" method="POST">
    {% csrf_token %}
    
    {% if messages %}
    <div style="margin-bottom: 1.5rem;">
        {% for message in messages %}
        <div style="padding: 1rem; background: {% if message.tags == 'success' %}#10B981{% else %}#EF4444{% endif %}; color: white; margin-bottom: 0.5rem;">
            {{ message }}
        </div>
        {% endfor %}
    </div>
    {% endif %}
```

**Note**: Add `{% csrf_token %}` right after the opening `<form>` tag!

#### 2. Office Information
**Find this**:
```html
<div class="office-block">
    <h3>India Office — Chennai</h3>
    <p>No. 30, 3rd Floor</p>
    <p>SSR Pankajam Towers</p>
    <!-- etc -->
</div>
```

**Replace with**:
```django
<div class="office-block">
    <h3>India Office — {{ company.india_office_city|default:"Chennai" }}</h3>
    {% if company %}
    <p>{{ company.india_office_address|linebreaks }}</p>
    <p>{{ company.india_office_city }}, {{ company.india_office_state }} - {{ company.india_office_pincode }}</p>
    <p style="margin-top: 1rem;">
        <strong>Phone:</strong><br>
        {{ company.india_phone_1 }}<br>
        {% if company.india_phone_2 %}{{ company.india_phone_2 }}<br>{% endif %}
        {% if company.india_phone_3 %}{{ company.india_phone_3 }}{% endif %}
    </p>
    {% else %}
    <p>No. 30, 3rd Floor</p>
    <p>SSR Pankajam Towers</p>
    <!-- Keep existing hardcoded content as fallback -->
    {% endif %}
</div>
```

Do the same for US Office section.

#### 3. Quick Contact Phone Numbers
**Find this**:
```html
<div class="phone-card">
    <h3>Chennai Office</h3>
    <a href="tel:+918667020798">+91 86670 20798</a>
</div>
```

**Replace with**:
```django
{% if company %}
<div class="phone-card">
    <h3>Chennai Office</h3>
    <a href="tel:{{ company.india_phone_1|cut:' '|cut:'+' }}">{{ company.india_phone_1 }}</a>
</div>
{% if company.india_phone_2 %}
<div class="phone-card">
    <h3>Chennai Office</h3>
    <a href="tel:{{ company.india_phone_2|cut:' '|cut:'+' }}">{{ company.india_phone_2 }}</a>
</div>
{% endif %}
<div class="phone-card">
    <h3>US Office</h3>
    <a href="tel:{{ company.us_phone|cut:' '|cut:'+' }}">{{ company.us_phone }}</a>
</div>
{% else %}
<!-- Keep existing hardcoded phones as fallback -->
{% endif %}
```

#### 4. Footer
Copy the footer from `services.html`

---

## 🔍 Testing Your Changes

### After Each Update:

1. **Save the file**

2. **Refresh the page** in browser:
   - About: http://localhost:8000/en/about/
   - Management: http://localhost:8000/en/management/
   - Contact: http://localhost:8000/en/contact/

3. **Check if**:
   - Content displays correctly
   - No errors in browser console
   - Fallback content shows if data is missing

4. **Test in Admin**:
   - Go to http://localhost:8000/en/admin/
   - Edit a service/team member/value
   - Refresh the page
   - See if changes appear!

---

## 💡 Tips

### Common Mistakes to Avoid:

1. **Forgetting closing tags**:
   ```django
   {% for item in items %}  <!-- Must close with {% endfor %} -->
   {% if condition %}       <!-- Must close with {% endif %} -->
   ```

2. **Wrong variable names**:
   - Check `content/views.py` for exact variable names
   - Case-sensitive: `company` not `Company`

3. **Missing CSRF token**:
   - Always add `{% csrf_token %}` in forms

4. **Linebreaks filter**:
   - Use `{{ text|linebreaks }}` to convert newlines to `<br>` tags

### Useful Filters:

```django
{{ text|upper }}           <!-- UPPERCASE -->
{{ text|lower }}           <!-- lowercase -->
{{ text|title }}           <!-- Title Case -->
{{ text|linebreaks }}      <!-- Convert \n to <br> -->
{{ text|default:"N/A" }}   <!-- Show "N/A" if empty -->
{{ text|cut:" " }}         <!-- Remove spaces -->
```

---

## 📞 Need Help?

If you get stuck:

1. **Check the services.html** - It's your reference
2. **Look at the view** - `content/views.py` shows what variables are available
3. **Check the model** - `content/models.py` shows what fields exist
4. **Test in admin** - Make sure data exists in database

---

## ✅ Checklist

- [ ] Update `about.html`
  - [ ] Mission section with company data
  - [ ] Stats loop
  - [ ] Values loop
  - [ ] Footer with company data

- [ ] Update `management.html`
  - [ ] Team members loop
  - [ ] Expertise areas loop
  - [ ] Footer with company data

- [ ] Update `contact.html`
  - [ ] Form with CSRF token
  - [ ] Office information with company data
  - [ ] Phone numbers with company data
  - [ ] Footer with company data

- [ ] Test all pages
  - [ ] About page loads
  - [ ] Management page loads
  - [ ] Contact form works
  - [ ] All data displays correctly

---

**When you're done, let me know and I'll update the blog.html page!**

Good luck, Viji! You've got this! 🚀

