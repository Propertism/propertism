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
            const teaserHTML = `
                <div class="realbot-teaser-bubble" id="realbotTeaserBubble">
                    <div class="logo-group">
                        <svg width="24" height="24" viewBox="0 0 100 100" fill="none" class="shrink-0" xmlns="http://www.w3.org/2000/svg" style="color: #C89B2B;">
                            <path d="M22 45 L50 21 L78 45" stroke="currentColor" stroke-width="7" stroke-linecap="square" />
                            <path d="M49 13 L86 38" stroke="currentColor" stroke-width="7" stroke-linecap="square" />
                            <path d="M30 46 L46 46 M38 46 L38 80" stroke="currentColor" stroke-width="7" stroke-linecap="square" />
                            <path d="M54 46 L54 80 M54 46 H68 C74 46 76 50 76 56 C76 62 74 65 68 65 H54" stroke="currentColor" stroke-width="7" stroke-linecap="square" />
                        </svg>
                        <div class="text-group">
                            <span class="title-text"><span class="realbot-real">real</span><span class="realbot-bot">BOT</span></span>
                            <span class="subtitle-text">by Propertism</span>
                        </div>
                    </div>
                </div>
            `;
            const triggerHTML = `
                <div class="realbot-trigger-wrapper" id="realbotTriggerWrapper">
                    ${teaserHTML}
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

            const teaserBubble = document.getElementById('realbotTeaserBubble');
            if (teaserBubble) {
                teaserBubble.addEventListener('click', function() {
                    togglePanel();
                });
            }
        }

        // Set teaser tooltip and handle teaser behavior globally
        const triggerBtn = document.getElementById('realbotTriggerBtn');
        if (triggerBtn) {
            triggerBtn.setAttribute('title', 'Open realBOT AI Workspace');
            triggerBtn.setAttribute('aria-label', 'Open realBOT');
            triggerBtn.addEventListener('click', togglePanel);
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

    // Initialize or load existing session from sessionStorage or URL query params
    function initializeSession() {
        const urlParams = new URLSearchParams(window.location.search);
        let urlSessionId = urlParams.get('session_id');
        if (urlSessionId) {
            sessionId = urlSessionId;
            sessionStorage.setItem('realbot_session_id', sessionId);
            setTimeout(() => {
                const trigger = document.getElementById('realbotTriggerBtn');
                if (trigger && !panelInstance.classList.contains('active')) {
                    trigger.click();
                }
            }, 500);
        } else {
            sessionId = sessionStorage.getItem('realbot_session_id');
            if (sessionId === 'undefined' || sessionId === 'null') {
                sessionId = null;
                sessionStorage.removeItem('realbot_session_id');
            }
        }
        
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
                if (data.success && data.data) {
                    sessionId = data.data.session_id;
                    sessionStorage.setItem('realbot_session_id', sessionId);
                    messages = data.data.messages || [];
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
                    text: "Welcome to **realBOT** (advisory channel). Connection failed. Please verify that the local server is running and database migrations have been applied.",
                    metadata: {
                        chips: ['Luxury Villas', 'Apartments', 'NRI Investment']
                    }
                }];
                renderMessages();
            });
    }

    // Clear chat session and messages history to start fresh
    function clearChat() {
        if (sessionId) {
            endSessionAndArchive();
        }
        sessionStorage.removeItem('realbot_session_id');
        sessionId = null;
        messages = [];
        initializeSession();
    }

    // Show elegant Coming Soon teaser toast message
    function showComingSoonToast(message) {
        let toast = document.getElementById('realbotComingSoonToast');
        if (toast) {
            toast.remove();
        }

        toast = document.createElement('div');
        toast.id = 'realbotComingSoonToast';
        toast.className = 'realbot-coming-soon-toast';
        toast.innerText = message || 'realBOT AI Advisor is coming soon to Propertism NRI clients.';
        
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
        
        const teaser = document.getElementById('realbotTeaserBubble');
        if (teaser) teaser.classList.add('hidden');
        
        // Focus input
        setTimeout(() => {
            const input = document.getElementById('realbotInput');
            if (input) input.focus();
        }, 320);
    }

    function closePanel() {
        if (!isInitialized) return;
        if (sessionId) {
            endSessionAndArchive();
        }
        overlayInstance.classList.remove('active');
        panelInstance.classList.remove('active');
        const wrapper = document.getElementById('realbotTriggerWrapper');
        if (wrapper) wrapper.classList.remove('hidden'); // Show wrapper containing ripples
        
        const teaser = document.getElementById('realbotTeaserBubble');
        if (teaser) teaser.classList.remove('hidden');

        // Start fresh next time
        sessionStorage.removeItem('realbot_session_id');
        sessionId = null;
        messages = [];
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

        messages.forEach((msg, idx) => {
            const now = msg.time || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            
            const renderTextWithBold = (txt) => {
                const parts = txt.split('**');
                return parts.map((part, idx) => (idx % 2 === 1 ? `<strong class="font-bold text-navy">${part}</strong>` : part)).join('');
            };

            const paragraphs = msg.text.split('\n\n').map(p => {
                if (p.startsWith('### ')) {
                    let headerText = p.replace('### ', '').trim();
                    let subHeader = '';
                    if (headerText.includes(' — ')) {
                        const parts = headerText.split(' — ');
                        headerText = parts[0].trim();
                        subHeader = `<span class="block text-[11px] font-semibold text-gray-400 normal-case mt-0.5">${parts[1].trim()}</span>`;
                    } else if (headerText.includes(' - ')) {
                        const parts = headerText.split(' - ');
                        headerText = parts[0].trim();
                        subHeader = `<span class="block text-[11px] font-semibold text-gray-400 normal-case mt-0.5">${parts[1].trim()}</span>`;
                    }
                    
                    let iconSVG = '';
                    const ht_lower = headerText.toLowerCase();
                    if (ht_lower.includes('nri assist') || ht_lower.includes('nri')) {
                        iconSVG = '<svg class="lucide-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>';
                    } else if (ht_lower.includes('overview') || ht_lower.includes('about')) {
                        iconSVG = '<svg class="lucide-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/></svg>';
                    } else if (ht_lower.includes('objective') || ht_lower.includes('mission')) {
                        iconSVG = '<svg class="lucide-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>';
                    } else if (ht_lower.includes('audience') || ht_lower.includes('client')) {
                        iconSVG = '<svg class="lucide-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>';
                    } else if (ht_lower.includes('contact') || ht_lower.includes('phone') || ht_lower.includes('email') || ht_lower.includes('support')) {
                        iconSVG = '<svg class="lucide-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>';
                    } else if (ht_lower.includes('location') || ht_lower.includes('locality') || ht_lower.includes('address') || ht_lower.includes('office')) {
                        iconSVG = '<svg class="lucide-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8c0 4.5-6 9-6 9s-6-4.5-6-9a6 6 0 0 1 12 0Z"/><circle cx="12" cy="8" r="2"/></svg>';
                    } else if (ht_lower.includes('price') || ht_lower.includes('pricing') || ht_lower.includes('budget') || ht_lower.includes('fee')) {
                        iconSVG = '<svg class="lucide-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" x2="12" y1="2" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>';
                    } else if (ht_lower.includes('document') || ht_lower.includes('file') || ht_lower.includes('brochure') || ht_lower.includes('policy') || ht_lower.includes('compliance')) {
                        iconSVG = '<svg class="lucide-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>';
                    } else if (ht_lower.includes('services') || ht_lower.includes('features')) {
                        iconSVG = '<svg class="lucide-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>';
                    }
                    
                    return `
                        <div class="mt-4 first:mt-0 pb-1 border-b border-navy/5">
                            <h3 class="text-[16px] font-bold text-navy uppercase tracking-tight font-sans flex items-center">${iconSVG}${headerText}</h3>
                            ${subHeader}
                        </div>
                    `;
                }
                return `<p class="text-[15px] text-gray-600 font-sans leading-relaxed">${renderTextWithBold(p)}</p>`;
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
            const headerLabel = isError ? 'SYSTEM ERROR' : (msg.sender === 'user' ? 'CLIENT CONSULTANT' : 'realBOT ADVISOR');

            // Avatar for realBOT Advisor welcome and subsequent messages
            let avatarHTML = '';
            if (msg.sender === 'assistant') {
                avatarHTML = `
                    <div class="w-5 h-5 rounded-full bg-[#0E2A47] border border-[#C89B2B] flex items-center justify-center text-[7px] font-extrabold text-[#C89B2B] shrink-0 select-none font-sans mr-2" style="box-shadow: 0 1px 3px rgba(15,23,42,0.15)">
                        rB
                    </div>
                `;
            }

            // Distinct classes per card type: user vs assistant (incorporates gold accent left border)
            let cardClasses = '';
            if (isError) {
                cardClasses = 'bg-red-50/70 border-red-200';
            } else if (msg.sender === 'user') {
                cardClasses = 'bg-[#F2F5F8] border-navy/5 rounded-sm';
            } else {
                cardClasses = 'bg-white border-navy/10 border-l-4 border-l-[#C89B2B] rounded-sm';
            }

            // Chips/Pills block inline with Lucide SVG outline icons
            let inlineChipsHTML = '';
            const isLastMsg = (idx === messages.length - 1);
            if (isLastMsg && msg.sender !== 'user' && msg.metadata) {
                const suggestions = msg.metadata.suggestions || [];
                const chips = msg.metadata.chips || [];
                
                let normalizedSuggestions = [];
                if (suggestions.length > 0) {
                    normalizedSuggestions = suggestions;
                } else if (chips.length > 0) {
                    normalizedSuggestions = chips.map(c => ({
                        display_text: c,
                        action: c === 'Talk to Advisor' || c === 'Contact Advisor' ? 'phone_call' : ''
                    }));
                }
                
                if (normalizedSuggestions.length > 0) {
                    const chipsList = normalizedSuggestions.map(sug => {
                        const chip = sug.display_text;
                        const action = sug.action || '';
                        let iconSVG = '';
                        const chip_lower = chip.toLowerCase();
                        if (chip_lower.includes('villa')) {
                            iconSVG = '<svg class="lucide-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>';
                        } else if (chip_lower.includes('apartment') || chip_lower.includes('rent')) {
                            iconSVG = '<svg class="lucide-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/></svg>';
                        } else if (chip_lower.includes('plot') || chip_lower.includes('land')) {
                            iconSVG = '<svg class="lucide-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8c0 4.5-6 9-6 9s-6-4.5-6-9a6 6 0 0 1 12 0Z"/><circle cx="12" cy="8" r="2"/></svg>';
                        } else if (chip_lower.includes('nri') || chip_lower.includes('investment') || chip_lower.includes('global')) {
                            iconSVG = '<svg class="lucide-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>';
                        } else if (chip_lower.includes('rental') || chip_lower.includes('key')) {
                            iconSVG = '<svg class="lucide-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6"/><path d="m15.5 7.5 3 3h3v-3h-3Z"/></svg>';
                        } else if (chip_lower.includes('compare') || chip_lower.includes('git')) {
                            iconSVG = '<svg class="lucide-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="5" cy="6" r="3"/><circle cx="19" cy="18" r="3"/><path d="m12 14 2-2 2 2"/><path d="M14 12V4a2 2 0 0 1 2-2h3"/><path d="m12 10-2 2-2-2"/><path d="M10 12v8a2 2 0 0 1-2 2H5"/></svg>';
                        } else if (chip_lower.includes('talk') || chip_lower.includes('advisor') || chip_lower.includes('contact') || chip_lower.includes('phone') || chip_lower.includes('call')) {
                            iconSVG = '<svg class="lucide-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>';
                        }
                        
                        const escapedChip = chip.replace(/'/g, "\\'");
                        const escapedAction = action.replace(/'/g, "\\'");
                        
                        return `
                            <button onclick="window.realbotControl.triggerChip('${escapedChip}', '${escapedAction}')" class="realbot-chip-pill">
                                ${iconSVG}
                                <span>${chip}</span>
                            </button>
                        `;
                    }).join('');
                    
                    inlineChipsHTML = `
                        <div class="flex flex-wrap gap-2 mt-2 px-1 select-none">
                            ${chipsList}
                        </div>
                    `;
                }
            }

            const msgHTML = `
                <div class="flex flex-col mb-2 select-text">
                    <div class="flex items-center text-[9px] text-gray-400 font-bold tracking-wider uppercase mb-1 px-1 font-sans select-none">
                        ${avatarHTML}
                        <span>${headerLabel}<span class="opacity-60 font-normal lowercase ml-2.5" style="font-variant: small-caps;">${now}</span></span>
                    </div>
                    <div class="${cardClasses} border py-2.5 px-3.5 text-[15px] font-sans text-gray-800 space-y-2">
                        ${paragraphs}
                        ${propertyCardHTML}
                        ${tableHTML}
                        ${citationsHTML}
                    </div>
                    ${inlineChipsHTML}
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

    // Render suggestion chips dynamically (Deprecated in favor of inline message pills)
    function renderSuggestionChips(chipsArray) {
        const chipsContainer = document.getElementById('realbotChipsContainer');
        if (chipsContainer) {
            chipsContainer.parentElement.classList.add('hidden');
        }
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
            if (data.success && data.data) {
                messages.push(data.data.message);
                renderMessages();
            } else {
                showAPIError((data.error && data.error.message) || "The advisor is currently offline. Please try again.");
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

    let toastTimeout = null;
    function showComingSoonToast(message) {
        // Ensure panel instance exists in DOM
        ensurePanelInDOM();
        if (!panelInstance) return;

        let toastEl = document.getElementById('realbotToast');
        if (!toastEl) {
            toastEl = document.createElement('div');
            toastEl.id = 'realbotToast';
            toastEl.className = 'realbot-toast';
            panelInstance.appendChild(toastEl);
        }

        toastEl.textContent = message || "Coming soon.";
        toastEl.classList.add('show');

        if (toastTimeout) {
            clearTimeout(toastTimeout);
        }

        toastTimeout = setTimeout(function() {
            toastEl.classList.remove('show');
        }, 3000);
    }

    // Helper to send end of session archive request
    function endSessionAndArchive() {
        if (!sessionId) return;
        const currentSessionId = sessionId;
        fetch('/chat/inquiry/handover/customer/end/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') || ''
            },
            body: JSON.stringify({
                session_id: currentSessionId,
                send_email: false
            })
        }).then(res => {
            if (res.ok) {
                console.log("Session archived successfully:", currentSessionId);
            }
        }).catch(err => {
            console.error("Error archiving session:", err);
        });
    }

    // Expose control hook triggers on global scope for inline HTML callbacks
    window.realbotControl = {
        triggerChip: function(text, action) {
            action = action || '';
            const action_lower = action.toLowerCase();
            if (action.startsWith('/') || action.startsWith('http')) {
                window.location.href = action;
            } else if (action_lower === 'phone_call' || action_lower === 'phone') {
                window.location.href = 'tel:+918667020798';
            } else if (action_lower === 'whatsapp') {
                window.location.href = 'https://wa.me/918667020798';
            } else if (action_lower === 'restart' || action_lower === 'clear') {
                clearChat();
            } else {
                triggerResponseSequence(text);
            }
        },
        clearChat: function() {
            clearChat();
        },
        togglePanel: function() {
            togglePanel();
        },
        showToast: function(message) {
            showComingSoonToast(message);
        }
    };

    // Auto-init on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
