/**
 * PetroCalc Web - Main JavaScript File
 * Handles common functionality across the application
 */

// Global application object
const PetroCalc = {
    // API base URL
    apiBase: '/api',
    
    // Store recent calculations
    recentCalculations: [],
    
    // Initialize the application
    init: function() {
        this.setupGlobalEventListeners();
        this.loadRecentCalculations();
        this.setupFormValidation();
    },
    
    // Setup global event listeners
    setupGlobalEventListeners: function() {
        // Handle navbar active states
        this.setActiveNavItem();
        
        // Setup tooltips if Bootstrap is available
        if (typeof bootstrap !== 'undefined') {
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
        
        // Setup copy to clipboard functionality
        this.setupCopyToClipboard();
    },
    
    // Set active navigation item based on current page
    setActiveNavItem: function() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    },
    
    // Setup form validation
    setupFormValidation: function() {
        const forms = document.querySelectorAll('form[id$="Form"]');
        
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                if (!form.checkValidity()) {
                    e.preventDefault();
                    e.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    },
    
    // Make API calls with error handling
    makeAPICall: async function(endpoint, data, options = {}) {
        const defaultOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        };
        
        const finalOptions = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(this.apiBase + endpoint, finalOptions);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            
            // Store successful calculation
            this.addRecentCalculation({
                endpoint: endpoint,
                data: data,
                result: result,
                timestamp: new Date().toISOString()
            });
            
            return result;
        } catch (error) {
            console.error('API call failed:', error);
            throw error;
        }
    },
    
    // Display result in specified element
    displayResult: function(elementId, content, type = 'success') {
        const element = document.getElementById(elementId);
        if (!element) return;
        
        const alertClass = type === 'error' ? 'alert-danger' : 'alert-success';
        const icon = type === 'error' ? 'fas fa-exclamation-triangle' : 'fas fa-check-circle';
        
        element.innerHTML = `
            <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
                <i class="${icon} me-2"></i>
                ${content}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
    },
    
    // Add calculation to recent calculations
    addRecentCalculation: function(calculation) {
        this.recentCalculations.unshift(calculation);
        
        // Keep only last 5 calculations
        if (this.recentCalculations.length > 5) {
            this.recentCalculations = this.recentCalculations.slice(0, 5);
        }
        
        // Save to localStorage
        localStorage.setItem('petroCalcRecentCalculations', JSON.stringify(this.recentCalculations));
        
        // Update display
        this.updateRecentCalculationsDisplay();
    },
    
    // Load recent calculations from localStorage
    loadRecentCalculations: function() {
        const stored = localStorage.getItem('petroCalcRecentCalculations');
        if (stored) {
            this.recentCalculations = JSON.parse(stored);
            this.updateRecentCalculationsDisplay();
        }
    },
    
    // Update recent calculations display
    updateRecentCalculationsDisplay: function() {
        const element = document.getElementById('recentCalculations');
        if (!element) return;
        
        if (this.recentCalculations.length === 0) {
            element.innerHTML = '<p class="text-muted">No recent calculations</p>';
            return;
        }
        
        let html = '';
        this.recentCalculations.forEach((calc, index) => {
            const date = new Date(calc.timestamp).toLocaleString();
            const endpoint = calc.endpoint.replace('/api/', '').replace(/\//g, ' > ');
            
            html += `
                <div class="small mb-2 p-2 bg-light rounded">
                    <strong>${endpoint}</strong><br>
                    <span class="text-muted">${date}</span>
                </div>
            `;
        });
        
        element.innerHTML = html;
    },
    
    // Setup copy to clipboard functionality
    setupCopyToClipboard: function() {
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('copy-btn')) {
                const textToCopy = e.target.dataset.copy;
                navigator.clipboard.writeText(textToCopy).then(function() {
                    // Show success feedback
                    const originalText = e.target.innerHTML;
                    e.target.innerHTML = '<i class="fas fa-check"></i> Copied!';
                    setTimeout(() => {
                        e.target.innerHTML = originalText;
                    }, 2000);
                });
            }
        });
    },
    
    // Format number for display
    formatNumber: function(num, decimals = 4) {
        if (isNaN(num)) return 'N/A';
        return parseFloat(num).toFixed(decimals);
    },
    
    // Show loading state
    showLoading: function(buttonElement) {
        if (!buttonElement) return;
        
        const originalHTML = buttonElement.innerHTML;
        buttonElement.dataset.originalHTML = originalHTML;
        buttonElement.innerHTML = '<span class="spinner me-2"></span>Calculating...';
        buttonElement.disabled = true;
    },
    
    // Hide loading state
    hideLoading: function(buttonElement) {
        if (!buttonElement) return;
        
        const originalHTML = buttonElement.dataset.originalHTML;
        if (originalHTML) {
            buttonElement.innerHTML = originalHTML;
        }
        buttonElement.disabled = false;
    },
    
    // Validate input ranges
    validateInput: function(value, min, max, fieldName) {
        if (value < min || value > max) {
            throw new Error(`${fieldName} must be between ${min} and ${max}`);
        }
        return true;
    },
    
    // Export calculation results to CSV
    exportToCSV: function(data, filename) {
        const csv = this.convertToCSV(data);
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.setAttribute('hidden', '');
        a.setAttribute('href', url);
        a.setAttribute('download', filename);
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    },
    
    // Convert data to CSV format
    convertToCSV: function(data) {
        const headers = Object.keys(data[0]).join(',');
        const rows = data.map(row => Object.values(row).join(','));
        return headers + '\n' + rows.join('\n');
    }
};

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    PetroCalc.init();
});

// Make PetroCalc available globally
window.PetroCalc = PetroCalc;
