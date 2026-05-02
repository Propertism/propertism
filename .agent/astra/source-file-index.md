# Propertism: Source File Index & Legend

This index serves as the "Source of Truth" for locating HTML templates and CSS modules within the Propertism platform.

## 🗺️ The Legend
| Prefix / Pattern | Meaning |
| :--- | :--- |
| `v4-*.css` | **Active V4 Modules**: The current design system. Use these for all modern styling. |
| `_*.html` | **Template Partials**: Reusable blocks included via `{% include %}`. |
| `sections/_*.html`| **Homepage Modules**: The individual building blocks of the homepage. |
| `v4-tokens.css` | **Global Variables**: Colors, typography, and spacing tokens. |

---

## 🏗️ Homepage Architecture (Order of Appearance)

| Section | Template (HTML) | Stylesheet (CSS) |
| :--- | :--- | :--- |
| **Global Nav** | `components/_header-english.html` | `v4-nav.css` |
| **Hero** | `home/sections/_hero.html` | `v4-hero.css` |
| **Trust Strip** | `home/sections/_trust_strip.html` | `v4-trust-strip.css` |
| **Services** | `home/sections/_services.html` | `v4-services.css` |
| **About** | `home/sections/_about.html` | `v4-about.css` |
| **Management** | `home/sections/_management.html` | `v4-management.css` |
| **Reviews** | `home/sections/_reviews.html` | `v4-reviews.css` |
| **Properties** | `home/sections/_properties.html` | `v4-properties.css` |
| **Insights (Blog)**| `home/sections/_insights.html` | `v4-insights.css` |
| **Contact** | `home/sections/_contact.html` | `v4-contact.css` |
| **Custom Cards** | `home/sections/_custom_cards.html` | `v4-custom-cards.css` |
| **Global Footer** | `components/_footer.html` | `v4-footer.css` |

---

## 📄 Page Layouts (Main Containers)

| Page | Template (HTML) |
| :--- | :--- |
| **Master Base** | `base.html` |
| **Homepage** | `home-premium.html` |
| **Property Detail**| `properties/detail.html` |
| **Team Member** | `team_member_detail.html` |
| **Management Page**| `management.html` |

---

## 🛠️ Design System Modules

| File Path | Description |
| :--- | :--- |
| `static/css/v4-tokens.css` | Brand colors (#0F172A, #B89A4A), typography profiles. |
| `static/css/viewport-section-normalization.css` | Enforces 100vh Hero/Trust Strip and global section density. |
| `static/css/mobile-layout.css` | Global responsive overrides. |

---

## 🗄️ Backend Models (Data Source)

| Feature | Model File |
| :--- | :--- |
| **Company Info / Socials** | `content/models.py` (CompanyInfo) |
| **Featured Properties** | `properties/models.py` (Property) |
| **Testimonials** | `content/models.py` (Review) |
| **Stats / Trust Strip** | `content/models.py` (Stat) |
| **Team Members** | `content/models.py` (TeamMember) |

---
*Maintained by Astra | 2026-05-02*
