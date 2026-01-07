// ========================================
// DASHBOARD EJECUTIVO
// ========================================
// Gamificación y estadísticas de uso

class DashboardManager {
    constructor() {
        this.storageKey = 'aztlan_dashboard_stats';
        this.stats = this.loadStats();
    }
    
    loadStats() {
        const stored = localStorage.getItem(this.storageKey);
        return stored ? JSON.parse(stored) : {
            teamsAnalyzed: 0,
            planetsAnalyzed: 0,
            comparisonsMade: 0,
            predictionsCorrect: 0,
            predictionsFailed: 0,
            matchesSimulated: 0,
            regionalsAnalyzed: 0,
            totalSearches: 0,
            firstVisit: new Date().toISOString(),
            lastVisit: new Date().toISOString(),
            achievements: []
        };
    }
    
    saveStats() {
        this.stats.lastVisit = new Date().toISOString();
        localStorage.setItem(this.storageKey, JSON.stringify(this.stats));
    }
    
    trackEvent(eventType, data = {}) {
        switch(eventType) {
            case 'team_analyzed':
                this.stats.teamsAnalyzed++;
                this.checkAchievement('teams_10', this.stats.teamsAnalyzed >= 10, '🤖 Scout Novato', 'Analiza 10 equipos');
                this.checkAchievement('teams_50', this.stats.teamsAnalyzed >= 50, '🏆 Scout Experto', 'Analiza 50 equipos');
                this.checkAchievement('teams_100', this.stats.teamsAnalyzed >= 100, '⭐ Scout Maestro', 'Analiza 100 equipos');
                break;
            
            case 'planet_analyzed':
                this.stats.planetsAnalyzed++;
                this.checkAchievement('planets_5', this.stats.planetsAnalyzed >= 5, '🪐 Astrónomo Aprendiz', 'Analiza 5 planetas');
                this.checkAchievement('planets_25', this.stats.planetsAnalyzed >= 25, '🌌 Astrónomo Experto', 'Analiza 25 planetas');
                break;
            
            case 'comparison_made':
                this.stats.comparisonsMade++;
                this.checkAchievement('comparisons_10', this.stats.comparisonsMade >= 10, '⚔️ Estratega', 'Realiza 10 comparaciones');
                break;
            
            case 'prediction_result':
                if (data.correct) {
                    this.stats.predictionsCorrect++;
                } else {
                    this.stats.predictionsFailed++;
                }
                const accuracy = this.getPredictionAccuracy();
                this.checkAchievement('accuracy_80', accuracy >= 80, '🎯 Predictor Preciso', '80% de precisión');
                this.checkAchievement('accuracy_90', accuracy >= 90, '🔮 Oráculo Perfecto', '90% de precisión');
                break;
            
            case 'match_simulated':
                this.stats.matchesSimulated++;
                this.checkAchievement('matches_20', this.stats.matchesSimulated >= 20, '🎲 Simulador Pro', 'Simula 20 matches');
                break;
            
            case 'regional_analyzed':
                this.stats.regionalsAnalyzed++;
                this.checkAchievement('regionals_5', this.stats.regionalsAnalyzed >= 5, '🏆 Analista Regional', 'Analiza 5 regionales');
                break;
            
            case 'search':
                this.stats.totalSearches++;
                break;
        }
        
        this.saveStats();
    }
    
    checkAchievement(id, condition, name, description) {
        if (condition && !this.hasAchievement(id)) {
            this.stats.achievements.push({
                id: id,
                name: name,
                description: description,
                unlockedAt: new Date().toISOString()
            });
            this.showAchievementNotification(name, description);
        }
    }
    
    hasAchievement(id) {
        return this.stats.achievements.some(a => a.id === id);
    }
    
    getPredictionAccuracy() {
        const total = this.stats.predictionsCorrect + this.stats.predictionsFailed;
        if (total === 0) return 0;
        return Math.round((this.stats.predictionsCorrect / total) * 100);
    }
    
    getDaysActive() {
        const first = new Date(this.stats.firstVisit);
        const last = new Date(this.stats.lastVisit);
        return Math.floor((last - first) / (1000 * 60 * 60 * 24)) + 1;
    }
    
    getLevel() {
        const totalActions = this.stats.teamsAnalyzed + 
                            this.stats.planetsAnalyzed + 
                            this.stats.comparisonsMade + 
                            this.stats.matchesSimulated + 
                            this.stats.regionalsAnalyzed;
        
        if (totalActions >= 200) return { level: 5, name: '⚡ LEYENDA AZTLÁN', next: null };
        if (totalActions >= 100) return { level: 4, name: '🌟 MAESTRO', next: 200 };
        if (totalActions >= 50) return { level: 3, name: '🏆 EXPERTO', next: 100 };
        if (totalActions >= 20) return { level: 2, name: '🎖️ AVANZADO', next: 50 };
        return { level: 1, name: '🌱 INICIANTE', next: 20 };
    }
    
    renderDashboard() {
        const level = this.getLevel();
        const accuracy = this.getPredictionAccuracy();
        const daysActive = this.getDaysActive();
        
        const totalActions = this.stats.teamsAnalyzed + 
                            this.stats.planetsAnalyzed + 
                            this.stats.comparisonsMade + 
                            this.stats.matchesSimulated + 
                            this.stats.regionalsAnalyzed;
        
        const progressToNext = level.next ? 
            Math.min(100, Math.round((totalActions / level.next) * 100)) : 100;
        
        return `
            <div class="dashboard-container">
                <div class="dashboard-header">
                    <h2>📊 Tu Dashboard AZTLÁN</h2>
                    <div class="dashboard-level">
                        <div class="level-badge">${level.name}</div>
                        ${level.next ? `
                            <div class="level-progress">
                                <div class="progress-bar" style="width: ${progressToNext}%"></div>
                                <span class="progress-text">${totalActions}/${level.next}</span>
                            </div>
                        ` : '<div class="max-level">✨ NIVEL MÁXIMO</div>'}
                    </div>
                </div>
                
                <div class="dashboard-stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon">🤖</div>
                        <div class="stat-value">${this.stats.teamsAnalyzed}</div>
                        <div class="stat-label">Equipos Analizados</div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="stat-icon">🪐</div>
                        <div class="stat-value">${this.stats.planetsAnalyzed}</div>
                        <div class="stat-label">Planetas Descubiertos</div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="stat-icon">⚔️</div>
                        <div class="stat-value">${this.stats.comparisonsMade}</div>
                        <div class="stat-label">Comparaciones</div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="stat-icon">🎯</div>
                        <div class="stat-value">${accuracy}%</div>
                        <div class="stat-label">Precisión Predicciones</div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="stat-icon">🎲</div>
                        <div class="stat-value">${this.stats.matchesSimulated}</div>
                        <div class="stat-label">Matches Simulados</div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="stat-icon">🏆</div>
                        <div class="stat-value">${this.stats.regionalsAnalyzed}</div>
                        <div class="stat-label">Regionales Analizados</div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="stat-icon">📅</div>
                        <div class="stat-value">${daysActive}</div>
                        <div class="stat-label">Días Activo</div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="stat-icon">🔍</div>
                        <div class="stat-value">${this.stats.totalSearches}</div>
                        <div class="stat-label">Búsquedas Totales</div>
                    </div>
                </div>
                
                ${this.renderAchievements()}
                
                <div class="dashboard-footer">
                    <button onclick="dashboardManager.exportDashboard()" class="btn-export">
                        📤 Exportar Estadísticas
                    </button>
                    <button onclick="dashboardManager.resetStats()" class="btn-reset">
                        🔄 Reiniciar Stats
                    </button>
                </div>
            </div>
        `;
    }
    
    renderAchievements() {
        if (this.stats.achievements.length === 0) {
            return `
                <div class="achievements-section">
                    <h3>🏅 Logros</h3>
                    <div class="empty-achievements">
                        <p>Aún no tienes logros desbloqueados</p>
                        <small>¡Explora el sistema para desbloquearlos!</small>
                    </div>
                </div>
            `;
        }
        
        const sorted = [...this.stats.achievements].sort((a, b) => 
            new Date(b.unlockedAt) - new Date(a.unlockedAt)
        );
        
        return `
            <div class="achievements-section">
                <h3>🏅 Logros Desbloqueados (${this.stats.achievements.length})</h3>
                <div class="achievements-grid">
                    ${sorted.map(achievement => `
                        <div class="achievement-card">
                            <div class="achievement-name">${achievement.name}</div>
                            <div class="achievement-desc">${achievement.description}</div>
                            <div class="achievement-date">
                                ${new Date(achievement.unlockedAt).toLocaleDateString('es-MX')}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    showAchievementNotification(name, description) {
        const notification = document.createElement('div');
        notification.className = 'achievement-notification';
        notification.innerHTML = `
            <div class="achievement-content">
                <div class="achievement-icon">🏆</div>
                <div class="achievement-text">
                    <div class="achievement-title">¡LOGRO DESBLOQUEADO!</div>
                    <div class="achievement-name">${name}</div>
                    <div class="achievement-description">${description}</div>
                </div>
            </div>
        `;
        document.body.appendChild(notification);
        
        setTimeout(() => notification.classList.add('show'), 10);
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 500);
        }, 5000);
    }
    
    exportDashboard() {
        const exportData = {
            ...this.stats,
            level: this.getLevel(),
            accuracy: this.getPredictionAccuracy(),
            daysActive: this.getDaysActive(),
            exportedAt: new Date().toISOString()
        };
        
        const dataStr = JSON.stringify(exportData, null, 2);
        const blob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'aztlan_dashboard_stats.json';
        link.click();
    }
    
    resetStats() {
        if (confirm('¿Estás seguro de reiniciar todas las estadísticas? Esta acción no se puede deshacer.')) {
            localStorage.removeItem(this.storageKey);
            this.stats = this.loadStats();
            window.location.reload();
        }
    }
}

// Initialize global instance
const dashboardManager = new DashboardManager();
