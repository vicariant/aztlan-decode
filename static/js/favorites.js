// ========================================
// SISTEMA DE FAVORITOS
// ========================================
// Persistencia en LocalStorage

class FavoritesManager {
    constructor() {
        this.storageKey = 'aztlan_favorites';
        this.favorites = this.loadFavorites();
    }
    
    loadFavorites() {
        const stored = localStorage.getItem(this.storageKey);
        return stored ? JSON.parse(stored) : [];
    }
    
    saveFavorites() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.favorites));
    }
    
    addFavorite(team) {
        if (!this.isFavorite(team.number)) {
            this.favorites.push({
                number: team.number,
                name: team.name || `Team ${team.number}`,
                opr: team.opr || 0,
                wins: team.wins || 0,
                losses: team.losses || 0,
                addedAt: new Date().toISOString()
            });
            this.saveFavorites();
            this.updateUI();
            this.showNotification(`⭐ Equipo ${team.number} agregado a favoritos`);
            return true;
        }
        return false;
    }
    
    removeFavorite(teamNumber) {
        this.favorites = this.favorites.filter(t => t.number !== teamNumber);
        this.saveFavorites();
        this.updateUI();
        this.showNotification(`❌ Equipo ${teamNumber} removido de favoritos`);
    }
    
    isFavorite(teamNumber) {
        return this.favorites.some(t => t.number === teamNumber);
    }
    
    getFavorites() {
        return this.favorites;
    }
    
    updateUI() {
        // Update star buttons
        document.querySelectorAll('.favorite-btn').forEach(btn => {
            const teamNumber = parseInt(btn.dataset.teamNumber);
            if (this.isFavorite(teamNumber)) {
                btn.innerHTML = '⭐';
                btn.classList.add('active');
                btn.title = 'Remover de favoritos';
            } else {
                btn.innerHTML = '☆';
                btn.classList.remove('active');
                btn.title = 'Agregar a favoritos';
            }
        });
        
        // Update favorites sidebar
        this.renderFavoritesSidebar();
    }
    
    renderFavoritesSidebar() {
        const sidebar = document.getElementById('favorites-sidebar');
        if (!sidebar) return;
        
        if (this.favorites.length === 0) {
            sidebar.innerHTML = `
                <div class="empty-favorites">
                    <p>⭐ No hay favoritos</p>
                    <small>Haz clic en ☆ para agregar equipos</small>
                </div>
            `;
            return;
        }
        
        const html = this.favorites.map(team => `
            <div class="favorite-item" data-team="${team.number}">
                <div class="favorite-info">
                    <div class="favorite-number">#${team.number}</div>
                    <div class="favorite-name">${team.name}</div>
                    <div class="favorite-stats">
                        OPR: ${team.opr} | W-L: ${team.wins}-${team.losses}
                    </div>
                </div>
                <div class="favorite-actions">
                    <button onclick="viewTeam(${team.number})" class="btn-mini">👁️</button>
                    <button onclick="favoritesManager.removeFavorite(${team.number})" class="btn-mini">🗑️</button>
                </div>
            </div>
        `).join('');
        
        sidebar.innerHTML = html;
    }
    
    showNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'notification-toast';
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => notification.classList.add('show'), 10);
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    exportFavorites() {
        const dataStr = JSON.stringify(this.favorites, null, 2);
        const blob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'aztlan_favorites.json';
        link.click();
    }
    
    compareAllFavorites() {
        if (this.favorites.length < 2) {
            alert('Necesitas al menos 2 equipos favoritos para comparar');
            return;
        }
        
        const numbers = this.favorites.map(t => t.number).join(',');
        window.location.href = `/compare-multiple?teams=${numbers}`;
    }
}

// Initialize global instance
const favoritesManager = new FavoritesManager();

// Create favorite button
function createFavoriteButton(teamNumber, teamData = {}) {
    const btn = document.createElement('button');
    btn.className = 'favorite-btn';
    btn.dataset.teamNumber = teamNumber;
    btn.onclick = () => {
        if (favoritesManager.isFavorite(teamNumber)) {
            favoritesManager.removeFavorite(teamNumber);
        } else {
            favoritesManager.addFavorite({
                number: teamNumber,
                name: teamData.name,
                opr: teamData.opr,
                wins: teamData.wins,
                losses: teamData.losses
            });
        }
    };
    return btn;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    favoritesManager.updateUI();
});
