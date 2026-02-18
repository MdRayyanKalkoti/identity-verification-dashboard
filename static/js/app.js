// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔍 Dashboard Initializing...');

    // ===== App State =====
    const AppState = {
        authenticated: false,
        currentSection: 'overview',
        identityData: null
    };

    // ===== DOM Elements =====
    const DOM = {
        lockOverlay: document.getElementById('lockOverlay'),
        lockIcon: document.getElementById('lockIcon'),
        passwordInput: document.getElementById('passwordInput'),
        unlockBtn: document.getElementById('unlockBtn'),
        errorMessage: document.getElementById('errorMessage'),
        dashboard: document.getElementById('dashboard'),
        navItems: document.querySelectorAll('.nav-item'),
        sections: document.querySelectorAll('.section'),
        logoutBtn: document.getElementById('logoutBtn'),
        identityData: document.getElementById('identityData'),
        pdfModal: document.getElementById('pdfModal'),
        pdfViewer: document.getElementById('pdfViewer'),
        pdfTitle: document.getElementById('pdfTitle'),
        pdfClose: document.querySelector('.pdf-close')
    };

    console.log('✅ DOM Elements loaded');

    // ===== Utility Functions =====
    const showError = (message) => {
        DOM.errorMessage.textContent = message;
        DOM.errorMessage.style.color = '#ef4444';
    };

    const showSuccess = (message) => {
        DOM.errorMessage.textContent = message;
        DOM.errorMessage.style.color = '#10b981';
    };

    const clearError = () => {
        DOM.errorMessage.textContent = '';
    };

    // ===== API Functions =====
    const API = {
        async verifyPassword(password) {
            const response = await fetch('/api/verify-password', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ password: password })
            });
            return response.json();
        },
        
        async getIdentity() {
            const response = await fetch('/api/identity');
            return response.json();
        }
    };

    // ===== Authentication =====
    const handleUnlock = async () => {
        const password = DOM.passwordInput.value.trim();
        
        if (!password) {
            showError('Please enter a password');
            return;
        }
        
        clearError();
        DOM.unlockBtn.disabled = true;
        DOM.unlockBtn.innerHTML = '<span>Verifying...</span>';
        
        try {
            const result = await API.verifyPassword(password);
            
            if (result.success) {
                showSuccess('✓ Access Granted');
                DOM.lockIcon.textContent = '🔓';
                
                setTimeout(() => {
                    DOM.lockOverlay.style.display = 'none';
                    DOM.dashboard.classList.remove('blurred');
                    DOM.dashboard.classList.add('active');
                    AppState.authenticated = true;
                    loadDashboardData();
                }, 800);
            } else {
                showError(result.error || 'Invalid password');
                DOM.unlockBtn.disabled = false;
                DOM.unlockBtn.innerHTML = '<span>Unlock Dashboard</span>';
            }
        } catch (error) {
            showError('Connection error. Please try again.');
            DOM.unlockBtn.disabled = false;
            DOM.unlockBtn.innerHTML = '<span>Unlock Dashboard</span>';
        }
    };

    // ===== Dashboard Data Loading =====
    const loadDashboardData = async () => {
        try {
            const result = await API.getIdentity();
            if (result.success) {
                AppState.identityData = result.data;
                renderIdentityData(result.data);
            }
        } catch (error) {
            console.error('Failed to load identity data:', error);
        }
    };

    const renderIdentityData = (data) => {
        const html = `
            <div class="info-item">
                <div class="info-label">Full Name</div>
                <div class="info-value">${data.name}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Aadhaar Number</div>
                <div class="info-value">${data.aadhaar}</div>
            </div>
            <div class="info-item">
                <div class="info-label">PAN Number</div>
                <div class="info-value">${data.pan}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Passport Number</div>
                <div class="info-value">${data.passport}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Date of Birth</div>
                <div class="info-value">${data.dob}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Verification Status</div>
                <div class="info-value" style="color: #10b981">${data.verification_status}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Verified On</div>
                <div class="info-value">${data.verification_date}</div>
            </div>
        `;
        DOM.identityData.innerHTML = html;
    };

    // ===== Navigation =====
    const navigateToSection = (sectionId) => {
        DOM.navItems.forEach(item => {
            if (item.dataset.section === sectionId) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
        
        DOM.sections.forEach(section => {
            if (section.id === sectionId) {
                section.classList.add('active');
            } else {
                section.classList.remove('active');
            }
        });
        
        AppState.currentSection = sectionId;
    };

    // ===== PDF Modal - UPDATED FOR IFRAME WITH PARAMETERS =====
    const openPDFModal = (docType) => {
        console.log('📄 Opening PDF modal for:', docType);
        
        if (!DOM.pdfModal || !DOM.pdfViewer) {
            console.error('❌ PDF Modal elements not found!');
            window.open('/api/documents/' + docType, '_blank');
            return;
        }
        
        const titles = {
            'aadhaar': 'Aadhaar Card',
            'pan': 'PAN Card',
            'passport': 'Passport'
        };
        
        // Add parameters to hide PDF controls and optimize display
        const pdfUrl = '/api/documents/' + docType + '#toolbar=0&navpanes=0&scrollbar=0&view=FitH';
        
        // Set title
        DOM.pdfTitle.textContent = titles[docType] || 'Document Viewer';
        
        // Set iframe src
        DOM.pdfViewer.setAttribute('src', pdfUrl);
        
        // Show modal
        DOM.pdfModal.classList.add('active');
        
        console.log('✅ PDF Modal opened');
    };

    const closePDFModal = () => {
        console.log('❌ Closing PDF modal');
        if (DOM.pdfModal) {
            DOM.pdfModal.classList.remove('active');
            if (DOM.pdfViewer) {
                // Clear iframe src to stop loading
                DOM.pdfViewer.setAttribute('src', '');
            }
        }
    };

    // ===== Event Listeners =====
    
    // Authentication
    DOM.unlockBtn.addEventListener('click', handleUnlock);
    DOM.passwordInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleUnlock();
    });

    // Navigation
    DOM.navItems.forEach(item => {
        item.addEventListener('click', () => {
            navigateToSection(item.dataset.section);
        });
    });

    document.querySelectorAll('[data-navigate]').forEach(btn => {
        btn.addEventListener('click', () => {
            navigateToSection(btn.dataset.navigate);
        });
    });

    // Logout
    DOM.logoutBtn.addEventListener('click', async () => {
        if (confirm('Are you sure you want to logout?')) {
            await fetch('/api/logout', { method: 'POST' });
            location.reload();
        }
    });

    // Document buttons
    document.querySelectorAll('.doc-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const docType = this.getAttribute('data-doc');
            const action = this.getAttribute('data-action');
            
            console.log('🔘 Document button clicked:', docType, action);
            
            if (action === 'view') {
                openPDFModal(docType);
            } else if (action === 'download') {
                window.location.href = '/api/documents/' + docType + '?action=download';
            }
        });
    });

    // Report generation
    const generateReportBtn = document.getElementById('generateReport');
    if (generateReportBtn) {
        generateReportBtn.addEventListener('click', () => {
            window.open('/api/generate-report', '_blank');
        });
    }

    const quickReportBtn = document.getElementById('quickReport');
    if (quickReportBtn) {
        quickReportBtn.addEventListener('click', () => {
            window.open('/api/generate-report', '_blank');
        });
    }

    // PDF Modal close button
    if (DOM.pdfClose) {
        DOM.pdfClose.addEventListener('click', closePDFModal);
    }

    // Close modal when clicking outside
    if (DOM.pdfModal) {
        DOM.pdfModal.addEventListener('click', (e) => {
            if (e.target === DOM.pdfModal) {
                closePDFModal();
            }
        });
    }

    // Close modal with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && DOM.pdfModal.classList.contains('active')) {
            closePDFModal();
        }
    });

    console.log('✅ Dashboard Initialized Successfully!');
});