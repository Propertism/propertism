/**
 * GA4 Conversion Analytics — Propertism
 * Property: G-WZCH8BV34J
 *
 * Tracks: whatsapp_click, phone_call_click, contact_form_submit,
 *         resource_hub_click, newsletter_subscribe
 *
 * Each event captures: page_url, page_type, service_intent, city_context, timestamp
 */
(function () {
  "use strict";

  // ── Page context ────────────────────────────────────────────────────────────
  var body = document.body;
  var PAGE_CONTEXT = {
    page_url:       window.location.href,
    page_type:      body.dataset.intentType || body.dataset.pageType || "static",
    service_intent: body.dataset.intentSlug || body.dataset.intent  || "",
    city_context:   body.dataset.citySlug   || body.dataset.city    || "",
  };

  function fire(eventName, extra) {
    if (typeof gtag !== "function") return;
    gtag("event", eventName, Object.assign({}, PAGE_CONTEXT, {
      event_timestamp: new Date().toISOString(),
    }, extra || {}));
  }

  // ── 1. WhatsApp click ───────────────────────────────────────────────────────
  document.addEventListener("click", function (e) {
    var el = e.target.closest("a[href*='wa.me'], a[href*='whatsapp'], #floating-whatsapp, .floating-wa, [data-whatsapp]");
    if (!el) return;
    fire("whatsapp_click", { link_url: el.href || "" });
  });

  // ── 2. Phone call click ──────────────────────────────────────────────────────
  document.addEventListener("click", function (e) {
    var el = e.target.closest("a[href^='tel:']");
    if (!el) return;
    fire("phone_call_click", { phone_number: el.href.replace("tel:", "") });
  });

  // ── 3. Contact / lead form submit ───────────────────────────────────────────
  document.addEventListener("submit", function (e) {
    var form = e.target;
    if (!form || form.tagName !== "FORM") return;
    // Match lead forms, contact forms, NRI assist forms
    var isLead = form.matches(
      "#lead-form, .lead-form, #contact-form, .contact-form, " +
      "[data-form='lead'], [data-form='contact'], .js-lead-form"
    );
    if (!isLead) return;
    var formType = form.dataset.form || form.id || "contact";
    fire("contact_form_submit", { form_type: formType });
  });

  // ── 4. Resource hub click ────────────────────────────────────────────────────
  document.addEventListener("click", function (e) {
    var el = e.target.closest(
      "a[href*='/blog/'], a[href*='/resources/'], a[href*='/guides/'], " +
      "[data-track='resource'], .resource-link, .blog-card a"
    );
    if (!el) return;
    fire("resource_hub_click", { resource_url: el.href || "" });
  });

  // ── 5. Newsletter subscribe ──────────────────────────────────────────────────
  document.addEventListener("submit", function (e) {
    var form = e.target;
    if (!form || form.tagName !== "FORM") return;
    if (!form.matches("#newsletter-form, .newsletter-form, [data-form='newsletter']")) return;
    fire("newsletter_subscribe", {});
  });

})();
