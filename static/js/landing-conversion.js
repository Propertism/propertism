/**
 * Landing Page Conversion Engine
 * Lead funnel + WhatsApp support + GA4-ready event tracking
 */

const WHATSAPP_CONFIG = {
    phone: "918667020798",
    defaultMessage: "Hi, I am interested in properties in Chennai. Please share details.",
};

const leadState = {
    started: false,
    currentStep: 1,
    leadId: null,
};

function getPageContext() {
    const body = document.body;
    return {
        city: body.dataset.city || "Chennai",
        intent: body.dataset.intent || "properties",
        citySlug: body.dataset.citySlug || "chennai",
        intentSlug: body.dataset.intentSlug || "",
        intentType: body.dataset.intentType || "buy",
        geoOrigin: body.dataset.nriOrigin || "",
        pagePath: body.dataset.pagePath || window.location.pathname,
    };
}

function trackLandingEvent(eventName, extraPayload = {}) {
    if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
        console.log("[landing-track-bypass] Local development:", eventName, extraPayload);
        return;
    }
    const context = getPageContext();
    const payload = {
        intent_type: context.intentType,
        geo_origin: context.geoOrigin || "domestic",
        page_path: context.pagePath,
        ...extraPayload,
    };

    console.info(`[landing-track] ${eventName}`, payload);

    if (typeof gtag !== "undefined") {
        gtag("event", eventName, payload);
    }
}

function generateWhatsAppMessage(city, intent) {
    const intentText = intent.replace(/-/g, " ");
    return `Hi, I'm interested in ${intentText} in ${city}. Please share more details.`;
}

function openWhatsApp(customMessage = null) {
    const context = getPageContext();
    const message = customMessage || generateWhatsAppMessage(context.city, context.intent);
    const url = `https://wa.me/${WHATSAPP_CONFIG.phone}?text=${encodeURIComponent(message)}`;

    trackLandingEvent("cta_click", {
        cta_label: "WhatsApp",
        cta_target: "whatsapp",
    });

    window.open(url, "_blank");
}

function getLeadForm() {
    return document.getElementById("landing-lead-form-element");
}

function getLeadSection() {
    return document.getElementById("landing-lead-form");
}

function getIntentFieldBlocks() {
    return document.querySelectorAll("[data-intent-fields]");
}

function setLeadStep(step) {
    leadState.currentStep = step;
    document.querySelectorAll(".lead-form-step").forEach((panel) => {
        panel.hidden = panel.dataset.step !== String(step);
    });
    if (step !== "followup") {
        document.querySelectorAll("[data-step-indicator]").forEach((indicator) => {
            indicator.classList.toggle("is-active", indicator.dataset.stepIndicator === String(step));
        });
    }
}

function clearLeadErrors(form) {
    form.querySelectorAll("[data-error-for]").forEach((node) => {
        node.textContent = "";
    });
    const feedback = form.querySelector("[data-feedback]");
    if (feedback) {
        feedback.hidden = true;
        feedback.className = "lead-form-feedback";
        feedback.textContent = "";
    }
}

function showLeadErrors(form, errors = {}) {
    Object.entries(errors).forEach(([field, message]) => {
        const errorNode = form.querySelector(`[data-error-for="${field}"]`);
        if (errorNode) {
            errorNode.textContent = message;
        }
    });
}

function showLeadFeedback(form, message, kind = "success") {
    const feedback = form.querySelector("[data-feedback]");
    if (!feedback) return;
    feedback.hidden = false;
    feedback.className = `lead-form-feedback is-${kind}`;
    feedback.textContent = message;
}

function updateIntentSpecificFields() {
    const form = getLeadForm();
    if (!form) return;

    const context = getPageContext();
    getIntentFieldBlocks().forEach((block) => {
        block.hidden = block.dataset.intentFields !== context.intentType;
    });
}

function openLeadForm(source = "cta", ctaLabel = "Get Property Valuation") {
    const section = getLeadSection();
    const form = getLeadForm();
    if (!section || !form) return;

    section.hidden = false;
    section.classList.add("is-visible");
    updateIntentSpecificFields();
    setLeadStep(1);
    clearLeadErrors(form);
    section.scrollIntoView({ behavior: "smooth", block: "start" });

    trackLandingEvent("cta_click", {
        cta_label: ctaLabel,
        cta_target: "lead_form",
        cta_source: source,
    });

    if (!leadState.started) {
        trackLandingEvent("lead_form_start", {
            cta_label: ctaLabel,
            cta_source: source,
        });
        leadState.started = true;
        scheduleWhatsAppFallback();
    }
}

function validateStepOne(form) {
    const errors = {};
    const phone = (form.querySelector('[name="phone"]')?.value || "").trim();
    const propertyCity = (form.querySelector('[name="property_city"]')?.value || "").trim();

    if (!phone) {
        errors.phone = "Phone number is required.";
    }
    if (!propertyCity) {
        errors.property_city = "Property city is required.";
    }
    return errors;
}

function nextLeadStep() {
    const form = getLeadForm();
    if (!form) return;

    clearLeadErrors(form);
    const errors = validateStepOne(form);
    if (Object.keys(errors).length > 0) {
        showLeadErrors(form, errors);
        return;
    }

    setLeadStep(2);
    updateIntentSpecificFields();
}

function serializeLeadForm(form) {
    const formData = new FormData(form);
    const context = getPageContext();
    formData.set("intent_type", context.intentType);
    formData.set("geo_origin", context.geoOrigin || "");
    return formData;
}

async function submitLeadForm(event) {
    event.preventDefault();
    const form = event.currentTarget;
    clearLeadErrors(form);

    const submitButton = form.querySelector(".js-lead-submit");
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = "Submitting...";
    }

    try {
        const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]")?.value || "";
        const response = await fetch(form.dataset.endpoint, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "XMLHttpRequest",
            },
            body: serializeLeadForm(form),
        });

        const payload = await response.json();
        if (!response.ok || !payload.ok) {
            showLeadErrors(form, payload.errors || {});
            showLeadFeedback(form, "Please correct the highlighted fields and try again.", "error");
            return;
        }

        leadState.leadId = payload.lead_id;
        trackLandingEvent("lead_form_submit", {
            lead_stage: payload.lead_stage || "qualified",
            lead_score: payload.lead_score || 0,
            lead_category: payload.lead_category || "cold",
        });
        trackLandingEvent("lead_scored", {
            lead_score: payload.lead_score || 0,
            lead_category: payload.lead_category || "cold",
        });
        if (payload.lead_stage === "qualified") {
            trackLandingEvent("lead_qualified", {
                lead_score: payload.lead_score || 0,
                lead_category: payload.lead_category || "cold",
            });
        }

        form.reset();
        const cityField = form.querySelector('[name="property_city"]');
        if (cityField) {
            cityField.value = getPageContext().city;
        }
        updateIntentSpecificFields();

        if (getPageContext().intentType === "sell") {
            setLeadStep("followup");
            showLeadFeedback(form, "One last detail helps us qualify faster.", "success");
        } else {
            setLeadStep(1);
            showLeadFeedback(form, payload.message || "Thanks. We will get back to you shortly.", "success");
        }
    } catch (error) {
        console.error("Landing lead submission failed", error);
        showLeadFeedback(form, "We could not submit your request right now. Please try again.", "error");
    } finally {
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.textContent = submitButton.dataset.defaultLabel || "Get Property Valuation";
        }
    }
}

async function submitLeadFollowup() {
    const form = getLeadForm();
    if (!form || !leadState.leadId) return;

    const priceRange = (document.getElementById("lead-followup-price-range")?.value || "").trim();
    const contactTime = (document.getElementById("lead-followup-contact-time")?.value || "").trim();
    const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]")?.value || "";

    try {
        const response = await fetch("/api/landing-lead/followup/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "XMLHttpRequest",
            },
            body: new URLSearchParams({
                lead_id: leadState.leadId,
                expected_price_range: priceRange,
                preferred_contact_time: contactTime,
            }),
        });

        const payload = await response.json();
        if (!response.ok || !payload.ok) {
            showLeadFeedback(form, "We could not save your preferences. Please try again.", "error");
            return;
        }

        trackLandingEvent("lead_scored", {
            lead_score: payload.lead_score || 0,
            lead_category: payload.lead_category || "cold",
        });

        setLeadStep(1);
        showLeadFeedback(form, payload.message || "Thanks. We saved your preferences.", "success");
    } catch (error) {
        console.error("Landing lead followup failed", error);
        showLeadFeedback(form, "We could not save your preferences. Please try again.", "error");
    }
}

function scheduleWhatsAppFallback() {
    const fallback = document.getElementById("whatsapp-fallback");
    if (!fallback) return;
    setTimeout(() => {
        if (leadState.leadId) {
            return;
        }
        fallback.hidden = false;
        fallback.classList.add("is-visible");
    }, 20000);
}

let chatbotVisible = false;
let chatbotTriggered = false;

function showBotPrompt() {
    if (chatbotTriggered) return;
    chatbotTriggered = true;

    const context = getPageContext();
    const chatbot = document.getElementById("smart-chatbot");
    if (!chatbot) return;

    chatbot.classList.add("visible");
    chatbotVisible = true;

    const prompt = `Looking for ${context.intent.replace(/-/g, " ")} in ${context.city}?`;
    renderBotMessage(prompt, [
        { text: "Under 50L", value: "budget_50l" },
        { text: "2 BHK", value: "2bhk" },
        { text: "3 BHK", value: "3bhk" },
        { text: "Talk to Expert", value: "expert" },
    ]);
}

function renderBotMessage(message, options = []) {
    const chatMessages = document.getElementById("chat-messages");
    if (!chatMessages) return;

    const messageDiv = document.createElement("div");
    messageDiv.className = "bot-message";
    messageDiv.innerHTML = `
        <div class="message-bubble bot">
            <p>${message}</p>
        </div>
    `;
    chatMessages.appendChild(messageDiv);

    if (options.length > 0) {
        const optionsDiv = document.createElement("div");
        optionsDiv.className = "bot-options";
        options.forEach((option) => {
            const btn = document.createElement("button");
            btn.className = "bot-option-btn";
            btn.textContent = option.text;
            btn.onclick = () => handleBotOption(option.text, option.value);
            optionsDiv.appendChild(btn);
        });
        chatMessages.appendChild(optionsDiv);
    }

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addUserMessage(message) {
    const chatMessages = document.getElementById("chat-messages");
    if (!chatMessages) return;

    const messageDiv = document.createElement("div");
    messageDiv.className = "user-message";
    messageDiv.innerHTML = `
        <div class="message-bubble user">
            <p>${message}</p>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function handleBotOption(optionText, optionValue) {
    const optionsDiv = document.querySelector(".bot-options");
    if (optionsDiv) optionsDiv.remove();

    addUserMessage(optionText);

    setTimeout(() => {
        if (optionValue === "expert") {
            renderBotMessage("Great! Let me connect you with our property expert on WhatsApp.");
            setTimeout(() => {
                openWhatsApp();
            }, 1000);
        } else if (optionValue === "budget_50l") {
            renderBotMessage("Perfect! I'll connect you with our expert for budget options.");
            setTimeout(() => {
                const context = getPageContext();
                openWhatsApp(`Hi, I'm looking for properties under 50 lakhs in ${context.city}. Please share options.`);
            }, 1500);
        } else if (optionValue === "2bhk" || optionValue === "3bhk") {
            const bhk = optionValue === "2bhk" ? "2 BHK" : "3 BHK";
            renderBotMessage(`Got it! Looking for ${bhk} options. Let me connect you with our expert.`);
            setTimeout(() => {
                const context = getPageContext();
                openWhatsApp(`Hi, I'm looking for ${bhk} flats in ${context.city}. Please share options.`);
            }, 1500);
        }
    }, 500);
}

function closeChatbot() {
    const chatbot = document.getElementById("smart-chatbot");
    if (chatbot) {
        chatbot.classList.remove("visible");
        chatbotVisible = false;
    }
}

function toggleChatbot() {
    if (chatbotVisible) {
        closeChatbot();
    } else {
        showBotPrompt();
    }
}

document.addEventListener("DOMContentLoaded", () => {
    // Track landing page visit event on page load
    trackLandingEvent("landing_page_visit");

    setTimeout(() => {
        showBotPrompt();
    }, 5000);

    document.querySelectorAll(".js-open-lead-form").forEach((button) => {
        button.addEventListener("click", () => {
            openLeadForm(button.dataset.ctaSource || "cta", button.dataset.ctaLabel || button.textContent.trim());
        });
    });

    document.querySelectorAll(".whatsapp-cta").forEach((button) => {
        button.addEventListener("click", (event) => {
            event.preventDefault();
            openWhatsApp(button.dataset.message || null);
        });
    });

    const nextButton = document.querySelector(".js-lead-next");
    if (nextButton) {
        nextButton.addEventListener("click", nextLeadStep);
    }

    const backButton = document.querySelector(".js-lead-back");
    if (backButton) {
        backButton.addEventListener("click", () => setLeadStep(1));
    }

    const leadForm = getLeadForm();
    if (leadForm) {
        updateIntentSpecificFields();
        leadForm.addEventListener("submit", submitLeadForm);
    }

    const followupButton = document.querySelector(".js-lead-followup-submit");
    if (followupButton) {
        followupButton.addEventListener("click", submitLeadFollowup);
    }

    const skipFollowupButton = document.querySelector(".js-lead-skip-followup");
    if (skipFollowupButton) {
        skipFollowupButton.addEventListener("click", () => {
            const form = getLeadForm();
            if (form) {
                setLeadStep(1);
                showLeadFeedback(form, "Thanks. We will get back to you shortly.", "success");
            }
        });
    }

    const floatingBtn = document.getElementById("floating-whatsapp");
    if (floatingBtn) {
        floatingBtn.addEventListener("click", (event) => {
            event.preventDefault();
            openWhatsApp();
        });
    }

    const closeBtn = document.getElementById("close-chatbot");
    if (closeBtn) {
        closeBtn.addEventListener("click", closeChatbot);
    }
});

window.openWhatsApp = openWhatsApp;
window.toggleChatbot = toggleChatbot;
window.closeChatbot = closeChatbot;
window.openLeadForm = openLeadForm;
