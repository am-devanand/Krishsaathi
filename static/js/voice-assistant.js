/**
 * Voice Assistant UI & Logic
 * Handles Floating UI, Speech Recognition, TTS, Backend Communication, and Form Filling.
 * Now includes TEXT INPUT fallback for when voice doesn't work.
 */

class VoiceAssistant {
    constructor() {
        this.isOpen = false;
        this.isListening = false;
        this.messages = [];
        this.conversationId = null;

        // UI Elements
        this.container = null;
        this.triggerBtn = null;
        this.overlay = null;
        this.messagesContainer = null;
        this.statusText = null;
        this.micBtn = null;
        this.textInput = null;
        this.sendBtn = null;

        this.init();
    }

    init() {
        this.createUI();
        this.loadHistory();
        this.attachEvents();

        this.isProfilePage = document.querySelector('.profile-form') !== null;
    }

    createUI() {
        // 1. Trigger Button
        this.triggerBtn = document.createElement('button');
        this.triggerBtn.className = 'voice-trigger-btn';
        this.triggerBtn.innerHTML = `
      <svg viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/></svg>
    `;
        this.triggerBtn.title = "Voice Assistant";
        document.body.appendChild(this.triggerBtn);

        // 2. Overlay with TEXT INPUT
        this.overlay = document.createElement('div');
        this.overlay.className = 'voice-overlay hidden';
        this.overlay.innerHTML = `
      <div class="voice-header">
        <h3>🎤 Voice Assistant</h3>
        <button class="voice-close-btn">&times;</button>
      </div>
      <div class="voice-messages"></div>
      <div class="voice-input-area">
        <input type="text" class="voice-text-input" placeholder="Type your message..." />
        <button class="voice-send-btn" title="Send">➤</button>
      </div>
      <div class="voice-controls">
        <button class="voice-mic-btn" title="Click to speak">
          <svg style="width:20px;height:20px;fill:currentColor" viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/></svg>
        </button>
        <span class="voice-status">Type or tap mic to speak</span>
      </div>
    `;
        document.body.appendChild(this.overlay);

        this.messagesContainer = this.overlay.querySelector('.voice-messages');
        this.statusText = this.overlay.querySelector('.voice-status');
        this.micBtn = this.overlay.querySelector('.voice-mic-btn');
        this.textInput = this.overlay.querySelector('.voice-text-input');
        this.sendBtn = this.overlay.querySelector('.voice-send-btn');
    }

    attachEvents() {
        this.triggerBtn.addEventListener('click', () => this.toggle());

        this.overlay.querySelector('.voice-close-btn').addEventListener('click', () => this.toggle(false));

        this.micBtn.addEventListener('click', () => {
            if (this.isListening) {
                this.stopListening();
            } else {
                this.startListening();
            }
        });

        // Text input events
        this.sendBtn.addEventListener('click', () => this.sendTextMessage());
        this.textInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendTextMessage();
        });
    }

    sendTextMessage() {
        const text = this.textInput.value.trim();
        if (text) {
            this.textInput.value = '';
            this.handleUserMessage(text);
        }
    }

    toggle(state) {
        this.isOpen = state !== undefined ? state : !this.isOpen;
        if (this.isOpen) {
            this.overlay.classList.remove('hidden');
            this.triggerBtn.style.display = 'none';
            if (this.messages.length === 0) this.greet();
            this.textInput.focus();
        } else {
            this.overlay.classList.add('hidden');
            this.triggerBtn.style.display = 'flex';
            this.stopListening();
        }
    }

    appendMessage(text, isUser) {
        const msg = document.createElement('div');
        msg.className = `voice-msg ${isUser ? 'user' : 'bot'}`;
        msg.textContent = text;
        this.messagesContainer.appendChild(msg);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        this.messages.push({ text, isUser });
    }

    setStatus(text) {
        this.statusText.textContent = text;
    }

    async loadHistory() {
        try {
            const res = await fetch('/api/voice/history');
            const data = await res.json();
            if (data.history && Array.isArray(data.history)) {
                data.history.forEach(m => this.appendMessage(m.text, m.is_user));
            }
        } catch (e) {
            console.error("Failed to load history", e);
        }
    }

    greet() {
        const greeting = window.i18n
            ? window.i18n.t('greeting', 'chatbot', { name: (window.currentUser?.name || 'Farmer') })
            : "Hello! I'm your farming assistant. How can I help you today?";
        this.appendMessage(greeting, false);
        this.speak(greeting);
    }

    startListening() {
        // Check if voice handler exists
        if (!window.voiceHandler || !window.voiceHandler.recognition) {
            this.setStatus("❌ Voice not supported. Please type your message.");
            console.log("Voice handler not available");
            return;
        }

        this.isListening = true;
        this.micBtn.classList.add('listening');
        this.setStatus("🎤 Listening... Speak now!");

        try {
            window.voiceHandler.start(
                (transcript) => {
                    this.stopListening();
                    if (transcript && transcript.trim()) {
                        this.handleUserMessage(transcript);
                    } else {
                        this.setStatus("🔇 No speech detected. Try again or type.");
                    }
                },
                (error) => {
                    console.error("Voice recognition error:", error);
                    this.stopListening();

                    // Map common errors to user-friendly messages
                    const errorMsg = String(error.error || error.message || error || 'unknown');

                    if (errorMsg.includes('no-speech')) {
                        this.setStatus("🔇 No speech detected. Speak louder or tap mic again.");
                    } else if (errorMsg.includes('not-allowed') || errorMsg.includes('denied')) {
                        this.setStatus("🔒 Mic blocked. Click lock icon in address bar to allow.");
                    } else if (errorMsg.includes('network')) {
                        this.setStatus("🌐 Network error. Check internet connection.");
                    } else if (errorMsg.includes('audio-capture')) {
                        this.setStatus("🎤 Mic not available. Connect a microphone.");
                    } else {
                        this.setStatus("⌨️ Voice unavailable. Please type your message.");
                    }
                }
            );
        } catch (e) {
            console.error("Failed to start voice:", e);
            this.stopListening();
            this.setStatus("⌨️ Voice error. Please type your message.");
        }
    }

    stopListening() {
        this.isListening = false;
        this.micBtn.classList.remove('listening');
        this.setStatus("Type or tap mic to speak");
        if (window.voiceHandler) window.voiceHandler.stop();
    }

    async handleUserMessage(text) {
        if (!text) return;
        this.appendMessage(text, true);
        this.setStatus("🤔 Thinking...");

        try {
            const payload = {
                message: text,
                conversation_id: this.conversationId
            };

            const res = await fetch('/api/chatbot/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept-Language': window.i18n ? window.i18n.getCurrentLanguage() : 'hi'
                },
                body: JSON.stringify(payload)
            });

            const data = await res.json();

            if (data.reply) {
                this.appendMessage(data.reply, false);
                this.speak(data.reply);

                if (data.conversation_id) this.conversationId = data.conversation_id;
                this.checkForFormUpdates(data.reply);
            } else {
                this.appendMessage("Sorry, I couldn't understand. Please try again.", false);
            }
            this.setStatus("Type or tap mic to speak");

        } catch (e) {
            this.setStatus("Connection error. Try again.");
            console.error(e);
            this.appendMessage("Sorry, couldn't connect to server. Please try again.", false);
        }
    }

    speak(text) {
        if (window.voiceHandler && window.voiceHandler.speak) {
            window.voiceHandler.speak(text, window.i18n ? window.i18n.getCurrentLanguage() : 'hi');
        }
    }

    checkForFormUpdates(reply) {
        if (reply.includes("Updated:") || reply.includes("अपडेट")) {
            const stateMatch = reply.match(/State=([^,]+)/i) || reply.match(/राज्य=([^,]+)/);
            const districtMatch = reply.match(/District=([^,.]+)/i) || reply.match(/ज़िला=([^,.]+)/);

            if (this.isProfilePage) {
                if (stateMatch) {
                    this.setSelectValue('profile-state', stateMatch[1].trim());
                    this.pulseField('profile-state');
                }
                if (districtMatch) {
                    const distInput = document.getElementById('profile-district');
                    if (distInput) distInput.value = districtMatch[1].trim();
                    this.pulseField('profile-district');
                }
            }
        }
    }

    setSelectValue(id, textValue) {
        const sel = document.getElementById(id);
        if (!sel) return;
        for (let i = 0; i < sel.options.length; i++) {
            if (sel.options[i].text.toLowerCase().includes(textValue.toLowerCase())) {
                sel.selectedIndex = i;
                return;
            }
        }
        sel.value = textValue;
    }

    pulseField(id) {
        const el = document.getElementById(id);
        if (el) {
            el.style.transition = 'box-shadow 0.5s';
            el.style.boxShadow = '0 0 10px #4caf50';
            setTimeout(() => el.style.boxShadow = '', 1000);
        }
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    window.voiceAssistant = new VoiceAssistant();
});
