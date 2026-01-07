// ========================================
// SISTEMA DE NOTAS POR EQUIPO
// ========================================

class TeamNotesManager {
    constructor() {
        this.storageKey = 'aztlan_team_notes';
        this.notes = this.loadNotes();
    }
    
    loadNotes() {
        const stored = localStorage.getItem(this.storageKey);
        return stored ? JSON.parse(stored) : {};
    }
    
    saveNotes() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.notes));
    }
    
    getTeamNotes(teamNumber) {
        return this.notes[teamNumber] || {
            text: '',
            tags: [],
            rating: 0,
            photos: [],
            createdAt: null,
            updatedAt: null
        };
    }
    
    saveTeamNote(teamNumber, noteData) {
        const existing = this.notes[teamNumber] || {};
        
        this.notes[teamNumber] = {
            text: noteData.text || existing.text || '',
            tags: noteData.tags || existing.tags || [],
            rating: noteData.rating !== undefined ? noteData.rating : existing.rating || 0,
            photos: noteData.photos || existing.photos || [],
            createdAt: existing.createdAt || new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };
        
        this.saveNotes();
        this.showNotification(`📝 Nota guardada para equipo ${teamNumber}`);
    }
    
    addTag(teamNumber, tag) {
        const notes = this.getTeamNotes(teamNumber);
        if (!notes.tags.includes(tag)) {
            notes.tags.push(tag);
            this.saveTeamNote(teamNumber, notes);
        }
    }
    
    removeTag(teamNumber, tag) {
        const notes = this.getTeamNotes(teamNumber);
        notes.tags = notes.tags.filter(t => t !== tag);
        this.saveTeamNote(teamNumber, notes);
    }
    
    deleteTeamNotes(teamNumber) {
        if (confirm(`¿Eliminar todas las notas del equipo ${teamNumber}?`)) {
            delete this.notes[teamNumber];
            this.saveNotes();
            this.showNotification(`🗑️ Notas del equipo ${teamNumber} eliminadas`);
            return true;
        }
        return false;
    }
    
    renderNotesPanel(teamNumber) {
        const notes = this.getTeamNotes(teamNumber);
        
        return `
            <div class="notes-panel" id="notes-panel-${teamNumber}">
                <div class="notes-header">
                    <h3>📝 Notas del Equipo #${teamNumber}</h3>
                    <button onclick="teamNotesManager.closeNotesPanel(${teamNumber})" class="btn-close">×</button>
                </div>
                
                <div class="notes-content">
                    <!-- Rating -->
                    <div class="rating-section">
                        <label>⭐ Calificación:</label>
                        <div class="star-rating">
                            ${[1,2,3,4,5].map(star => `
                                <span class="star ${notes.rating >= star ? 'active' : ''}" 
                                      onclick="teamNotesManager.setRating(${teamNumber}, ${star})">
                                    ${notes.rating >= star ? '★' : '☆'}
                                </span>
                            `).join('')}
                        </div>
                    </div>
                    
                    <!-- Text Notes -->
                    <div class="text-notes-section">
                        <label>📋 Observaciones:</label>
                        <textarea id="notes-text-${teamNumber}" 
                                  class="notes-textarea" 
                                  placeholder="Ej: Buen driver, pero autónomo falla 30%"
                                  onchange="teamNotesManager.saveText(${teamNumber})">${notes.text}</textarea>
                    </div>
                    
                    <!-- Tags -->
                    <div class="tags-section">
                        <label>🏷️ Tags:</label>
                        <div class="tags-container">
                            ${notes.tags.map(tag => `
                                <span class="tag">
                                    ${tag}
                                    <button onclick="teamNotesManager.removeTag(${teamNumber}, '${tag}')" class="tag-remove">×</button>
                                </span>
                            `).join('')}
                        </div>
                        <div class="tag-input-container">
                            <input type="text" 
                                   id="tag-input-${teamNumber}" 
                                   class="tag-input" 
                                   placeholder="Agregar tag..."
                                   onkeypress="if(event.key==='Enter') teamNotesManager.addTagFromInput(${teamNumber})">
                            <button onclick="teamNotesManager.addTagFromInput(${teamNumber})" class="btn-add-tag">+</button>
                        </div>
                        <div class="quick-tags">
                            ${['defensa', 'ataque', 'consistente', 'rápido', 'lento', 'confiable', 'rookie'].map(tag => `
                                <button onclick="teamNotesManager.addTag(${teamNumber}, '${tag}')" class="quick-tag">${tag}</button>
                            `).join('')}
                        </div>
                    </div>
                    
                    <!-- Metadata -->
                    ${notes.createdAt ? `
                        <div class="notes-metadata">
                            <small>Creado: ${new Date(notes.createdAt).toLocaleString('es-MX')}</small>
                            ${notes.updatedAt !== notes.createdAt ? `
                                <br><small>Actualizado: ${new Date(notes.updatedAt).toLocaleString('es-MX')}</small>
                            ` : ''}
                        </div>
                    ` : ''}
                </div>
                
                <div class="notes-footer">
                    <button onclick="teamNotesManager.exportTeamNotes(${teamNumber})" class="btn-export">
                        📤 Exportar
                    </button>
                    <button onclick="teamNotesManager.deleteTeamNotes(${teamNumber})" class="btn-delete">
                        🗑️ Borrar Todo
                    </button>
                </div>
            </div>
        `;
    }
    
    openNotesPanel(teamNumber) {
        // Check if panel already exists
        let panel = document.getElementById(`notes-panel-${teamNumber}`);
        if (panel) {
            panel.remove();
        }
        
        // Create panel
        const panelHTML = this.renderNotesPanel(teamNumber);
        const container = document.createElement('div');
        container.innerHTML = panelHTML;
        document.body.appendChild(container.firstElementChild);
        
        // Show with animation
        setTimeout(() => {
            document.getElementById(`notes-panel-${teamNumber}`).classList.add('show');
        }, 10);
    }
    
    closeNotesPanel(teamNumber) {
        const panel = document.getElementById(`notes-panel-${teamNumber}`);
        if (panel) {
            panel.classList.remove('show');
            setTimeout(() => panel.remove(), 300);
        }
    }
    
    saveText(teamNumber) {
        const textarea = document.getElementById(`notes-text-${teamNumber}`);
        if (textarea) {
            const notes = this.getTeamNotes(teamNumber);
            notes.text = textarea.value;
            this.saveTeamNote(teamNumber, notes);
        }
    }
    
    setRating(teamNumber, rating) {
        const notes = this.getTeamNotes(teamNumber);
        notes.rating = rating;
        this.saveTeamNote(teamNumber, notes);
        this.openNotesPanel(teamNumber); // Refresh UI
    }
    
    addTagFromInput(teamNumber) {
        const input = document.getElementById(`tag-input-${teamNumber}`);
        if (input && input.value.trim()) {
            this.addTag(teamNumber, input.value.trim());
            input.value = '';
            this.openNotesPanel(teamNumber); // Refresh UI
        }
    }
    
    exportTeamNotes(teamNumber) {
        const notes = this.getTeamNotes(teamNumber);
        const exportData = {
            team: teamNumber,
            ...notes
        };
        
        const dataStr = JSON.stringify(exportData, null, 2);
        const blob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `team_${teamNumber}_notes.json`;
        link.click();
    }
    
    getAllNotesCount() {
        return Object.keys(this.notes).length;
    }
    
    getTeamsWithNotes() {
        return Object.keys(this.notes).map(Number);
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
}

// Initialize global instance
const teamNotesManager = new TeamNotesManager();

// Create notes button for team profiles
function createNotesButton(teamNumber) {
    const btn = document.createElement('button');
    btn.className = 'notes-btn';
    btn.innerHTML = '📝';
    btn.title = 'Agregar notas';
    btn.onclick = () => teamNotesManager.openNotesPanel(teamNumber);
    
    const notes = teamNotesManager.getTeamNotes(teamNumber);
    if (notes.text || notes.tags.length > 0) {
        btn.classList.add('has-notes');
    }
    
    return btn;
}
