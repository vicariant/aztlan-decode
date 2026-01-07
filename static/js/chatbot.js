/**
 * AZTLÁN CHATBOT - Sistema de asistencia IA
 * Widget interactivo con Groq AI
 */

class AztlanChatbot {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.context = {};
        this.init();
    }

    init() {
        this.createWidget();
        this.attachEventListeners();
        this.addWelcomeMessage();
    }

    createWidget() {
        const widget = document.createElement('div');
        widget.className = 'chatbot-widget';
        widget.innerHTML = `
            <button class="chatbot-toggle" id="chatbotToggle" title="Abrir Asistente IA">
                💬
            </button>
            <div class="chatbot-window" id="chatbotWindow">
                <div class="chatbot-header">
                    <h3>🤖 AZTLÁN AI</h3>
                    <button class="chatbot-close" id="chatbotClose">×</button>
                </div>
                <div class="chatbot-messages" id="chatbotMessages"></div>
                <div class="chatbot-suggestions" id="chatbotSuggestions"></div>
                <div class="chatbot-input-area">
                    <input 
                        type="text" 
                        class="chatbot-input" 
                        id="chatbotInput" 
                        placeholder="Pregunta sobre FTC o exoplanetas..."
                        maxlength="500"
                    />
                    <button class="chatbot-send" id="chatbotSend">
                        ➤
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(widget);

        this.elements = {
            toggle: document.getElementById('chatbotToggle'),
            window: document.getElementById('chatbotWindow'),
            close: document.getElementById('chatbotClose'),
            messages: document.getElementById('chatbotMessages'),
            suggestions: document.getElementById('chatbotSuggestions'),
            input: document.getElementById('chatbotInput'),
            send: document.getElementById('chatbotSend')
        };
    }

    attachEventListeners() {
        this.elements.toggle.addEventListener('click', () => this.toggle());
        this.elements.close.addEventListener('click', () => this.toggle());
        this.elements.send.addEventListener('click', () => this.sendMessage());
        this.elements.input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }

    toggle() {
        this.isOpen = !this.isOpen;
        this.elements.window.classList.toggle('active', this.isOpen);
        if (this.isOpen) {
            this.elements.input.focus();
            this.updateSuggestions();
        }
    }

    addWelcomeMessage() {
        const welcomeMsg = `¡Hola! Soy AZTLÁN AI con acceso a datos reales:

🔍 **Búsquedas en tiempo real:**
• Equipos FTC (ej: "equipo 16418", "busca #254")
• Exoplanetas NASA (próximamente)
• Estadísticas y análisis

💡 **Ejemplos:**
- "Info del equipo 16418"
- "¿Qué es el OPR?"
- "Explica el récord WLT"

¿Qué quieres saber?`;
        this.addMessage(welcomeMsg, 'bot');
    }

    addMessage(text, sender = 'user') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chatbot-message ${sender}`;
        messageDiv.innerHTML = `
            <div class="message-bubble">
                ${this.formatMessage(text)}
            </div>
        `;
        this.elements.messages.appendChild(messageDiv);
        this.elements.messages.scrollTop = this.elements.messages.scrollHeight;

        this.messages.push({ text, sender, timestamp: new Date() });
    }

    formatMessage(text) {
        // Convertir markdown básico y emojis
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>')
            .replace(/•/g, '•');
    }

    showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'chatbot-message bot';
        indicator.id = 'typingIndicator';
        indicator.innerHTML = `
            <div class="message-bubble">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        this.elements.messages.appendChild(indicator);
        this.elements.messages.scrollTop = this.elements.messages.scrollHeight;
    }

    hideTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) indicator.remove();
    }

    async sendMessage() {
        const message = this.elements.input.value.trim();
        if (!message) return;

        // Agregar mensaje del usuario
        this.addMessage(message, 'user');
        this.elements.input.value = '';
        this.elements.send.disabled = true;

        // Mostrar indicador de escritura
        this.showTypingIndicator();

        try {
            // Enviar a la API
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    context: this.context
                })
            });

            const data = await response.json();

            this.hideTypingIndicator();

            if (data.success) {
                this.addMessage(data.response, 'bot');
            } else {
                this.addMessage(
                    `⚠️ ${data.error || 'Error al procesar tu mensaje'}`, 
                    'bot'
                );
            }

        } catch (error) {
            console.error('Error en chatbot:', error);
            this.hideTypingIndicator();
            this.addMessage(
                '⚠️ Error de conexión. Verifica que el servidor esté activo.', 
                'bot'
            );
        } finally {
            this.elements.send.disabled = false;
            this.updateSuggestions();
        }
    }

    updateContext(newContext) {
        this.context = { ...this.context, ...newContext };
    }

    updateSuggestions() {
        // Sugerencias contextuales según la página actual
        const page = window.location.pathname;
        let suggestions = [];

        if (page.includes('scouting') || page.includes('ftc')) {
            suggestions = [
                'Info del equipo 16418',
                '¿Qué es TRIDENTE?',
                'Explica el OPR',
                'Récord WLT'
            ];
        } else if (page.includes('astronomy') || page.includes('astlan')) {
            suggestions = [
                '¿Qué es un exoplaneta?',
                'Zona habitable',
                'Radio planetario',
                'Tipos de planetas'
            ];
        } else {
            suggestions = [
                'Busca equipo 254',
                'Info del equipo 16418',
                'Funciones disponibles',
                '¿Cómo funciona FTC Scout?'
            ];
        }

        this.elements.suggestions.innerHTML = suggestions
            .map(s => `<button class="suggestion-chip" data-suggestion="${s}">${s}</button>`)
            .join('');

        // Event listeners para sugerencias
        this.elements.suggestions.querySelectorAll('.suggestion-chip').forEach(chip => {
            chip.addEventListener('click', () => {
                this.elements.input.value = chip.dataset.suggestion;
                this.sendMessage();
            });
        });
    }

    clearHistory() {
        this.messages = [];
        this.elements.messages.innerHTML = '';
        this.addWelcomeMessage();
    }
}

// Inicializar chatbot cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.aztlanChatbot = new AztlanChatbot();
    console.log('🤖 AZTLÁN AI Chatbot inicializado');
});

// Función global para actualizar contexto desde otras páginas
function updateChatbotContext(context) {
    if (window.aztlanChatbot) {
        window.aztlanChatbot.updateContext(context);
    }
}
