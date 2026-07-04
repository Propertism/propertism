/* realBOT Sliding Panel - JavaScript Controller (Polished UI & API Integration) */
(function() {
    'use strict';

    // Global state
    let panelInstance = null;
    let overlayInstance = null;
    let isInitialized = false;
    let dbProperties = [];
    let sessionId = null;
    let messages = [];

    // Initialize triggers
    function init() {
        // Create trigger FAB if it doesn't exist
        if (!document.getElementById('realbotTriggerWrapper')) {
            const triggerHTML = `
                <div class="realbot-trigger-wrapper" id="realbotTriggerWrapper">
                    <div class="realbot-ripple-ring ring-1"></div>
                    <div class="realbot-ripple-ring ring-2"></div>
                    <div class="realbot-ripple-ring ring-3"></div>
                    <button class="realbot-trigger-btn" id="realbotTriggerBtn" aria-label="Open realBOT" title="Open realBOT AI Workspace">
                        <svg width="30" height="30" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M22 45 L50 21 L78 45" stroke="#C89B2B" stroke-width="6" stroke-linecap="square" />
                            <path d="M49 13 L86 38" stroke="#C89B2B" stroke-width="6" stroke-linecap="square" />
                            <path d="M30 46 L46 46 M38 46 L38 80" stroke="#C89B2B" stroke-width="6" stroke-linecap="square" />
                            <path d="M54 46 L54 80 M54 46 H68 C74 46 76 50 76 56 C76 62 74 65 68 65 H54" stroke="#C89B2B" stroke-width="6" stroke-linecap="square" />
                        </svg>
                    </button>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', triggerHTML);
        }

        // Set teaser tooltip and handle teaser behavior globally (Coming Soon)
        const triggerBtn = document.getElementById('realbotTriggerBtn');
        if (triggerBtn) {
            triggerBtn.setAttribute('title', 'realBOT AI Advisor (Coming Soon)');
            triggerBtn.setAttribute('aria-label', 'realBOT AI Advisor (Coming Soon)');
            triggerBtn.addEventListener('click', showComingSoonToast);
        }

        // Global ESC key listener to close panel
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closePanel();
            }
        });

        // Read dynamic properties from base template if available
        try {
            const propsEl = document.getElementById('featured-properties-data');
            if (propsEl) {
                const parsed = JSON.parse(propsEl.textContent || propsEl.innerText);
                if (parsed && Array.isArray(parsed)) {
                    dbProperties = parsed;
                }
            }
        } catch (e) {
            console.log('Failed to parse database properties for realBOT', e);
        }
    }

    // Lazy load markup into DOM
    function ensurePanelInDOM() {
        if (isInitialized) return;

        const template = document.getElementById('realbot-panel-template');
        if (!template) return;

        // Insert wrapper overlay and panel HTML
        document.body.insertAdjacentHTML('beforeend', template.innerHTML);
        
        panelInstance = document.getElementById('realbotPanel');
        overlayInstance = document.getElementById('realbotOverlay');

        // Setup event handlers inside the panel
        overlayInstance.addEventListener('click', closePanel);
        document.getElementById('realbotCloseBtn').addEventListener('click', closePanel);
        document.getElementById('realbotSendBtn').addEventListener('click', handleSendAction);
        
        // Textarea Keyboard listeners (Enter to Send, Shift+Enter to newline)
        const textarea = document.getElementById('realbotInput');
        textarea.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSendAction();
            }
        });

        // Initialize session on first load
        initializeSession();

        isInitialized = true;
    }

    // Initialize or load existing session from sessionStorage
    function initializeSession() {
        // Check sessionStorage
        sessionId = sessionStorage.getItem('realbot_session_id');
        
        let url = '/chat/session/init/';
        if (sessionId) {
            url += '?session_id=' + encodeURIComponent(sessionId);
        }

        fetch(url)
            .then(response => {
                if (!response.ok) throw new Error("Session init failed");
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    sessionId = data.session_id;
                    sessionStorage.setItem('realbot_session_id', sessionId);
                    messages = data.messages;
                    renderMessages();
                }
            })
            .catch(error => {
                console.error("Error initializing realBOT session:", error);
                // Fallback local greeting if server fails
                messages = [{
                    id: Date.now(),
                    sender: 'assistant',
                    time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                    text: "Welcome to **realBOT** (advisory channel). Session synchronization failed, but I am ready to advise you locally.",
                    metadata: {
                        chips: ['Luxury Villas', 'Apartments', 'NRI Investment']
                    }
                }];
                renderMessages();
            });
    }

    // Show elegant Coming Soon teaser toast message
    function showComingSoonToast() {
        if (document.getElementById('realbotComingSoonToast')) return;

        const toast = document.createElement('div');
        toast.id = 'realbotComingSoonToast';
        toast.className = 'realbot-coming-soon-toast';
        toast.innerText = 'realBOT AI Advisor is coming soon to Propertism NRI clients.';
        
        if (!document.getElementById('realbotToastStyles')) {
            const style = document.createElement('style');
            style.id = 'realbotToastStyles';
            style.textContent = `
                .realbot-coming-soon-toast {
                    position: fixed;
                    bottom: 96px;
                    right: 24px;
                    background-color: #0E2A47;
                    color: #FFFFFF;
                    border: 1px solid #C89B2B;
                    padding: 12px 20px;
                    font-family: 'Inter', sans-serif;
                    font-size: 11px;
                    font-weight: 600;
                    letter-spacing: 0.03em;
                    text-transform: uppercase;
                    box-shadow: 0 4px 12px rgba(14, 42, 71, 0.2);
                    opacity: 0;
                    transform: translateY(10px);
                    transition: opacity 300ms ease, transform 300ms ease;
                    z-index: 9999;
                }
                .realbot-coming-soon-toast.show {
                    opacity: 1;
                    transform: translateY(0);
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(toast);

        // Force reflow
        toast.offsetHeight;

        // Show toast
        toast.classList.add('show');

        // Hide and remove after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 3000);
    }

    // Toggle sliding panel
    function togglePanel() {
        ensurePanelInDOM();
        if (panelInstance.classList.contains('active')) {
            closePanel();
        } else {
            openPanel();
        }
    }

    function openPanel() {
        ensurePanelInDOM();
        overlayInstance.classList.add('active');
        panelInstance.classList.add('active');
        const wrapper = document.getElementById('realbotTriggerWrapper');
        if (wrapper) wrapper.classList.add('hidden'); // Hide wrapper containing ripples
        
        // Focus input
        setTimeout(() => {
            const input = document.getElementById('realbotInput');
            if (input) input.focus();
        }, 320);
    }

    function closePanel() {
        if (!isInitialized) return;
        overlayInstance.classList.remove('active');
        panelInstance.classList.remove('active');
        const wrapper = document.getElementById('realbotTriggerWrapper');
        if (wrapper) wrapper.classList.remove('hidden'); // Show wrapper containing ripples
    }

    // Scroll chat scroll area to base
    function scrollToBottom() {
        const area = document.getElementById('realbotChatArea');
        if (area) area.scrollTop = area.scrollHeight;
    }

    // Render conversation list
    function renderMessages() {
        const area = document.getElementById('realbotChatArea');
        if (!area) return;

        area.innerHTML = '';

        messages.forEach(msg => {
            const now = msg.time || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            
            const renderTextWithBold = (txt) => {
                const parts = txt.split('**');
                return parts.map((part, idx) => (idx % 2 === 1 ? `<strong class="font-bold text-navy">${part}</strong>` : part)).join('');
            };

            const paragraphs = msg.text.split('\n\n').map(p => {
                if (p.startsWith('### ')) {
                    return `<h3 class="text-[11px] font-bold text-navy uppercase tracking-wider mt-4 first:mt-0 font-sans border-b border-navy/5 pb-1">${p.replace('### ', '')}</h3>`;
                }
                return `<p class="text-xs text-gray-600">${renderTextWithBold(p)}</p>`;
            }).join('');

            // Render property card
            let propertyCardHTML = '';
            if (msg.metadata && msg.metadata.property) {
                const prop = msg.metadata.property;
                propertyCardHTML = `
                    <div class="border border-navy/10 bg-white flex flex-col relative mt-3 select-none">
                        <div class="relative w-full aspect-[16/10] overflow-hidden bg-secondaryBg">
                            <img src="${prop.imageUrl}" alt="${prop.name}" class="w-full h-full object-cover" />
                            <div class="absolute top-0 left-0 bg-gold text-white text-[8px] font-bold tracking-widest uppercase px-2.5 py-1 font-sans">
                                ${prop.badge || 'EXCLUSIVE PORTFOLIO'}
                            </div>
                        </div>
                        <div class="p-4 flex flex-col justify-between bg-white text-left">
                            <div>
                                <div class="flex justify-between items-start gap-2 mb-2">
                                    <div>
                                        <h4 class="text-xs font-bold text-navy font-sans tracking-tight uppercase leading-tight">${prop.name}</h4>
                                        <p class="text-[9px] text-gray-500 font-sans tracking-wide mt-0.5">${prop.location}</p>
                                    </div>
                                    <div class="text-xs font-bold text-gold font-sans whitespace-nowrap">${prop.price}</div>
                                </div>
                                
                                <hr class="border-t border-navy/5 my-2.5" />
                                
                                <div class="grid grid-cols-3 gap-2 text-left mb-3">
                                    <div class="border-r border-navy/5 pr-1.5">
                                        <span class="block text-[7px] uppercase tracking-wider text-gray-400 font-sans">Config</span>
                                        <span class="block text-[9px] font-semibold text-navy truncate font-sans">${prop.config}</span>
                                    </div>
                                    <div class="border-r border-navy/5 px-1.5">
                                        <span class="block text-[7px] uppercase tracking-wider text-gray-400 font-sans">Area</span>
                                        <span class="block text-[9px] font-semibold text-navy truncate font-sans">${prop.area}</span>
                                    </div>
                                    <div class="pl-1.5">
                                        <span class="block text-[7px] uppercase tracking-wider text-gray-400 font-sans">Builder</span>
                                        <span class="block text-[9px] font-semibold text-navy truncate font-sans">${prop.builder}</span>
                                    </div>
                                </div>
                                
                                <div class="mb-1">
                                    <span class="block text-[7px] uppercase tracking-wider text-gray-400 font-sans mb-1">Highlights</span>
                                    <div class="flex flex-wrap gap-1">
                                        ${prop.highlights.map(h => `<span class="text-[8px] font-medium text-navy bg-secondaryBg border border-navy/5 px-2 py-0.5 uppercase tracking-wider font-sans whitespace-nowrap">${h}</span>`).join('')}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }

            // Tabular comparisons
            let tableHTML = '';
            if (msg.metadata && msg.metadata.comparison) {
                const comp = msg.metadata.comparison;
                tableHTML = `
                    <div class="border border-navy/10 mt-3 overflow-x-auto">
                        <table class="w-full text-left text-[11px] font-sans">
                            <thead>
                                <tr class="bg-secondaryBg border-b border-navy/10 font-bold text-navy">
                                    ${comp.headers.map(h => `<th class="p-2 uppercase tracking-wider text-[8px]">${h}</th>`).join('')}
                                </tr>
                            </thead>
                            <tbody>
                                ${comp.rows.map(row => `
                                    <tr class="border-b border-navy/5 bg-white last:border-0">
                                        ${row.map((cell, idx) => `
                                            <td class="p-2 ${idx === 0 ? 'font-semibold' : 'text-gray-600 font-medium'}">${cell}</td>
                                        `).join('')}
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                `;
            }

            // Citations block
            let citationsHTML = '';
            if (msg.metadata && msg.metadata.citations && msg.metadata.citations.length > 0) {
                citationsHTML = `
                    <div class="pt-2 border-t border-navy/5 text-[9px] text-gray-400 italic flex flex-col gap-0.5 font-sans">
                        ${msg.metadata.citations.map(cite => `<span>${cite}</span>`).join('')}
                    </div>
                `;
            }

            // Error styling
            const isError = msg.sender === 'error';
            const bodyBg = isError ? 'bg-red-50/70 border-red-200' : 'bg-white border-navy/10';
            const headerLabel = isError ? 'SYSTEM ERROR' : (msg.sender === 'user' ? 'CLIENT CONSULTANT' : 'realBOT ADVISOR');

            const msgHTML = `
                <div class="flex flex-col mb-4 select-text">
                    <div class="flex justify-between items-center text-[9px] text-gray-400 font-semibold tracking-wider uppercase mb-1.5 px-1 font-sans select-none">
                        <span>${headerLabel}</span>
                        <span>${now}</span>
                    </div>
                    <div class="${bodyBg} border p-5 text-xs font-sans text-gray-800 space-y-3">
                        ${paragraphs}
                        ${propertyCardHTML}
                        ${tableHTML}
                        ${citationsHTML}
                    </div>
                </div>
            `;
            area.insertAdjacentHTML('beforeend', msgHTML);
        });

        // Load chips for last response dynamically
        const lastMsg = messages[messages.length - 1];
        const chips = (lastMsg && lastMsg.metadata) ? lastMsg.metadata.chips : [];
        renderSuggestionChips(chips || []);
        
        scrollToBottom();
    }

    // Render suggestion chips dynamically
    function renderSuggestionChips(chipsArray) {
        const chipsContainer = document.getElementById('realbotChipsContainer');
        if (!chipsContainer) return;

        chipsContainer.innerHTML = '';
        
        if (!chipsArray || chipsArray.length === 0) {
            chipsContainer.parentElement.classList.add('hidden');
            return;
        }

        chipsContainer.parentElement.classList.remove('hidden');

        chipsArray.forEach(chip => {
            const btnHTML = `
                <button onclick="window.realbotControl.triggerChip('${chip}')" class="realbot-chip">
                    ${chip}
                </button>
            `;
            chipsContainer.insertAdjacentHTML('beforeend', btnHTML);
        });
    }

    // Handle Send Button or Enter
    function handleSendAction() {
        const inputEl = document.getElementById('realbotInput');
        const text = inputEl.value.trim();
        if (!text) return;

        inputEl.value = '';
        triggerResponseSequence(text);
    }

    // AJAX call to submit queries to Django endpoint
    function triggerResponseSequence(text) {
        // Save user message locally first
        const userMsg = {
            id: Date.now(),
            sender: 'user',
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            text: text
        };
        messages.push(userMsg);
        renderMessages();

        // Show typing indicator
        const indicator = document.getElementById('realbotTypingIndicator');
        if (indicator) indicator.classList.remove('hidden');
        scrollToBottom();

        // Clear chips while calling API
        renderSuggestionChips([]);

        // Send POST request to REST backend
        fetch('/chat/query/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Optional: Django CSRF token from cookie if available
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                session_id: sessionId,
                message: text
            })
        })
        .then(response => {
            if (!response.ok) throw new Error("Query processing failed");
            return response.json();
        })
        .then(data => {
            if (indicator) indicator.classList.add('hidden');
            if (data.success) {
                messages.push(data.message);
                renderMessages();
            } else {
                showAPIError(data.error || "The advisor is currently offline. Please try again.");
            }
        })
        .catch(error => {
            console.error("Error posting realBOT query:", error);
            if (indicator) indicator.classList.add('hidden');
            showAPIError("Connection failure. Check your internet connection and try again.");
        });
    }

    // Helper to render user friendly system errors inside conversational flow
    function showAPIError(errMsg) {
        messages.push({
            id: Date.now(),
            sender: 'error',
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            text: errMsg,
            metadata: {
                chips: ['Premium Villas', 'Apartments', 'NRI Investment']
            }
        });
        renderMessages();
    }

    // Helper to read CSRF Cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Expose control hook triggers on global scope for inline HTML callbacks
    window.realbotControl = {
        triggerChip: function(text) {
            triggerResponseSequence(text);
        }
    };

    // Auto-init on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
