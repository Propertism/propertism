// Chat Widget JavaScript
(function() {
    'use strict';
    
    const ChatWidget = {
        init() {
            this.createWidget();
            this.attachEventListeners();
        },
        
        createWidget() {
            const widgetHTML = `
                <div class="chat-widget">
                    <div class="chat-backdrop" id="chatBackdrop"></div>
                    
                    <button class="chat-button" id="chatButton" aria-label="Open chat">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                            <path d="M8 9h8M8 13h5"/>
                        </svg>
                    </button>
                    
                    <div class="chat-window" id="chatWindow">
                        <div class="chat-header">
                            <div>
                                <div class="chat-header-title">Leave a message</div>
                                <div class="chat-header-subtitle">We'll get back to you soon</div>
                            </div>
                            <button class="chat-close" id="chatClose" aria-label="Close chat">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                                    <path d="M18 6L6 18M6 6l12 12"/>
                                </svg>
                            </button>
                        </div>
                        
                        <div class="chat-body" id="chatBody">
                            <form class="chat-form" id="chatForm">
                                <div id="chatError" class="chat-error" style="display: none;"></div>
                                
                                <div class="chat-input-group">
                                    <label class="chat-label" for="chatName">Name *</label>
                                    <input type="text" id="chatName" class="chat-input" required>
                                </div>
                                
                                <div class="chat-input-group">
                                    <label class="chat-label" for="chatEmail">Email *</label>
                                    <input type="email" id="chatEmail" class="chat-input" required>
                                </div>
                                
                                <div class="chat-input-group">
                                    <label class="chat-label" for="chatPhone">Phone</label>
                                    <input type="tel" id="chatPhone" class="chat-input">
                                </div>
                                
                                <div class="chat-input-group">
                                    <label class="chat-label" for="chatMessage">Message *</label>
                                    <textarea id="chatMessage" class="chat-textarea" required></textarea>
                                </div>
                                
                                <button type="submit" class="chat-submit" id="chatSubmit">
                                    <span>Send</span>
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                        <path d="M12 19V5M5 12l7-7 7 7"/>
                                    </svg>
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.insertAdjacentHTML('beforeend', widgetHTML);
        },
        
        attachEventListeners() {
            const chatButton = document.getElementById('chatButton');
            const chatWindow = document.getElementById('chatWindow');
            const chatBackdrop = document.getElementById('chatBackdrop');
            const chatClose = document.getElementById('chatClose');
            const chatForm = document.getElementById('chatForm');
            
            chatButton.addEventListener('click', () => this.toggleChat());
            chatClose.addEventListener('click', () => this.closeChat());
            chatBackdrop.addEventListener('click', () => this.closeChat());
            chatForm.addEventListener('submit', (e) => this.handleSubmit(e));
        },
        
        toggleChat() {
            const chatWindow = document.getElementById('chatWindow');
            const chatBackdrop = document.getElementById('chatBackdrop');
            chatWindow.classList.toggle('active');
            chatBackdrop.classList.toggle('active');
            
            // Prevent body scroll when chat is open on mobile
            if (chatWindow.classList.contains('active')) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        },
        
        closeChat() {
            const chatWindow = document.getElementById('chatWindow');
            const chatBackdrop = document.getElementById('chatBackdrop');
            chatWindow.classList.remove('active');
            chatBackdrop.classList.remove('active');
            document.body.style.overflow = '';
        },
        
        async handleSubmit(e) {
            e.preventDefault();
            
            const submitBtn = document.getElementById('chatSubmit');
            const errorDiv = document.getElementById('chatError');
            
            // Get form data
            const formData = new FormData();
            formData.append('name', document.getElementById('chatName').value);
            formData.append('email', document.getElementById('chatEmail').value);
            formData.append('phone', document.getElementById('chatPhone').value);
            formData.append('message', document.getElementById('chatMessage').value);
            
            // Disable submit button
            submitBtn.disabled = true;
            const submitText = submitBtn.querySelector('span');
            submitText.textContent = 'Sending...';
            errorDiv.style.display = 'none';
            
            try {
                const response = await fetch('/chat/submit/', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    this.showSuccess();
                } else {
                    throw new Error(data.error || 'Something went wrong');
                }
            } catch (error) {
                errorDiv.textContent = error.message;
                errorDiv.style.display = 'block';
                submitBtn.disabled = false;
                const submitText = submitBtn.querySelector('span');
                submitText.textContent = 'Send';
            }
        },
        
        showSuccess() {
            const chatBody = document.getElementById('chatBody');
            chatBody.innerHTML = `
                <div class="chat-success">
                    <div class="chat-success-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                            <path d="M20 6L9 17l-5-5"/>
                        </svg>
                    </div>
                    <div class="chat-success-title">Message sent!</div>
                    <div class="chat-success-message">
                        Thanks for reaching out. We'll get back to you within 24 hours.
                    </div>
                </div>
            `;
            
            // Close chat after 3 seconds
            setTimeout(() => {
                this.closeChat();
                // Reset form after closing
                setTimeout(() => {
                    location.reload();
                }, 300);
            }, 3000);
        }
    };
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => ChatWidget.init());
    } else {
        ChatWidget.init();
    }
})();
