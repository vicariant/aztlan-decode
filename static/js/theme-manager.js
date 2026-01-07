/**
 * SISTEMA DE TEMAS VISUALES INMERSIVOS
 * Maneja fondos animados para cada módulo
 */

class ThemeManager {
    constructor() {
        this.currentPage = this.detectPage();
        this.isNightMode = this.isNightTime();
        this.init();
    }

    detectPage() {
        const path = window.location.pathname;
        if (path.includes('scouting')) return 'scouting';
        if (path.includes('astronomy')) return 'astronomy';
        if (path.includes('comparison')) return 'comparison';
        return null;
    }

    isNightTime() {
        const hour = new Date().getHours();
        return hour >= 19 || hour < 6; // 7PM - 6AM es noche
    }

    init() {
        if (!this.currentPage) return;

        document.body.setAttribute('data-page', this.currentPage);

        switch(this.currentPage) {
            case 'scouting':
                this.initArchaeologicalScene();
                break;
            case 'astronomy':
                this.initCosmicScene();
                break;
            case 'comparison':
                this.initBattlefieldScene();
                break;
        }

        this.createToggleButton();
    }

    // ==========================================
    // ESCENA ARQUEOLÓGICA (SCOUTING)
    // ==========================================
    initArchaeologicalScene() {
        const scene = document.createElement('div');
        scene.className = `archaeological-scene ${this.isNightMode ? 'night-mode' : 'day-mode'}`;
        
        scene.innerHTML = `
            <div class="sky"></div>
            
            <!-- Sol con rayos -->
            <div class="sun">
                <div class="sun-rays">
                    ${this.generateSunRays(12)}
                </div>
            </div>
            
            <!-- Luna con cráteres -->
            <div class="moon">
                <div class="crater" style="width: 15px; height: 15px; top: 25%; left: 30%;"></div>
                <div class="crater" style="width: 12px; height: 12px; top: 45%; left: 50%;"></div>
                <div class="crater" style="width: 10px; height: 10px; top: 60%; left: 35%;"></div>
                <div class="crater" style="width: 8px; height: 8px; top: 35%; left: 60%;"></div>
            </div>
            
            <!-- Estrellas (solo noche) -->
            <div class="stars">${this.generateStars(150)}</div>
            
            <!-- Nubes -->
            <div class="clouds">${this.generateClouds(6)}</div>
            
            <!-- Pajaros volando -->
            <div class="birds">${this.generateBirds(5)}</div>
            
            <!-- Dunas de arena con sombras -->
            <div class="dunes">
                <div class="dune dune-1">
                    <div class="dune-shadow"></div>
                </div>
                <div class="dune dune-2">
                    <div class="dune-shadow"></div>
                </div>
                <div class="dune dune-3">
                    <div class="dune-shadow"></div>
                </div>
            </div>
            
            <!-- Ruinas arqueológicas mejoradas -->
            <div class="ruins">
                <div class="pillar pillar-1">
                    <div class="pillar-top"></div>
                    <div class="pillar-cracks"></div>
                </div>
                <div class="pillar pillar-2">
                    <div class="pillar-top"></div>
                    <div class="pillar-cracks"></div>
                </div>
                <div class="pillar pillar-3">
                    <div class="pillar-top"></div>
                    <div class="pillar-cracks"></div>
                </div>
            </div>
            
            <!-- Palmeras con movimiento -->
            <div class="palm-tree palm-1">
                <div class="palm-trunk"></div>
                <div class="palm-leaves">
                    <div class="palm-leaf"></div>
                    <div class="palm-leaf"></div>
                    <div class="palm-leaf"></div>
                    <div class="palm-leaf"></div>
                    <div class="palm-leaf"></div>
                </div>
            </div>
            
            <div class="palm-tree palm-2">
                <div class="palm-trunk"></div>
                <div class="palm-leaves">
                    <div class="palm-leaf"></div>
                    <div class="palm-leaf"></div>
                    <div class="palm-leaf"></div>
                    <div class="palm-leaf"></div>
                    <div class="palm-leaf"></div>
                </div>
            </div>
            
            <!-- Tormenta de arena suave -->
            <div class="sandstorm">${this.generateSandParticles(40)}</div>
            
            <!-- Oasis con agua -->
            <div class="oasis">
                <div class="water-reflection"></div>
            </div>
        `;

        document.body.insertBefore(scene, document.body.firstChild);
    }

    generateStars(count) {
        let starsHTML = '';
        for (let i = 0; i < count; i++) {
            const x = Math.random() * 100;
            const y = Math.random() * 100;
            const delay = Math.random() * 3;
            const duration = 2 + Math.random() * 3;
            const size = Math.random() > 0.7 ? 'large' : (Math.random() > 0.5 ? 'medium' : 'small');
            
            starsHTML += `
                <div class="star star-${size}" style="
                    left: ${x}%;
                    top: ${y}%;
                    animation-delay: ${delay}s;
                    animation-duration: ${duration}s;
                "></div>
            `;
        }
        return starsHTML;
    }

    generateSunRays(count) {
        let raysHTML = '';
        for (let i = 0; i < count; i++) {
            const rotation = (360 / count) * i;
            raysHTML += `
                <div class="sun-ray" style="transform: rotate(${rotation}deg);"></div>
            `;
        }
        return raysHTML;
    }

    generateClouds(count) {
        let cloudsHTML = '';
        for (let i = 0; i < count; i++) {
            const y = 10 + Math.random() * 30;
            const delay = Math.random() * 20;
            const duration = 40 + Math.random() * 40;
            const scale = 0.6 + Math.random() * 0.8;
            
            cloudsHTML += `
                <div class="cloud" style="
                    top: ${y}%;
                    animation-delay: ${delay}s;
                    animation-duration: ${duration}s;
                    transform: scale(${scale});
                "></div>
            `;
        }
        return cloudsHTML;
    }

    generateBirds(count) {
        let birdsHTML = '';
        for (let i = 0; i < count; i++) {
            const y = 15 + Math.random() * 25;
            const delay = Math.random() * 15;
            const duration = 20 + Math.random() * 20;
            
            birdsHTML += `
                <div class="bird" style="
                    top: ${y}%;
                    animation-delay: ${delay}s;
                    animation-duration: ${duration}s;
                ">
                    <div class="bird-wing bird-wing-left"></div>
                    <div class="bird-wing bird-wing-right"></div>
                </div>
            `;
        }
        return birdsHTML;
    }
            
            starsHTML += `
                <div class="star" style="
                    left: ${x}%;
                    top: ${y}%;
                    animation-delay: ${delay}s;
                    animation-duration: ${duration}s;
                "></div>
            `;
        }
        return starsHTML;
    }

    generateSandParticles(count) {
        let particlesHTML = '';
        for (let i = 0; i < count; i++) {
            const size = 3 + Math.random() * 8;
            const x = Math.random() * 100;
            const y = Math.random() * 100;
            const delay = Math.random() * 15;
            const duration = 10 + Math.random() * 10;
            
            particlesHTML += `
                <div class="sand-particle" style="
                    width: ${size}px;
                    height: ${size}px;
                    left: ${x}%;
                    top: ${y}%;
                    animation-delay: ${delay}s;
                    animation-duration: ${duration}s;
                "></div>
            `;
        }
        return particlesHTML;
    }

    // ==========================================
    // ESCENA CÓSMICA (ASTRONOMY)
    // ==========================================
    initCosmicScene() {
        const scene = document.createElement('div');
        scene.className = `cosmic-scene ${this.isNightMode ? 'night-mode' : 'day-mode'}`;
        
        scene.innerHTML = `
            <!-- Sol (modo dia) con corona -->
            <div class="cosmic-sun">
                <div class="sun-corona"></div>
                <div class="sun-flares">${this.generateSolarFlares(8)}</div>
            </div>
            
            <!-- Luna llena con crateres detallados (modo noche) -->
            <div class="full-moon">
                <div class="crater" style="width: 40px; height: 40px; top: 25%; left: 30%;"></div>
                <div class="crater" style="width: 30px; height: 30px; top: 45%; left: 50%;"></div>
                <div class="crater" style="width: 25px; height: 25px; top: 60%; left: 35%;"></div>
                <div class="crater" style="width: 35px; height: 35px; top: 35%; left: 60%;"></div>
                <div class="crater" style="width: 20px; height: 20px; top: 70%; left: 55%;"></div>
                <div class="moon-glow"></div>
            </div>
            
            <!-- Estrellas del cosmos con distintos tamanos -->
            <div class="cosmic-stars">${this.generateCosmicStars(250)}</div>
            
            <!-- Estrellas fugaces -->
            <div class="shooting-stars">${this.generateShootingStars(4)}</div>
            
            <!-- Nebulosas multiples -->
            <div class="nebula nebula-purple"></div>
            <div class="nebula nebula-blue"></div>
            
            <!-- Galaxia espiral animada -->
            <div class="galaxy">
                <div class="galaxy-core"></div>
                <div class="galaxy-arms"></div>
            </div>
            
            <!-- Planetas en el fondo -->
            <div class="planet planet-1"></div>
            <div class="planet planet-2"></div>
            
            <!-- Cometas -->
            <div class="comet"></div>
            <div class="comet comet-2"></div>
        `;

        document.body.insertBefore(scene, document.body.firstChild);
    }
            
            <!-- Cometas -->
            <div class="comet" style="animation-delay: 0s;"></div>
            <div class="comet" style="animation-delay: 4s;"></div>
            <div class="comet" style="animation-delay: 7s;"></div>
        `;

        document.body.insertBefore(scene, document.body.firstChild);
    }

    generateCosmicStars(count) {
        let starsHTML = '';
        for (let i = 0; i < count; i++) {
            const x = Math.random() * 100;
            const y = Math.random() * 100;
            const delay = Math.random() * 4;
            const duration = 3 + Math.random() * 4;
            const size = Math.random();
            
            let sizeClass = 'small';
            if (size > 0.7) sizeClass = 'large';
            else if (size > 0.4) sizeClass = 'medium';
            
            starsHTML += `
                <div class="cosmic-star ${sizeClass}" style="
                    left: ${x}%;
                    top: ${y}%;
                    animation-delay: ${delay}s;
                    animation-duration: ${duration}s;
                "></div>
            `;
        }
        return starsHTML;
    }

    generateSolarFlares(count) {
        let flaresHTML = '';
        for (let i = 0; i < count; i++) {
            const rotation = (360 / count) * i;
            flaresHTML += `
                <div class="solar-flare" style="transform: rotate(${rotation}deg);"></div>
            `;
        }
        return flaresHTML;
    }

    generateShootingStars(count) {
        let starsHTML = '';
        for (let i = 0; i < count; i++) {
            const delay = Math.random() * 10;
            starsHTML += `
                <div class="shooting-star" style="animation-delay: ${delay}s;"></div>
            `;
        }
        return starsHTML;
    }
                    animation-duration: ${duration}s;
                "></div>
            `;
        }
        return starsHTML;
    }

    // ==========================================
    // ESCENA DE BATALLA (COMPARISON)
    // ==========================================
    initBattlefieldScene() {
        const scene = document.createElement('div');
        scene.className = `battlefield-scene ${this.isNightMode ? 'night-mode' : 'day-mode'}`;
        
        scene.innerHTML = `
            <!-- Sol brillante con rayos (modo día) -->
            <div class="bright-sun">
                <div class="sun-ray"></div>
                <div class="sun-ray"></div>
                <div class="sun-ray"></div>
                <div class="sun-ray"></div>
                <div class="sun-ray"></div>
                <div class="sun-ray"></div>
                <div class="sun-ray"></div>
                <div class="sun-ray"></div>
            </div>
            
            <!-- Luna de batalla (modo noche) -->
            <div class="battle-moon"></div>
            
            <!-- Estrellas (modo noche) -->
            <div class="battle-stars">${this.generateStars(100)}</div>
            
            <!-- Montañas -->
            <div class="battlefield-mountains">
                <div class="mountain"></div>
                <div class="mountain"></div>
                <div class="mountain"></div>
            </div>
            
            <!-- Banderas -->
            <div class="battle-flag" style="left: 15%; bottom: 45%;">
                <div class="flag-pole"></div>
                <div class="flag-cloth"></div>
            </div>
            <div class="battle-flag" style="right: 20%; bottom: 42%;">
                <div class="flag-pole"></div>
                <div class="flag-cloth"></div>
            </div>
            
            <!-- Nubes de polvo -->
            ${this.generateDustClouds(5)}
        `;

        document.body.insertBefore(scene, document.body.firstChild);
    }

    generateDustClouds(count) {
        let cloudsHTML = '';
        for (let i = 0; i < count; i++) {
            const x = Math.random() * 80 + 10;
            const size = 100 + Math.random() * 150;
            const delay = Math.random() * 10;
            const duration = 8 + Math.random() * 6;
            
            cloudsHTML += `
                <div class="dust-cloud" style="
                    left: ${x}%;
                    width: ${size}px;
                    height: ${size}px;
                    animation-delay: ${delay}s;
                    animation-duration: ${duration}s;
                "></div>
            `;
        }
        return cloudsHTML;
    }

    // ==========================================
    // BOTÓN DE CAMBIO DÍA/NOCHE
    // ==========================================
    createToggleButton() {
        const button = document.createElement('button');
        button.className = 'theme-toggle';
        button.innerHTML = `
            <span class="theme-toggle-icon">${this.isNightMode ? '●' : '○'}</span>
            <span class="theme-toggle-text">${this.isNightMode ? 'Modo Noche' : 'Modo Dia'}</span>
        `;

        button.addEventListener('click', () => {
            this.toggleDayNight();
        });

        document.body.appendChild(button);
    }

    toggleDayNight() {
        this.isNightMode = !this.isNightMode;
        
        // Actualizar escena según el módulo
        let scene;
        if (this.currentPage === 'scouting') {
            scene = document.querySelector('.archaeological-scene');
        } else if (this.currentPage === 'astronomy') {
            scene = document.querySelector('.cosmic-scene');
        } else if (this.currentPage === 'comparison') {
            scene = document.querySelector('.battlefield-scene');
        }
        
        if (scene) {
            // Agregar transición suave
            scene.style.transition = 'all 3s cubic-bezier(0.4, 0, 0.2, 1)';
            
            // Cambiar clases con delay para mejor efecto
            scene.classList.remove('day-mode', 'night-mode');
            
            setTimeout(() => {
                scene.classList.add(this.isNightMode ? 'night-mode' : 'day-mode');
            }, 50);
        }

        // Actualizar botón con animación
        const button = document.querySelector('.theme-toggle');
        if (button) {
            button.style.transform = 'scale(0.9)';
            button.style.transition = 'transform 0.2s ease';
            
            setTimeout(() => {
                button.innerHTML = `
                    <span class="theme-toggle-icon">${this.isNightMode ? '●' : '○'}</span>
                    <span class="theme-toggle-text">${this.isNightMode ? 'Modo Noche' : 'Modo Dia'}</span>
                `;
                button.style.transform = 'scale(1)';
            }, 150);
        }

        // Guardar preferencia
        localStorage.setItem('aztlan-night-mode', this.isNightMode);
    }
        } else if (this.currentPage === 'astronomy') {
            scene = document.querySelector('.cosmic-scene');
        } else if (this.currentPage === 'comparison') {
            scene = document.querySelector('.battlefield-scene');
        }
        
        if (scene) {
            scene.classList.remove('day-mode', 'night-mode');
            scene.classList.add(this.isNightMode ? 'night-mode' : 'day-mode');
        }

        // Actualizar boton
        const button = document.querySelector('.theme-toggle');
        if (button) {
            button.innerHTML = `
                <span class="theme-toggle-icon">${this.isNightMode ? '●' : '○'}</span>
                <span class="theme-toggle-text">${this.isNightMode ? 'Modo Noche' : 'Modo Dia'}</span>
            `;
        }

        // Guardar preferencia
        localStorage.setItem('aztlan-night-mode', this.isNightMode);
    }

    // Cargar preferencia guardada
    loadSavedPreference() {
        const saved = localStorage.getItem('aztlan-night-mode');
        if (saved !== null) {
            this.isNightMode = saved === 'true';
            // Actualizar la escena con la preferencia guardada
            let scene;
            if (this.currentPage === 'scouting') {
                scene = document.querySelector('.archaeological-scene');
            } else if (this.currentPage === 'astronomy') {
                scene = document.querySelector('.cosmic-scene');
            } else if (this.currentPage === 'comparison') {
                scene = document.querySelector('.battlefield-scene');
            }
            
            if (scene) {
                scene.classList.remove('day-mode', 'night-mode');
                scene.classList.add(this.isNightMode ? 'night-mode' : 'day-mode');
            }

            // Actualizar el boton
            const button = document.querySelector('.theme-toggle');
            if (button) {
                button.innerHTML = `
                    <span class="theme-toggle-icon">${this.isNightMode ? '●' : '○'}</span>
                    <span class="theme-toggle-text">${this.isNightMode ? 'Modo Noche' : 'Modo Dia'}</span>
                `;
            }
        }
    }
}

// Inicializar cuando el DOM esté listo (una sola vez)
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        const manager = new ThemeManager();
        manager.loadSavedPreference();
    });
} else {
    const manager = new ThemeManager();
    manager.loadSavedPreference();
}
