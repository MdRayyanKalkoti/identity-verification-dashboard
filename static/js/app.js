// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    console.log('🔍 Dashboard Initializing...');

    // ===== App State =====
    const AppState = {
        authenticated: false,
        hasLoggedIn: false,
        currentSection: 'overview',
        identityData: null,
        sessionCheckInterval: null
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

    // ===== Utility =====
    const showError = msg => {
        DOM.errorMessage.textContent = msg;
        DOM.errorMessage.style.color = '#ef4444';
    };

    const showSuccess = msg => {
        DOM.errorMessage.textContent = msg;
        DOM.errorMessage.style.color = '#10b981';
    };

    const showWarning = msg => {
        DOM.errorMessage.textContent = msg;
        DOM.errorMessage.style.color = '#f59e0b';
    };

    const clearError = () => {
        DOM.errorMessage.textContent = '';
    };

    const resetUnlockButton = () => {
        DOM.unlockBtn.disabled = false;
        DOM.unlockBtn.innerHTML = '<span>Unlock Dashboard</span>';
    };

    // ===== Navigation =====
    const navigateToSection = (sectionId) => {
        DOM.navItems.forEach(item =>
            item.classList.toggle('active', item.dataset.section === sectionId)
        );

        DOM.sections.forEach(section =>
            section.classList.toggle('active', section.id === sectionId)
        );

        AppState.currentSection = sectionId;
    };

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

    // ===== Session Monitoring =====
    const checkSessionStatus = async () => {
        try {
            const res = await fetch('/api/status');
            const data = await res.json();

            if (data.password_changed && AppState.authenticated) {
                await handlePasswordChanged();
                return;
            }

            if (AppState.hasLoggedIn && AppState.authenticated && !data.authenticated) {
                await handleSessionExpired();
            }
        } catch (e) {
            console.error('Session check failed', e);
        }
    };

    const startSessionMonitoring = () => {
        if (!AppState.sessionCheckInterval) {
            AppState.sessionCheckInterval = setInterval(checkSessionStatus, 2000);
        }
    };

    const stopSessionMonitoring = () => {
        if (AppState.sessionCheckInterval) {
            clearInterval(AppState.sessionCheckInterval);
            AppState.sessionCheckInterval = null;
        }
    };

    // ===== Forced Logout =====
    const handlePasswordChanged = async () => {
        stopSessionMonitoring();
        AppState.authenticated = false;

        try {
            await fetch('/api/acknowledge-password-change', { method: 'POST' });
        } catch {}

        DOM.dashboard.classList.remove('active');
        DOM.dashboard.classList.add('blurred');
        DOM.lockOverlay.style.display = 'flex';
        DOM.lockOverlay.style.pointerEvents = 'auto';
        DOM.lockIcon.textContent = '🔒';
        DOM.passwordInput.value = '';

        showWarning('⚠️ Password changed. Please login again.');
        resetUnlockButton();
    };

    const handleSessionExpired = async () => {
        if (!AppState.hasLoggedIn) return;

        stopSessionMonitoring();
        AppState.authenticated = false;

        DOM.dashboard.classList.remove('active');
        DOM.dashboard.classList.add('blurred');
        DOM.lockOverlay.style.display = 'flex';
        DOM.lockOverlay.style.pointerEvents = 'auto';
        DOM.lockIcon.textContent = '🔒';
        DOM.passwordInput.value = '';

        showError('Session expired. Please login again.');
        resetUnlockButton();
    };

    // ===== API =====
    const API = {
        async verifyPassword(password) {
            const res = await fetch('/api/verify-password', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ password })
            });
            return res.json();
        },
        async getIdentity() {
            const res = await fetch('/api/identity');
            return res.json();
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
                    DOM.lockOverlay.style.pointerEvents = 'none';
                    DOM.dashboard.classList.remove('blurred');
                    DOM.dashboard.classList.add('active');

                    AppState.authenticated = true;
                    AppState.hasLoggedIn = true;

                    resetUnlockButton();
                    loadDashboardData();
                    startSessionMonitoring();
                }, 600);
            } else {
                showError(result.error || 'Invalid password');
                resetUnlockButton();
            }
        } catch {
            showError('Connection error');
            resetUnlockButton();
        }
    };

    // ===== Identity =====
    const loadDashboardData = async () => {
        try {
            const result = await API.getIdentity();
            if (result.success) {
                DOM.identityData.innerHTML = `
                    <div class="info-item"><div class="info-label">Full Name</div><div class="info-value">${result.data.name}</div></div>
                    <div class="info-item"><div class="info-label">Aadhaar Number</div><div class="info-value">${result.data.aadhaar}</div></div>
                    <div class="info-item"><div class="info-label">PAN Number</div><div class="info-value">${result.data.pan}</div></div>
                    <div class="info-item"><div class="info-label">Passport Number</div><div class="info-value">${result.data.passport}</div></div>
                    <div class="info-item"><div class="info-label">Date of Birth</div><div class="info-value">${result.data.dob}</div></div>
                `;
            }
        } catch (e) {
            console.error('Identity load failed', e);
        }
    };

    // ===== PDF Modal (FROM CLAUDE – PRESERVED) =====
    const openPDFModal = (docType) => {
        const titles = {
            aadhaar: 'Aadhaar Card',
            pan: 'PAN Card',
            passport: 'Passport'
        };

        if (!DOM.pdfModal || !DOM.pdfViewer) {
            window.open('/api/documents/' + docType, '_blank');
            return;
        }

        DOM.pdfTitle.textContent = titles[docType] || 'Document Viewer';
        DOM.pdfViewer.src = `/api/documents/${docType}#toolbar=0&navpanes=0&scrollbar=0&view=FitH`;
        DOM.pdfModal.classList.add('active');
    };

    const closePDFModal = () => {
        DOM.pdfModal.classList.remove('active');
        DOM.pdfViewer.src = '';
    };

    // ===== Event Listeners =====
    DOM.unlockBtn.addEventListener('click', handleUnlock);
    DOM.passwordInput.addEventListener('keypress', e => {
        if (e.key === 'Enter') handleUnlock();
    });

    DOM.logoutBtn.addEventListener('click', async () => {
        if (confirm('Logout?')) {
            stopSessionMonitoring();
            await fetch('/api/logout', { method: 'POST' });
            location.reload();
        }
    });

    // ===== Document Buttons (FROM CLAUDE – PRESERVED) =====
    document.querySelectorAll('.doc-btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();

            const docType = this.getAttribute('data-doc');
            const action = this.getAttribute('data-action');

            if (action === 'view') {
                openPDFModal(docType);
            } else if (action === 'download') {
                window.location.href = `/api/documents/${docType}?action=download`;
            }
        });
    });

    // ===== Report =====
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

    if (DOM.pdfClose) DOM.pdfClose.addEventListener('click', closePDFModal);
    if (DOM.pdfModal) {
        DOM.pdfModal.addEventListener('click', e => {
            if (e.target === DOM.pdfModal) closePDFModal();
        });
    }

    document.addEventListener('keydown', e => {
        if (e.key === 'Escape' && DOM.pdfModal.classList.contains('active')) {
            closePDFModal();
        }
    });

    console.log('✅ Dashboard Ready');
});
