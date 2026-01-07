// ========================================
// HISTORIAL DE BÚSQUEDAS
// ========================================

class SearchHistory {
    constructor() {
        this.storageKey = 'aztlan_search_history';
        this.maxItems = 20;
        this.history = this.loadHistory();
    }
    
    loadHistory() {
        const stored = localStorage.getItem(this.storageKey);
        return stored ? JSON.parse(stored) : [];
    }
    
    saveHistory() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.history));
    }
    
    addSearch(searchData) {
        const entry = {
            type: searchData.type, // 'team', 'planet', 'comparison', etc
            query: searchData.query,
            displayText: searchData.displayText,
            url: searchData.url || window.location.pathname + window.location.search,
            timestamp: new Date().toISOString()
        };
        
        // Remove duplicate if exists
        this.history = this.history.filter(h => 
            !(h.type === entry.type && h.query === entry.query)
        );
        
        // Add to beginning
        this.history.unshift(entry);
        
        // Keep only maxItems
        if (this.history.length > this.maxItems) {
            this.history = this.history.slice(0, this.maxItems);
        }
        
        this.saveHistory();
        this.updateUI();
    }
    
    clearHistory() {
        if (confirm('¿Borrar todo el historial de búsquedas?')) {
            this.history = [];
            this.saveHistory();
            this.updateUI();
        }
    }
    
    removeItem(index) {
        this.history.splice(index, 1);
        this.saveHistory();
        this.updateUI();
    }
    
    getRecentSearches(limit = 5) {
        return this.history.slice(0, limit);
    }
    
    formatTimestamp(isoString) {
        const date = new Date(isoString);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);
        
        if (diffMins < 1) return 'Ahora';
        if (diffMins < 60) return `Hace ${diffMins} min`;
        if (diffHours < 24) return `Hace ${diffHours} hora${diffHours > 1 ? 's' : ''}`;
        if (diffDays < 7) return `Hace ${diffDays} día${diffDays > 1 ? 's' : ''}`;
        return date.toLocaleDateString('es-MX');
    }
    
    getIconForType(type) {
        const icons = {
            'team': '🤖',
            'planet': '🪐',
            'comparison': '⚔️',
            'regional': '🏆',
            'spider': '🕸️',
            'oracle': '🔮',
            'quetzal': '🧠'
        };
        return icons[type] || '🔍';
    }
    
    updateUI() {
        const container = document.getElementById('search-history');
        if (!container) return;
        
        if (this.history.length === 0) {
            container.innerHTML = `
                <div class="empty-history">
                    <p>📜 Sin historial</p>
                    <small>Tus búsquedas aparecerán aquí</small>
                </div>
            `;
            return;
        }
        
        const html = `
            <div class="history-header">
                <h3>📜 Historial Reciente</h3>
                <button onclick="searchHistory.clearHistory()" class="btn-clear">🗑️ Limpiar</button>
            </div>
            <div class="history-list">
                ${this.history.map((item, index) => `
                    <div class="history-item">
                        <a href="${item.url}" class="history-link">
                            <span class="history-icon">${this.getIconForType(item.type)}</span>
                            <div class="history-content">
                                <div class="history-text">${item.displayText}</div>
                                <div class="history-time">${this.formatTimestamp(item.timestamp)}</div>
                            </div>
                        </a>
                        <button onclick="searchHistory.removeItem(${index})" class="btn-remove">×</button>
                    </div>
                `).join('')}
            </div>
        `;
        
        container.innerHTML = html;
    }
    
    renderQuickAccess() {
        const recent = this.getRecentSearches(3);
        if (recent.length === 0) return '';
        
        return `
            <div class="quick-access">
                <h4>⚡ Acceso Rápido</h4>
                ${recent.map(item => `
                    <a href="${item.url}" class="quick-link">
                        ${this.getIconForType(item.type)} ${item.displayText}
                    </a>
                `).join('')}
            </div>
        `;
    }
}

// Initialize global instance
const searchHistory = new SearchHistory();

// Helper function to track searches
function trackSearch(type, query, displayText, url = null) {
    searchHistory.addSearch({
        type: type,
        query: query,
        displayText: displayText,
        url: url
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    searchHistory.updateUI();
});
