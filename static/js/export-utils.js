// ========================================
// EXPORT UTILITIES
// ========================================

class ExportManager {
    constructor() {
        this.formats = ['csv', 'json', 'txt'];
    }
    
    /**
     * Export team data to CSV
     */
    exportToCSV(data, filename = 'aztlan_export') {
        let csv = '';
        
        if (Array.isArray(data) && data.length > 0) {
            // Get headers from first object
            const headers = Object.keys(data[0]);
            csv += headers.join(',') + '\n';
            
            // Add data rows
            data.forEach(row => {
                const values = headers.map(header => {
                    const value = row[header];
                    // Escape quotes and wrap in quotes if contains comma
                    if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
                        return `"${value.replace(/"/g, '""')}"`;
                    }
                    return value;
                });
                csv += values.join(',') + '\n';
            });
        } else if (typeof data === 'object') {
            // Single object - convert to key-value pairs
            csv = 'Campo,Valor\n';
            Object.entries(data).forEach(([key, value]) => {
                csv += `"${key}","${value}"\n`;
            });
        }
        
        this.downloadFile(csv, `${filename}.csv`, 'text/csv');
    }
    
    /**
     * Export data to JSON
     */
    exportToJSON(data, filename = 'aztlan_export') {
        const jsonStr = JSON.stringify(data, null, 2);
        this.downloadFile(jsonStr, `${filename}.json`, 'application/json');
    }
    
    /**
     * Export data to formatted text
     */
    exportToTXT(data, filename = 'aztlan_export') {
        let txt = '═══════════════════════════════════\n';
        txt += '    AZTLÁN DECODE - REPORTE\n';
        txt += `    ${new Date().toLocaleString('es-MX')}\n`;
        txt += '═══════════════════════════════════\n\n';
        
        if (Array.isArray(data)) {
            data.forEach((item, index) => {
                txt += `[${index + 1}] ─────────────────\n`;
                Object.entries(item).forEach(([key, value]) => {
                    txt += `  ${key}: ${value}\n`;
                });
                txt += '\n';
            });
        } else if (typeof data === 'object') {
            Object.entries(data).forEach(([key, value]) => {
                txt += `${key}: ${value}\n`;
            });
        }
        
        this.downloadFile(txt, `${filename}.txt`, 'text/plain');
    }
    
    /**
     * Export team comparison
     */
    exportComparison(team1Data, team2Data) {
        const comparisonData = {
            exportDate: new Date().toISOString(),
            team1: team1Data,
            team2: team2Data,
            comparison: {
                oprDifference: team1Data.opr - team2Data.opr,
                winRateDifference: team1Data.winRate - team2Data.winRate,
                winner: team1Data.opr > team2Data.opr ? team1Data.number : team2Data.number
            }
        };
        
        this.exportToJSON(comparisonData, `comparison_${team1Data.number}_vs_${team2Data.number}`);
    }
    
    /**
     * Export planet analysis
     */
    exportPlanetAnalysis(planetData) {
        const filename = `planet_${planetData.name || 'analysis'}`.replace(/\s+/g, '_');
        this.exportToJSON(planetData, filename);
    }
    
    /**
     * Export regional predictions
     */
    exportRegionalPrediction(regionalData) {
        const filename = `regional_${regionalData.eventName || 'prediction'}`.replace(/\s+/g, '_');
        
        // Create detailed CSV
        const csvData = [];
        
        // Rankings
        regionalData.ranking.forEach(team => {
            csvData.push({
                Rank: team.rank,
                'Número': team.number,
                Nombre: team.name,
                OPR: team.opr,
                'RP Predicho': team.predictedRP,
                'Récord Predicho': team.predictedRecord
            });
        });
        
        this.exportToCSV(csvData, filename);
    }
    
    /**
     * Generic download function
     */
    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.click();
        URL.revokeObjectURL(url);
        
        // Show notification
        this.showNotification(`📥 Descargado: ${filename}`);
    }
    
    /**
     * Create export button with dropdown
     */
    createExportButton(data, baseFilename = 'aztlan_export') {
        const container = document.createElement('div');
        container.className = 'export-dropdown';
        
        container.innerHTML = `
            <button class="btn-export-main" onclick="this.parentElement.classList.toggle('open')">
                📤 Exportar
                <span class="dropdown-arrow">▼</span>
            </button>
            <div class="export-options">
                <button onclick="exportManager.exportToCSV(${JSON.stringify(data)}, '${baseFilename}')">
                    📊 Exportar como CSV
                </button>
                <button onclick="exportManager.exportToJSON(${JSON.stringify(data)}, '${baseFilename}')">
                    📋 Exportar como JSON
                </button>
                <button onclick="exportManager.exportToTXT(${JSON.stringify(data)}, '${baseFilename}')">
                    📄 Exportar como TXT
                </button>
            </div>
        `;
        
        return container;
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
const exportManager = new ExportManager();

// ========================================
// MULTIPLE COMPARISON UTILITIES
// ========================================

class MultipleComparisonManager {
    constructor() {
        this.teams = [];
        this.maxTeams = 6;
    }
    
    addTeam(teamData) {
        if (this.teams.length >= this.maxTeams) {
            alert(`Máximo ${this.maxTeams} equipos para comparación`);
            return false;
        }
        
        // Check if already added
        if (this.teams.some(t => t.number === teamData.number)) {
            alert(`Equipo ${teamData.number} ya está en la comparación`);
            return false;
        }
        
        this.teams.push(teamData);
        this.renderComparison();
        return true;
    }
    
    removeTeam(teamNumber) {
        this.teams = this.teams.filter(t => t.number !== teamNumber);
        this.renderComparison();
    }
    
    clearAll() {
        this.teams = [];
        this.renderComparison();
    }
    
    renderComparison() {
        const container = document.getElementById('multiple-comparison-container');
        if (!container) return;
        
        if (this.teams.length === 0) {
            container.innerHTML = `
                <div class="empty-comparison">
                    <p>🤖 Agrega equipos para comparar</p>
                    <small>Hasta ${this.maxTeams} equipos</small>
                </div>
            `;
            return;
        }
        
        // Create comparison table
        const metrics = ['OPR', 'Win Rate', 'Awards', 'RP', 'Worlds'];
        
        let html = `
            <div class="comparison-header">
                <h3>⚔️ Comparando ${this.teams.length} Equipos</h3>
                <div class="comparison-actions">
                    <button onclick="multiCompare.exportComparison()" class="btn-mini">📤</button>
                    <button onclick="multiCompare.clearAll()" class="btn-mini">🗑️</button>
                </div>
            </div>
            
            <div class="comparison-table-container">
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>Métrica</th>
                            ${this.teams.map(team => `
                                <th>
                                    #${team.number}
                                    <button onclick="multiCompare.removeTeam(${team.number})" class="btn-remove-small">×</button>
                                </th>
                            `).join('')}
                        </tr>
                    </thead>
                    <tbody>
                        ${metrics.map(metric => `
                            <tr>
                                <td class="metric-name">${metric}</td>
                                ${this.teams.map(team => `
                                    <td class="metric-value ${this.getBestClass(metric, team)}">
                                        ${this.getMetricValue(team, metric)}
                                    </td>
                                `).join('')}
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
            
            <div class="comparison-chart">
                <canvas id="multi-comparison-chart"></canvas>
            </div>
        `;
        
        container.innerHTML = html;
        this.renderChart();
    }
    
    getMetricValue(team, metric) {
        switch(metric) {
            case 'OPR': return team.opr || 0;
            case 'Win Rate': return `${team.winRate || 0}%`;
            case 'Awards': return team.awards || 0;
            case 'RP': return team.rp || 0;
            case 'Worlds': return team.worldsQualified ? '✅' : '❌';
            default: return '-';
        }
    }
    
    getBestClass(metric, team) {
        if (metric === 'Worlds') return '';
        
        const values = this.teams.map(t => {
            const val = this.getMetricValue(t, metric);
            return typeof val === 'string' ? parseFloat(val) : val;
        });
        
        const teamValue = parseFloat(this.getMetricValue(team, metric));
        const maxValue = Math.max(...values);
        
        return teamValue === maxValue ? 'best-value' : '';
    }
    
    renderChart() {
        const canvas = document.getElementById('multi-comparison-chart');
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: this.teams.map(t => `#${t.number}`),
                datasets: [{
                    label: 'OPR',
                    data: this.teams.map(t => t.opr || 0),
                    backgroundColor: 'rgba(0, 168, 107, 0.7)',
                    borderColor: 'rgba(0, 168, 107, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        ticks: { color: '#fff' }
                    },
                    x: {
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        ticks: { color: '#fff' }
                    }
                }
            }
        });
    }
    
    exportComparison() {
        const exportData = this.teams.map(team => ({
            Número: team.number,
            Nombre: team.name,
            OPR: team.opr,
            'Win Rate': team.winRate,
            Awards: team.awards,
            RP: team.rp,
            'Worlds Qualified': team.worldsQualified ? 'Yes' : 'No'
        }));
        
        exportManager.exportToCSV(exportData, `comparison_${this.teams.length}_teams`);
    }
}

// Initialize global instance
const multiCompare = new MultipleComparisonManager();
