// Chat Widget JavaScript - Scrolls to contact section
(function() {
    'use strict';

    function init() {
        // Create only the floating button (no popup window)
        const widgetHTML = `
            <div class="chat-widget">
                <button class="chat-button" id="chatButton" aria-label="Get in touch">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                        <path d="M8 9h8M8 13h5"/>
                    </svg>
                </button>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', widgetHTML);

        // Scroll to contact section on click
        document.getElementById('chatButton').addEventListener('click', function () {
            var contactSection = document.getElementById('contact-section');
            if (contactSection) {
                var headerHeight = document.querySelector('.site-header, header')
                    ? document.querySelector('.site-header, header').offsetHeight
                    : 0;
                var top = contactSection.getBoundingClientRect().top + window.pageYOffset - headerHeight + 20;
                window.scrollTo({ top: top, behavior: 'smooth' });
            } else {
                window.location.href = '/#contact-section';
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
