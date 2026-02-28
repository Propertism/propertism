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

/* ============================================
   SIGN IN & PROFILE FUNCTIONALITY
   ============================================ */

/**
 * Show Sign In Modal
 */
function showSignInModal() {
    // Create modal if it doesn't exist
    let modal = document.getElementById('signInModal');
    
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'signInModal';
        modal.className = 'auth-modal';
        modal.innerHTML = `
            <div class="auth-modal-overlay" onclick="closeSignInModal()"></div>
            <div class="auth-modal-content">
                <button class="auth-modal-close" onclick="closeSignInModal()">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                </button>
                
                <div class="auth-modal-header">
                    <h2>Welcome to Propertism</h2>
                    <p>Sign in to save properties and manage your account</p>
                </div>
                
                <div class="auth-modal-body">
                    <button class="auth-btn auth-btn-guest" onclick="signInAsGuest()">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                            <circle cx="12" cy="7" r="4"/>
                        </svg>
                        Continue as Guest
                    </button>
                    
                    <div class="auth-divider">
                        <span>or sign in with</span>
                    </div>
                    
                    <button class="auth-btn auth-btn-google">
                        <svg width="20" height="20" viewBox="0 0 24 24">
                            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                        </svg>
                        Sign in with Google
                    </button>
                    
                    <button class="auth-btn auth-btn-email">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                            <polyline points="22,6 12,13 2,6"/>
                        </svg>
                        Sign in with Email
                    </button>
                </div>
                
                <div class="auth-modal-footer">
                    <p>By continuing, you agree to our <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a></p>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        
        // Add styles
        addAuthModalStyles();
    }
    
    // Show modal
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

/**
 * Close Sign In Modal
 */
function closeSignInModal() {
    const modal = document.getElementById('signInModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

/**
 * Sign in as Guest
 */
function signInAsGuest() {
    showAlert('Signed in as Guest', 'success');
    closeSignInModal();
    
    // Update UI to show guest user
    const signInBtn = document.getElementById('signInBtn');
    if (signInBtn) {
        signInBtn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
            </svg>
            Guest
        `;
    }
}

/**
 * Add Auth Modal Styles
 */
function addAuthModalStyles() {
    if (document.getElementById('authModalStyles')) return;
    
    const style = document.createElement('style');
    style.id = 'authModalStyles';
    style.textContent = `
        .auth-modal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s;
        }
        
        .auth-modal.active {
            opacity: 1;
            visibility: visible;
        }
        
        .auth-modal-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(4px);
        }
        
        .auth-modal-content {
            position: relative;
            width: 90%;
            max-width: 440px;
            background: white;
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            transform: scale(0.9);
            transition: transform 0.3s;
        }
        
        .auth-modal.active .auth-modal-content {
            transform: scale(1);
        }
        
        .auth-modal-close {
            position: absolute;
            top: 16px;
            right: 16px;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: transparent;
            border: none;
            color: #6B7280;
            cursor: pointer;
            border-radius: 50%;
            transition: all 0.2s;
        }
        
        .auth-modal-close:hover {
            background: #F3F4F6;
            color: #111827;
        }
        
        .auth-modal-header {
            text-align: center;
            margin-bottom: 32px;
        }
        
        .auth-modal-header h2 {
            font-family: "Object Sans", "Adjusted Arial", Tahoma, Geneva, sans-serif;
            font-size: 1.75rem;
            font-weight: 600;
            color: #111827;
            margin-bottom: 8px;
        }
        
        .auth-modal-header p {
            font-size: 0.9375rem;
            color: #6B7280;
            margin: 0;
        }
        
        .auth-modal-body {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        
        .auth-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            padding: 14px 24px;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            font-family: "Object Sans", "Adjusted Arial", Tahoma, Geneva, sans-serif;
            font-size: 0.9375rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            background: white;
            color: #111827;
        }
        
        .auth-btn:hover {
            background: #F9FAFB;
            border-color: #D1D5DB;
            transform: translateY(-1px);
        }
        
        .auth-btn-guest {
            background: #0A1628;
            color: white;
            border-color: #0A1628;
        }
        
        .auth-btn-guest:hover {
            background: #1a2942;
            border-color: #1a2942;
        }
        
        .auth-divider {
            display: flex;
            align-items: center;
            margin: 16px 0;
            color: #9CA3AF;
            font-size: 0.875rem;
        }
        
        .auth-divider::before,
        .auth-divider::after {
            content: '';
            flex: 1;
            height: 1px;
            background: #E5E7EB;
        }
        
        .auth-divider span {
            padding: 0 16px;
        }
        
        .auth-modal-footer {
            margin-top: 24px;
            text-align: center;
        }
        
        .auth-modal-footer p {
            font-size: 0.8125rem;
            color: #9CA3AF;
            margin: 0;
        }
        
        .auth-modal-footer a {
            color: #0A1628;
            text-decoration: none;
            font-weight: 600;
        }
        
        .auth-modal-footer a:hover {
            text-decoration: underline;
        }
    `;
    document.head.appendChild(style);
}

/**
 * Toggle Profile Dropdown
 */
function toggleProfileDropdown() {
    const profileDropdown = document.getElementById('profileDropdown');
    if (profileDropdown) {
        profileDropdown.classList.toggle('active');
    }
}

/**
 * Initialize Sign In
 */
function initSignIn() {
    const signInBtn = document.getElementById('signInBtn');
    
    if (signInBtn) {
        signInBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showSignInModal();
        });
    }
}

/**
 * Initialize Profile Dropdown
 */
function initProfileDropdown() {
    const profileBtn = document.getElementById('profileBtn');
    const profileDropdown = document.getElementById('profileDropdown');
    
    if (profileBtn && profileDropdown) {
        profileBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            profileDropdown.classList.toggle('active');
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!profileBtn.contains(e.target) && !profileDropdown.contains(e.target)) {
                profileDropdown.classList.remove('active');
            }
        });
    }
}

/**
 * Update DOMContentLoaded to include new functions
 */
document.addEventListener('DOMContentLoaded', function() {
    initGallery();
    initFormValidation();
    initSearch();
    initSignIn();
    initProfileDropdown();
});
