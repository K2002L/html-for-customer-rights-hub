const root = document.documentElement;
const body = document.body;
const panel = document.querySelector('.accessibility-panel');
const toggleButtons = document.querySelectorAll('[data-action="toggle-accessibility-panel"]');

const settings = JSON.parse(localStorage.getItem('crh_accessibility') || '{}');
settings.fontScale = settings.fontScale || 1;
settings.pageScale = settings.pageScale || 1;
settings.highContrast = Boolean(settings.highContrast);
settings.easyRead = Boolean(settings.easyRead);
settings.panelOpen = settings.panelOpen !== false;

function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
}

function saveSettings() {
    localStorage.setItem('crh_accessibility', JSON.stringify(settings));
}

function applySettings() {
    root.style.setProperty('--font-scale', settings.fontScale.toFixed(2));
    root.style.setProperty('--page-scale', settings.pageScale.toFixed(2));
    body.classList.toggle('high-contrast', settings.highContrast);
    body.classList.toggle('easy-read', settings.easyRead);
    if (panel) {
        panel.classList.toggle('collapsed', !settings.panelOpen);
    }
    toggleButtons.forEach((btn) => {
        btn.setAttribute('aria-expanded', String(settings.panelOpen));
        if (btn.classList.contains('accessibility-toggle')) {
            btn.textContent = settings.panelOpen ? 'Hide Accessibility' : 'Accessibility';
        }
    });
    saveSettings();
}

document.addEventListener('click', (event) => {
    const action = event.target.dataset.action;
    if (!action) return;

    switch (action) {
        case 'increase-font':
            settings.fontScale = clamp(settings.fontScale + 0.1, 0.9, 1.6);
            break;
        case 'decrease-font':
            settings.fontScale = clamp(settings.fontScale - 0.1, 0.9, 1.6);
            break;
        case 'increase-zoom':
            settings.pageScale = clamp(settings.pageScale + 0.05, 0.9, 1.2);
            break;
        case 'decrease-zoom':
            settings.pageScale = clamp(settings.pageScale - 0.05, 0.9, 1.2);
            break;
        case 'toggle-contrast':
            settings.highContrast = !settings.highContrast;
            break;
        case 'toggle-easy':
            settings.easyRead = !settings.easyRead;
            break;
        case 'reset-accessibility':
            settings.fontScale = 1;
            settings.pageScale = 1;
            settings.highContrast = false;
            settings.easyRead = false;
            settings.panelOpen = true;
            break;
        case 'toggle-accessibility-panel':
            settings.panelOpen = !settings.panelOpen;
            break;
        default:
            return;
    }
    applySettings();
});

applySettings();

const modal = document.getElementById('appModal');
const modalTitle = document.getElementById('appModalTitle');
const modalBody = document.getElementById('appModalBody');

function openModal(title, html) {
    if (!modal || !modalTitle || !modalBody) return;
    modalTitle.textContent = title;
    modalBody.innerHTML = html;
    modal.hidden = false;
    body.classList.add('modal-open');
}

function renderLiveChatChooser() {
    openModal(
        'Live Chat',
        `
        <div class="live-chat-shell">
            <div class="live-chat-stage">
                <div class="live-chat-actions">
                    <button type="button" class="primary-btn live-chat-choice" data-open-chat="ai">AI Service</button>
                    <button type="button" class="primary-btn live-chat-choice" data-open-chat="human">Human Service</button>
                </div>
            </div>
        </div>
        `,
    );
}

function renderChatModal(mode) {
    const isAi = mode === 'ai';
    const title = isAi ? 'Chat with AI' : 'Chat with Human';
    const badge = isAi ? 'AI' : 'HS';
    const greeting = 'You can ask whatever you want';
    const humanNotice = 'Waiting for the human customer service representative to join the chat. Feel free to send your question here';

    openModal(
        title,
        `
        <div class="chat-modal-shell" data-chat-shell="${mode}">
            <div class="chat-modal-surface">
                ${isAi ? '' : `<div class="chat-notice-banner" data-human-chat-notice>${humanNotice}</div>`}
                <div class="chat-thread" data-chat-thread>
                    ${isAi ? `
                    <div class="chat-message-row">
                        <span class="chat-avatar">${badge}</span>
                        <div class="chat-message-bubble">${greeting}</div>
                    </div>
                    ` : ''}
                </div>
                <form class="chat-compose" data-chat-form="${mode}">
                    <textarea name="message" rows="2" placeholder="Enter your message"></textarea>
                    <button type="submit" class="primary-btn chat-send-btn">Send</button>
                </form>
            </div>
        </div>
        `,
    );
}

function closeModal() {
    if (!modal) return;
    modal.hidden = true;
    body.classList.remove('modal-open');
}

document.addEventListener('click', (event) => {
    const trigger = event.target.closest('[data-modal]');
    if (trigger) {
        const modalType = trigger.dataset.modal;
        if (modalType === 'start-chat') {
            renderLiveChatChooser();
        }
        if (modalType === 'call-support') {
            openModal(
                'Call Support',
                `
                <div class="modal-stack">
                    <p>Please call <strong>1-800-555-0911</strong>.</p>
                    <p>For active fraud, this number is available 24/7.</p>
                </div>
                `,
            );
        }
        if (modalType === 'schedule-consultation') {
            openModal(
                'Legal Consultation Schedule',
                `
                <div class="modal-stack">
                    <div class="schedule-list">
                        <div><strong>Mon-Fri 9:00 AM - 5:00 PM</strong><span>Legal intake clinic</span></div>
                        <div><strong>Mon-Fri 9:00 AM - 5:00 PM</strong><span>Consumer dispute consultation</span></div>
                        <div><strong>24/7</strong><span>Fraud recovery support</span></div>
                    </div>
                    <p>Email <strong>legal@consumerrights.org</strong> to reserve a slot.</p>
                </div>
                `,
            );
        }
        if (modalType === 'share-story') {
            openModal(
                'Share Your Story',
                `
                <form class="modal-stack" id="shareStoryForm">
                    <label>Story Title<input type="text" name="title" placeholder="Brief title"></label>
                    <label>Your Story<textarea name="story" rows="5" placeholder="Share what happened and how it was resolved"></textarea></label>
                    <button type="submit" class="primary-btn">Submit Story</button>
                </form>
                `,
            );
        }
    }

    const chatOpenTrigger = event.target.closest('[data-open-chat]');
    if (chatOpenTrigger) {
        renderChatModal(chatOpenTrigger.dataset.openChat);
    }

    const downloadTrigger = event.target.closest('[data-download-title]');
    if (downloadTrigger) {
        const title = downloadTrigger.dataset.downloadTitle;
        const meta = downloadTrigger.dataset.downloadMeta || '';
        openModal(
            'Download Started',
            `
            <div class="modal-stack">
                <p><strong>${title}</strong> is downloading.</p>
                <p>Please wait a moment...</p>
            </div>
            `,
        );

        window.setTimeout(() => {
            openModal(
                'Download Complete',
                `
                <div class="modal-stack">
                    <p><strong>${title}</strong> download complete.</p>
                    <p>${meta}</p>
                </div>
                `,
            );
            window.setTimeout(closeModal, 1800);
        }, 1800);
    }

    if (event.target.matches('[data-modal-close]')) {
        closeModal();
    }
});

document.addEventListener('click', (event) => {
    const choice = event.target.closest('[data-chat-mode]');
    if (!choice || !modalBody) return;
    const mode = choice.dataset.chatMode;
    const chatWindow = modalBody.querySelector('.chat-window');
    if (chatWindow) {
        chatWindow.innerHTML += `<div class="chat-bubble user-bubble"><strong>You:</strong> I want ${mode}.</div>`;
        chatWindow.innerHTML += `<div class="chat-bubble"><strong>${mode}:</strong> Thanks. Please describe your issue and case ID if you have one.</div>`;
    }
});

document.addEventListener('submit', (event) => {
    const chatForm = event.target.closest('[data-chat-form]');
    if (!chatForm || !modalBody) return;
    event.preventDefault();
    const textarea = chatForm.querySelector('textarea[name="message"]');
    const thread = modalBody.querySelector('[data-chat-thread]');
    const humanNotice = modalBody.querySelector('[data-human-chat-notice]');
    if (!textarea || !thread) return;

    const text = textarea.value.trim();
    if (!text) return;

    thread.innerHTML += `
        <div class="chat-message-row self">
            <div class="chat-message-bubble self">${text}</div>
        </div>
    `;

    const mode = chatForm.dataset.chatForm;
    if (mode === 'human' && humanNotice) {
        humanNotice.textContent = 'A service representative has join the chat.';
    }
    const reply = mode === 'ai'
        ? 'I can help explain the next steps, suggest evidence to gather, or guide you to the right page.'
        : "Hello, I'm the customer service representative Marry. How can I assist you?";

    thread.innerHTML += `
        <div class="chat-message-row">
            <span class="chat-avatar">${mode === 'ai' ? 'AI' : 'HS'}</span>
            <div class="chat-message-bubble">${reply}</div>
        </div>
    `;

    textarea.value = '';
});

document.addEventListener('submit', (event) => {
    if (event.target.id === 'shareStoryForm') {
        event.preventDefault();
        openModal(
            'Story Submitted',
            `
            <div class="modal-stack">
                <p>Your story has been submitted for review.</p>
                <p>Thank you for helping other consumers.</p>
            </div>
            `,
        );
        window.setTimeout(closeModal, 1800);
    }
});

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        closeModal();
    }
});
