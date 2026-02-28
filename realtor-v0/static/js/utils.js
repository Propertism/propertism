/* ============================================
   UTILITY FUNCTIONS - PROPERTISM
   ============================================ */

/**
 * Format currency in Indian Rupees
 * @param {number} amount - Amount to format
 * @returns {string} Formatted currency string
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0
    }).format(amount);
}

/**
 * Format date
 * @param {string} dateString - Date string to format
 * @returns {string} Formatted date string
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-IN', options);
}

/**
 * Debounce function
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Get URL parameter
 * @param {string} param - Parameter name
 * @returns {string|null} Parameter value
 */
function getUrlParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

/**
 * Smooth scroll to element
 * @param {string} selector - Element selector
 */
function scrollToElement(selector) {
    const element = document.querySelector(selector);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

/**
 * Toggle class on element
 * @param {string} selector - Element selector
 * @param {string} className - Class name to toggle
 */
function toggleClass(selector, className) {
    const element = document.querySelector(selector);
    if (element) {
        element.classList.toggle(className);
    }
}

/**
 * Show/hide element
 * @param {string} selector - Element selector
 * @param {boolean} show - Show or hide
 */
function toggleElement(selector, show) {
    const element = document.querySelector(selector);
    if (element) {
        element.style.display = show ? 'block' : 'none';
    }
}

/**
 * Format phone number
 * @param {string} phone - Phone number
 * @returns {string} Formatted phone number
 */
function formatPhone(phone) {
    const cleaned = ('' + phone).replace(/\D/g, '');
    const match = cleaned.match(/^(\d{2})(\d{5})(\d{5})$/);
    if (match) {
        return '+' + match[1] + ' ' + match[2] + ' ' + match[3];
    }
    return phone;
}

/**
 * Validate email
 * @param {string} email - Email address
 * @returns {boolean} Is valid email
 */
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Validate phone
 * @param {string} phone - Phone number
 * @returns {boolean} Is valid phone
 */
function isValidPhone(phone) {
    const re = /^[\d\s\+\-\(\)]+$/;
    return re.test(phone) && phone.replace(/\D/g, '').length >= 10;
}

/**
 * Show alert message
 * @param {string} message - Alert message
 * @param {string} type - Alert type (success, error, warning, info)
 */
function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background-color: ${type === 'success' ? '#00a86b' : type === 'error' ? '#dc3545' : '#0066cc'};
        color: white;
        z-index: 9999;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    `;
    document.body.appendChild(alert);
    
    setTimeout(() => {
        alert.remove();
    }, 3000);
}

/**
 * Initialize property image gallery
 */
function initGallery() {
    const thumbs = document.querySelectorAll('.gallery-thumbs img');
    const mainImage = document.getElementById('mainImage');
    
    if (thumbs.length && mainImage) {
        thumbs.forEach(thumb => {
            thumb.addEventListener('click', function() {
                mainImage.src = this.src;
                thumbs.forEach(t => t.style.borderColor = 'transparent');
                this.style.borderColor = '#1a1a1a';
            });
        });
    }
}

/**
 * Initialize form validation
 */
function initFormValidation() {
    const forms = document.querySelectorAll('.form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const emailInputs = form.querySelectorAll('input[type="email"]');
            const phoneInputs = form.querySelectorAll('input[type="tel"]');
            
            let isValid = true;
            
            emailInputs.forEach(input => {
                if (!isValidEmail(input.value)) {
                    e.preventDefault();
                    showAlert('Please enter a valid email address', 'error');
                    input.focus();
                    isValid = false;
                }
            });
            
            if (isValid) {
                phoneInputs.forEach(input => {
                    if (!isValidPhone(input.value)) {
                        e.preventDefault();
                        showAlert('Please enter a valid phone number', 'error');
                        input.focus();
                        isValid = false;
                    }
                });
            }
        });
    });
}

/**
 * Initialize search functionality
 */
function initSearch() {
    const searchInput = document.querySelector('input[name="q"]');
    
    if (searchInput) {
        const debouncedSearch = debounce(function(value) {
            console.log('Searching for:', value);
        }, 500);
        
        searchInput.addEventListener('input', function() {
            debouncedSearch(this.value);
        });
    }
}

/**
 * Initialize on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    initGallery();
    initFormValidation();
    initSearch();
});