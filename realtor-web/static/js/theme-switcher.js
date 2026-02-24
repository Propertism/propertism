/**
 * Theme Switcher - Light, Dark, System
 * Manthraa Design Language Compatible
 */

(function() {
    'use strict';
    
    const THEME_KEY = 'propertism-theme';
    const THEMES = {
        LIGHT: 'light',
        DARK: 'dark',
        SYSTEM: 'system'
    };
    
    class ThemeSwitcher {
        constructor() {
            this.currentTheme = this.getStoredTheme() || THEMES.SYSTEM;
            this.init();
        }
        
        init() {
            // Apply theme on load
            this.applyTheme(this.currentTheme);
            
            // Setup event listeners
            this.setupEventListeners();
            
            // Listen for system theme changes
            this.watchSystemTheme();
        }
        
        setupEventListeners() {
            const themeToggle = document.getElementById('themeToggle');
            const themeOptions = document.querySelectorAll('.theme-option');
            
            if (themeToggle) {
                themeToggle.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const menu = themeToggle.nextElementSibling;
                    menu.classList.toggle('show');
                });
            }
            
            themeOptions.forEach(option => {
                option.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const theme = option.dataset.theme;
                    this.setTheme(theme);
                    
                    // Close menu
                    const menu = option.closest('.theme-menu');
                    if (menu) {
                        menu.classList.remove('show');
                    }
                    
                    // Update active state
                    themeOptions.forEach(opt => opt.classList.remove('active'));
                    option.classList.add('active');
                });
                
                // Set initial active state
                if (option.dataset.theme === this.currentTheme) {
                    option.classList.add('active');
                }
            });
            
            // Close menu when clicking outside
            document.addEventListener('click', (e) => {
                const themeMenu = document.querySelector('.theme-menu');
                if (themeMenu && !e.target.closest('.theme-switcher')) {
                    themeMenu.classList.remove('show');
                }
            });
        }
        
        setTheme(theme) {
            this.currentTheme = theme;
            this.storeTheme(theme);
            this.applyTheme(theme);
        }
        
        applyTheme(theme) {
            const html = document.documentElement;
            
            // Remove existing theme classes
            html.classList.remove('theme-light', 'theme-dark');
            
            if (theme === THEMES.SYSTEM) {
                // Use system preference
                const systemTheme = this.getSystemTheme();
                html.classList.add(`theme-${systemTheme}`);
                html.setAttribute('data-theme', systemTheme);
            } else {
                // Use selected theme
                html.classList.add(`theme-${theme}`);
                html.setAttribute('data-theme', theme);
            }
            
            // Update theme toggle icon
            this.updateThemeIcon(theme);
        }
        
        updateThemeIcon(theme) {
            const sunIcon = document.querySelector('.sun-icon');
            const moonIcon = document.querySelector('.moon-icon');
            
            if (!sunIcon || !moonIcon) return;
            
            const effectiveTheme = theme === THEMES.SYSTEM ? this.getSystemTheme() : theme;
            
            if (effectiveTheme === THEMES.DARK) {
                sunIcon.style.display = 'none';
                moonIcon.style.display = 'block';
            } else {
                sunIcon.style.display = 'block';
                moonIcon.style.display = 'none';
            }
        }
        
        getSystemTheme() {
            return window.matchMedia('(prefers-color-scheme: dark)').matches 
                ? THEMES.DARK 
                : THEMES.LIGHT;
        }
        
        watchSystemTheme() {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            
            mediaQuery.addEventListener('change', (e) => {
                if (this.currentTheme === THEMES.SYSTEM) {
                    this.applyTheme(THEMES.SYSTEM);
                }
            });
        }
        
        storeTheme(theme) {
            try {
                localStorage.setItem(THEME_KEY, theme);
            } catch (e) {
                console.warn('Could not store theme preference:', e);
            }
        }
        
        getStoredTheme() {
            try {
                return localStorage.getItem(THEME_KEY);
            } catch (e) {
                console.warn('Could not retrieve theme preference:', e);
                return null;
            }
        }
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            new ThemeSwitcher();
        });
    } else {
        new ThemeSwitcher();
    }
})();
