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

function renderScreenReaderModal() {
    openModal(
        'Screen Reader',
        `
        <div class="screenreader-shell">
            <div class="screenreader-panel">
                <div class="screenreader-controls">
                    <button type="button" class="screenreader-icon-btn" data-screenreader-demo="previous" aria-label="Previous section">⏮</button>
                    <button type="button" class="screenreader-icon-btn" data-screenreader-demo="next" aria-label="Next section">⏭</button>
                    <button type="button" class="screenreader-icon-btn active" data-screenreader-demo="play" aria-label="Play reading">▶</button>
                    <button type="button" class="screenreader-icon-btn" data-screenreader-demo="stop" aria-label="Stop reading">■</button>
                </div>
                <div class="screenreader-status" data-screenreader-status>Ready to read the current page aloud.</div>
                <div class="screenreader-row">
                    <span class="screenreader-row-icon">🔊</span>
                    <div class="screenreader-row-content">
                        <strong>Volume Control</strong>
                        <div class="screenreader-inline-control">
                            <button type="button" class="screenreader-adjust-btn" data-screenreader-volume-step="-10" aria-label="Decrease volume">-</button>
                            <span class="screenreader-value" data-screenreader-volume-value>70%</span>
                            <button type="button" class="screenreader-adjust-btn" data-screenreader-volume-step="10" aria-label="Increase volume">+</button>
                        </div>
                    </div>
                </div>
                <div class="screenreader-row">
                    <span class="screenreader-row-icon">⏱</span>
                    <div class="screenreader-row-content">
                        <strong>Playback Speed</strong>
                        <div class="screenreader-speed-group">
                            <button type="button" class="screenreader-speed-btn" data-screenreader-speed="0.75x">0.75x</button>
                            <button type="button" class="screenreader-speed-btn active" data-screenreader-speed="1x">1x</button>
                            <button type="button" class="screenreader-speed-btn" data-screenreader-speed="1.25x">1.25x</button>
                            <button type="button" class="screenreader-speed-btn" data-screenreader-speed="1.5x">1.5x</button>
                        </div>
                    </div>
                </div>
                <div class="screenreader-row">
                    <span class="screenreader-row-icon">🖱</span>
                    <div class="screenreader-row-content">
                        <div class="screenreader-listen-toggle">
                            <span class="screenreader-listen-label">Click and Listen</span>
                            <button type="button" class="screenreader-toggle-btn" data-screenreader-toggle aria-label="Click and Listen" aria-pressed="false">
                                <span class="screenreader-toggle-knob"></span>
                                <span class="screenreader-toggle-close" data-screenreader-toggle-icon>✕</span>
                            </button>
                        </div>
                    </div>
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
        if (modalType === 'screen-reader') {
            renderScreenReaderModal();
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
                        <div><strong>Mon-Sun 0:00 AM - 24:00 PM</strong><span>Fraud recovery support</span></div>
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

document.addEventListener('click', (event) => {
    const demoTrigger = event.target.closest('[data-screenreader-demo]');
    const speedTrigger = event.target.closest('[data-screenreader-speed]');
    const toggleTrigger = event.target.closest('[data-screenreader-toggle]');
    const volumeStepTrigger = event.target.closest('[data-screenreader-volume-step]');
    const status = modalBody?.querySelector('[data-screenreader-status]');

    if (toggleTrigger && modalBody) {
        const isActive = toggleTrigger.classList.toggle('active');
        toggleTrigger.setAttribute('aria-pressed', String(isActive));
        const icon = toggleTrigger.querySelector('[data-screenreader-toggle-icon]');
        if (icon) {
            icon.textContent = isActive ? '✓' : '✕';
        }
        if (status) {
            status.textContent = isActive
                ? 'Click and Listen is enabled. Select page content to hear it read aloud.'
                : 'Click and Listen is turned off.';
        }
        return;
    }

    if (volumeStepTrigger && modalBody) {
        const volumeValue = modalBody.querySelector('[data-screenreader-volume-value]');
        if (!volumeValue) return;
        const current = Number.parseInt(volumeValue.textContent, 10) || 70;
        const step = Number.parseInt(volumeStepTrigger.dataset.screenreaderVolumeStep, 10) || 0;
        const next = Math.min(100, Math.max(0, current + step));
        volumeValue.textContent = `${next}%`;
        if (status) {
            status.textContent = `Volume adjusted to ${next}%.`;
        }
        return;
    }

    if (demoTrigger && modalBody) {
        const groupedActions = ['previous', 'next', 'play', 'stop'];
        if (groupedActions.includes(demoTrigger.dataset.screenreaderDemo)) {
            modalBody.querySelectorAll('[data-screenreader-demo]').forEach((button) => {
                if (groupedActions.includes(button.dataset.screenreaderDemo)) {
                    button.classList.toggle('active', button === demoTrigger);
                }
            });
        }
    }

    if (speedTrigger && modalBody) {
        modalBody.querySelectorAll('[data-screenreader-speed]').forEach((button) => {
            button.classList.toggle('active', button === speedTrigger);
        });
        if (status) {
            status.textContent = `Playback speed set to ${speedTrigger.dataset.screenreaderSpeed}.`;
        }
    }

    if (!demoTrigger || !status) return;

    const action = demoTrigger.dataset.screenreaderDemo;
    const messages = {
        previous: 'Moved to the previous readable section.',
        next: 'Moved to the next readable section.',
        play: 'Screen reader audio preview is ready.',
        stop: 'Screen reader playback stopped.',
        'play-page': 'Reading the current page aloud now.',
    };

    status.textContent = messages[action] || 'Screen reader updated.';
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

document.querySelectorAll('[data-file-upload-input]').forEach((input) => {
    const targetId = input.dataset.fileNameTarget;
    const nameLabel = targetId ? document.getElementById(targetId) : null;
    const listId = input.dataset.fileListTarget;
    const fileList = listId ? document.getElementById(listId) : null;
    if (!nameLabel) return;

    let selectedFiles = [];

    const applySelectedFilesToInput = () => {
        const transfer = new DataTransfer();
        selectedFiles.forEach((file) => transfer.items.add(file));
        input.files = transfer.files;
    };

    const renderFileList = () => {
        if (!fileList) return;
        fileList.innerHTML = '';
        selectedFiles.forEach((file, index) => {
            const item = document.createElement('li');
            const name = document.createElement('span');
            name.textContent = file.name;
            const removeButton = document.createElement('button');
            removeButton.type = 'button';
            removeButton.className = 'file-upload-remove';
            removeButton.setAttribute('aria-label', `Remove ${file.name}`);
            removeButton.textContent = '×';
            removeButton.addEventListener('click', (event) => {
                event.preventDefault();
                event.stopPropagation();
                selectedFiles = selectedFiles.filter((_, i) => i !== index);
                syncFileState();
            });
            item.appendChild(name);
            item.appendChild(removeButton);
            fileList.appendChild(item);
        });
        fileList.hidden = selectedFiles.length === 0;
    };

    const syncFileState = () => {
        applySelectedFilesToInput();
        nameLabel.textContent = selectedFiles.length === 0
            ? 'No file selected'
            : `${selectedFiles.length} file${selectedFiles.length > 1 ? 's' : ''} selected`;
        renderFileList();
    };

    input.addEventListener('change', () => {
        const incomingFiles = Array.from(input.files || []);
        if (incomingFiles.length === 0) return;
        incomingFiles.forEach((file) => {
            const exists = selectedFiles.some(
                (current) =>
                    current.name === file.name
                    && current.size === file.size
                    && current.lastModified === file.lastModified,
            );
            if (!exists) {
                selectedFiles.push(file);
            }
        });
        syncFileState();
    });

    syncFileState();
});
