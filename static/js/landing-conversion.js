/**
 * Landing Page Conversion Engine
 * WhatsApp Lead Funnel + Smart Chatbot
 */

// Configuration
const WHATSAPP_CONFIG = {
    phone: '918667020798',
    defaultMessage: 'Hi, I am interested in properties in Chennai. Please share details.'
};

// Get page context from data attributes
function getPageContext() {
    const body = document.body;
    return {
        city: body.dataset.city || 'Chennai',
        intent: body.dataset.intent || 'properties',
        citySlug: body.dataset.citySlug || 'chennai',
        intentSlug: body.dataset.intentSlug || ''
    };
}

// Generate dynamic WhatsApp message based on context
function generateWhatsAppMessage(city, intent) {
    const intentText = intent.replace(/-/g, ' ');
    
    // Intent-specific message variants
    const messageVariants = {
        'flats for sale': `Hi, I'm looking to buy flats in ${city}. Please share best available options.`,
        'villas for sale': `Hi, I'm interested in villa options in ${city}. Please share details.`,
        'flats under 50 lakhs': `Hi, I'm looking for flats under 50 lakhs in ${city}. Please share options.`,
        'luxury apartments': `Hi, I'm interested in luxury apartments in ${city}. Please share premium options.`,
        'gated community flats': `Hi, I'm looking for flats in gated communities in ${city}. Please share details.`,
        'flats for rent': `Hi, I'm looking for rental flats in ${city}. Please share available options.`,
        'villas for rent': `Hi, I'm interested in renting a villa in ${city}. Please share details.`,
        '2 bhk flats': `Hi, I'm looking for 2 BHK flats in ${city}. Please share options.`,
        '3 bhk flats': `Hi, I'm looking for 3 BHK flats in ${city}. Please share options.`,
        'ready to move flats': `Hi, I'm looking for ready to move flats in ${city}. Please share immediate possession options.`
    };
    
    return messageVariants[intentText] || `Hi, I'm interested in ${intentText} in ${city}. Please share best available options.`;
}

// Open WhatsApp with pre-filled message
function openWhatsApp(customMessage = null) {
    const context = getPageContext();
    const message = customMessage || generateWhatsAppMessage(context.city, context.intent);
    const url = `https://wa.me/${WHATSAPP_CONFIG.phone}?text=${encodeURIComponent(message)}`;
    
    // Track conversion
    if (typeof gtag !== 'undefined') {
        gtag('event', 'whatsapp_click', {
            'event_category': 'conversion',
            'event_label': context.intent
        });
    }
    
    window.open(url, '_blank');
}

// Chatbot State
let chatbotVisible = false;
let chatbotTriggered = false;

// Show chatbot prompt
function showBotPrompt() {
    if (chatbotTriggered) return;
    chatbotTriggered = true;
    
    const context = getPageContext();
    const intentText = context.intent.replace(/-/g, ' ');
    
    const chatbot = document.getElementById('smart-chatbot');
    if (!chatbot) return;
    
    chatbot.classList.add('visible');
    chatbotVisible = true;
    
    // Render initial message
    const prompt = `Looking for ${intentText} in ${context.city}?`;
    renderBotMessage(prompt, [
        { text: 'Under 50L', value: 'budget_50l' },
        { text: '2 BHK', value: '2bhk' },
        { text: '3 BHK', value: '3bhk' },
        { text: 'Talk to Expert', value: 'expert' }
    ]);
}

// Render bot message with options
function renderBotMessage(message, options = []) {
    const chatMessages = document.getElementById('chat-messages');
    if (!chatMessages) return;
    
    // Add bot message
    const messageDiv = document.createElement('div');
    messageDiv.className = 'bot-message';
    messageDiv.innerHTML = `
        <div class="message-bubble bot">
            <p>${message}</p>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    
    // Add options if provided
    if (options.length > 0) {
        const optionsDiv = document.createElement('div');
        optionsDiv.className = 'bot-options';
        options.forEach(option => {
            const btn = document.createElement('button');
            btn.className = 'bot-option-btn';
            btn.textContent = option.text;
            btn.onclick = () => handleBotOption(option.text, option.value);
            optionsDiv.appendChild(btn);
        });
        chatMessages.appendChild(optionsDiv);
    }
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Add user message
function addUserMessage(message) {
    const chatMessages = document.getElementById('chat-messages');
    if (!chatMessages) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'user-message';
    messageDiv.innerHTML = `
        <div class="message-bubble user">
            <p>${message}</p>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Handle bot option click
function handleBotOption(optionText, optionValue) {
    // Remove all option buttons
    const optionsDiv = document.querySelector('.bot-options');
    if (optionsDiv) optionsDiv.remove();
    
    // Add user message
    addUserMessage(optionText);
    
    // Handle response
    setTimeout(() => {
        if (optionValue === 'expert') {
            renderBotMessage("Great! Let me connect you with our property expert on WhatsApp.");
            setTimeout(() => {
                openWhatsApp();
            }, 1000);
        } else if (optionValue === 'budget_50l') {
            renderBotMessage("Perfect! I'll show you properties under 50 lakhs. Let me connect you with our expert for the best deals.");
            setTimeout(() => {
                const context = getPageContext();
                openWhatsApp(`Hi, I'm looking for properties under 50 lakhs in ${context.city}. Please share options.`);
            }, 1500);
        } else if (optionValue === '2bhk' || optionValue === '3bhk') {
            const bhk = optionValue === '2bhk' ? '2 BHK' : '3 BHK';
            renderBotMessage(`Got it! Looking for ${bhk} options. Let me connect you with our expert.`);
            setTimeout(() => {
                const context = getPageContext();
                openWhatsApp(`Hi, I'm looking for ${bhk} flats in ${context.city}. Please share options.`);
            }, 1500);
        }
    }, 500);
}

// Close chatbot
function closeChatbot() {
    const chatbot = document.getElementById('smart-chatbot');
    if (chatbot) {
        chatbot.classList.remove('visible');
        chatbotVisible = false;
    }
}

// Toggle chatbot
function toggleChatbot() {
    if (chatbotVisible) {
        closeChatbot();
    } else {
        showBotPrompt();
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Auto-trigger chatbot after 5 seconds
    setTimeout(() => {
        showBotPrompt();
    }, 5000);
    
    // Bind WhatsApp button clicks
    document.querySelectorAll('.whatsapp-cta').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const customMessage = this.dataset.message;
            openWhatsApp(customMessage);
        });
    });
    
    // Floating button click
    const floatingBtn = document.getElementById('floating-whatsapp');
    if (floatingBtn) {
        floatingBtn.addEventListener('click', function(e) {
            e.preventDefault();
            openWhatsApp();
        });
    }
    
    // Chatbot close button
    const closeBtn = document.getElementById('close-chatbot');
    if (closeBtn) {
        closeBtn.addEventListener('click', closeChatbot);
    }
});

// Expose functions globally
window.openWhatsApp = openWhatsApp;
window.toggleChatbot = toggleChatbot;
window.closeChatbot = closeChatbot;
