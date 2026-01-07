#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AZTLÁN DECODE - GENERADOR DE ANÁLISIS IA AVANZADO
Sistema de generación de texto con templates mejorados y análisis profundo
"""

import random
from datetime import datetime

class TextAnalyzer:
    """Generador ULTRA AVANZADO de análisis en texto natural"""
    
    def __init__(self):
        """Inicializa el analizador de texto con templates mejorados"""
        self.templates_team_analysis = [
            "🔬 **ANÁLISIS ESTRATÉGICO AVANZADO**\n\n{team_name} (#{team_number}) presenta {performance_level} con una puntuación global de **{score}/100**\n\n{momentum_section}**📊 MÉTRICAS CLAVE:**\n{metrics}\n\n**⚡ FORTALEZAS IDENTIFICADAS:**\n{strengths}\n\n{outliers_section}{weaknesses_section}**🔮 PREDICCIÓN AVANZADA:**\n{prediction}\n\n**🎯 ESTRATEGIA PERSONALIZADA:**\n{strategy}\n\n{alliance_section}**💡 ANÁLISIS FINAL:** {final_insight}",
            
            "⚔️ **REPORTE TÁCTICO COMPLETO**\n\n🏆 {team_name} - Equipo #{team_number}\n📈 Score Global: **{score}/100** | {category} {emoji}\n\n{momentum_section}**🎯 PERFIL DE RENDIMIENTO:**\n{performance_desc}\n\n**📊 ESTADÍSTICAS DETALLADAS:**\n{stats}\n\n**💎 VENTAJAS COMPETITIVAS:**\n{advantages}\n\n{strategic_adv_section}{weaknesses_section}**🔮 PROYECCIÓN FUTURA:**\n{forecast}\n\n**🎖️ PLAN DE ACCIÓN:**\n{tactics}\n\n{alliance_section}**⚡ CONCLUSIÓN:** {final_insight}",
            
            "🧠 **ANÁLISIS IA PROFUNDO**\n\n═══════════════════════════════\n🤖 {team_name} (#{team_number})\n═══════════════════════════════\n\n**SCORE ACTUAL:** {score}/100 - {category}\n**SCORE FUTURO:** {future_score}/100 {trend_indicator}\n\n{momentum_section}**📈 MÉTRICAS DE RENDIMIENTO:**\n{detailed_metrics}\n\n**🌟 PUNTOS FUERTES:**\n{strengths}\n\n{strategic_adv_section}{outliers_section}{weaknesses_section}**🎲 PREDICCIONES:**\n{detailed_prediction}\n\n**🎯 RECOMENDACIONES ESTRATÉGICAS:**\n{strategy}\n\n{alliance_section}═══════════════════════════════\n**🏆 VEREDICTO FINAL:** {final_insight}\n═══════════════════════════════",
        ]
        
        self.templates_comparison = [
            "⚔️ **ANÁLISIS COMPARATIVO AVANZADO**\n\n**{team1_name} (#{team1_num})**\n{team1_desc}\n\n**VS**\n\n**{team2_name} (#{team2_num})**\n{team2_desc}\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n**📊 ANÁLISIS DE DIFERENCIAS:**\n{differences}\n\n**🎯 PREDICCIÓN DE MATCH:**\n{prediction_detailed}\n\n**⚡ VENTAJAS ESTRATÉGICAS:**\n{strategic_comparison}\n\n**🏆 VEREDICTO FINAL:**\n{verdict}\n\n**💡 RECOMENDACIÓN TÁCTICA:**\n{strategy}\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n**🎲 NIVEL DE CONFIANZA:** {confidence}",
            
            "🥊 **CONFRONTACIÓN TÁCTICA DETALLADA**\n\n═══════════════════════════════\n\n**EQUIPO 1: {team1_name}**\n• Score: {team1_score}/100 ({team1_category})\n• Momentum: {team1_momentum}\n• Win Probability: **{team1_prob}%**\n\n{team1_strengths}\n\n**VS**\n\n**EQUIPO 2: {team2_name}**\n• Score: {team2_score}/100 ({team2_category})\n• Momentum: {team2_momentum}\n• Win Probability: **{team2_prob}%**\n\n{team2_strengths}\n\n═══════════════════════════════\n\n**⚖️ BALANCE DE PODER:**\n{balance}\n\n**🎯 ANÁLISIS PREDICTIVO:**\n{prediction}\n\n**🔬 FACTORES CRÍTICOS:**\n{critical_factors}\n\n**📌 RECOMENDACIÓN:**\n{recommendation}\n\n═══════════════════════════════\n**🎲 CONFIANZA:** {confidence}%\n═══════════════════════════════",
        ]
    
    def generate_team_analysis(self, team_data, analysis_result):
        """
        Genera análisis ULTRA DETALLADO en texto natural
        
        Args:
            team_data: Datos del equipo
            analysis_result: Resultado del análisis FTC AVANZADO
            
        Returns:
            str: Análisis SÚPER completo en texto natural
        """
        try:
            template = random.choice(self.templates_team_analysis)
            
            # Datos básicos
            team_name = team_data.get('name', 'Equipo Desconocido')
            team_number = team_data.get('team', 'N/A')
            category = analysis_result.get('category', 'SIN CLASIFICAR')
            emoji = analysis_result.get('category_emoji', '📊')
            global_score = analysis_result.get('global_score', 0)
            future_score = analysis_result.get('future_score', global_score)
            
            # MOMENTUM (nuevo)
            momentum = analysis_result.get('momentum', 0)
            momentum_desc = analysis_result.get('momentum_desc', 'ESTABLE')
            momentum_section = f"**🔥 MOMENTUM:** {momentum_desc}\n**📈 Tendencia:** Score proyectado {future_score:.1f}/100\n\n"
            
            # Indicador de tendencia
            if future_score > global_score + 2:
                trend_indicator = "📈 (Mejorando)"
            elif future_score < global_score - 2:
                trend_indicator = "📉 (Declive)"
            else:
                trend_indicator = "➡️ (Estable)"
            
            # Métricas DETALLADAS
            metrics = analysis_result.get('metrics', {})
            metrics_list = []
            metrics_list.append(f"• **Ranking Points:** {metrics.get('ranking_points', 0):.0f} RP")
            metrics_list.append(f"• **Win Rate:** {metrics.get('win_rate', 0):.1%}")
            metrics_list.append(f"• **Consistencia:** {metrics.get('consistency', 0):.1%}")
            metrics_list.append(f"• **OPR Máximo:** {metrics.get('peak_performance', 0):.1f} pts")
            metrics_list.append(f"• **Factor Momentum:** {momentum:+.2f}")
            
            # Métricas MÁS detalladas
            detailed_metrics = '\n'.join(metrics_list)
            wins = team_data.get('wins', 0)
            losses = team_data.get('losses', 0)
            detailed_metrics += f"\n• **Récord:** {wins}W - {losses}L"
            if team_data.get('worlds_qualified'):
                detailed_metrics += "\n• **🌍 CLASIFICADO A WORLDS**"
            
            # Fortalezas
            strengths = analysis_result.get('strengths', [])
            strengths_text = '\n'.join([f"• {s}" for s in strengths])
            
            # OUTLIERS/Anomalías (nuevo)
            outliers = analysis_result.get('outliers', [])
            outliers_section = ""
            if outliers:
                outliers_text = '\n'.join([f"• {o['desc']}" for o in outliers])
                outliers_section = f"**🌟 DESTACADOS EXCEPCIONALES:**\n{outliers_text}\n\n"
            
            # VENTAJAS ESTRATÉGICAS (nuevo)
            strategic_adv = analysis_result.get('strategic_advantages', [])
            strategic_adv_section = ""
            if strategic_adv:
                strat_text = '\n'.join([f"• {adv['desc']} (Impacto: {adv['impact']})" for adv in strategic_adv])
                strategic_adv_section = f"**⚔️ VENTAJAS ESTRATÉGICAS:**\n{strat_text}\n\n"
            
            # Debilidades
            weaknesses = analysis_result.get('weaknesses', [])
            weaknesses_section = ""
            if weaknesses and weaknesses != ["📊 Rendimiento estándar"]:
                weaknesses_text = '\n'.join([f"• {w}" for w in weaknesses])
                weaknesses_section = f"**⚠️ ÁREAS DE MEJORA:**\n{weaknesses_text}\n\n"
            
            # Predicción AVANZADA
            prediction = analysis_result.get('prediction', {})
            pred_text = f"• **Outlook:** {prediction.get('outlook', 'N/A')}\n"
            pred_text += f"• **Prob. Worlds:** {prediction.get('probability_worlds', 0):.1f}%\n"
            pred_text += f"• **Prob. Victoria Regional:** {prediction.get('probability_regional_win', 0):.1f}%\n"
            pred_text += f"• **Impacto Momentum:** {prediction.get('momentum_impact', 0):+.2f}\n"
            pred_text += f"• **Rating Consistencia:** {prediction.get('consistency_rating', 'N/A')}"
            
            detailed_prediction = pred_text + f"\n• **Recomendación:** {prediction.get('recommendation', 'N/A')}"
            
            # Estrategia MEJORADA
            strategy_items = analysis_result.get('strategy', [])
            if isinstance(strategy_items, list) and len(strategy_items) > 0 and isinstance(strategy_items[0], dict):
                # Nueva estrategia con prioridades
                strategy_by_priority = {}
                for item in strategy_items:
                    priority = item.get('priority', 2)
                    if priority not in strategy_by_priority:
                        strategy_by_priority[priority] = []
                    strategy_by_priority[priority].append(f"• {item['action']}")
                
                strategy_text = ""
                for priority in sorted(strategy_by_priority.keys()):
                    priority_name = "🔴 CRÍTICO" if priority == 1 else "🟡 IMPORTANTE" if priority == 2 else "🟢 OPCIONAL"
                    strategy_text += f"\n**{priority_name}:**\n" + '\n'.join(strategy_by_priority[priority]) + "\n"
            else:
                strategy_text = '\n'.join([f"• {s}" for s in strategy_items])
            
            # ALIANZAS (nuevo)
            alliance_recs = analysis_result.get('alliance_recommendations', [])
            alliance_section = ""
            if alliance_recs:
                alliance_text = '\n'.join([f"• **{rec['type']}:** {rec['desc']}\n  {rec['picks']}" for rec in alliance_recs])
                alliance_section = f"**🤝 RECOMENDACIONES DE ALIANZA:**\n{alliance_text}\n\n"
            
            # Nivel de desempeño
            if global_score >= 90:
                performance_level = "un rendimiento **LEGENDARIO** 👑"
            elif global_score >= 85:
                performance_level = "un rendimiento **EXCEPCIONAL** 💎"
            elif global_score >= 75:
                performance_level = "un **EXCELENTE** desempeño 🔥"
            elif global_score >= 65:
                performance_level = "un desempeño **MUY BUENO** ⚡"
            elif global_score >= 50:
                performance_level = "un rendimiento **SÓLIDO** ✅"
            else:
                performance_level = "un rendimiento **EN DESARROLLO** 🌱"
            
            # Descripción de rendimiento
            performance_desc = f"Con un récord de {wins}W-{losses}L, este equipo ha demostrado {self._get_performance_adjective(wins, losses)}."
            
            # Insight final
            final_insight = self._generate_final_insight(global_score, momentum, len(strategic_adv))
            
            # Formatear template
            result = template.format(
                team_name=team_name,
                team_number=team_number,
                performance_level=performance_level,
                score=global_score,
                future_score=future_score,
                trend_indicator=trend_indicator,
                category=category,
                emoji=emoji,
                momentum_section=momentum_section,
                rp=metrics.get('ranking_points', 0),
                metrics='\n'.join(metrics_list),
                detailed_metrics=detailed_metrics,
                strengths=strengths_text,
                outliers_section=outliers_section,
                strategic_adv_section=strategic_adv_section,
                weaknesses_section=weaknesses_section,
                prediction=pred_text,
                detailed_prediction=detailed_prediction,
                strategy=strategy_text,
                performance_desc=performance_desc,
                stats='\n'.join(metrics_list),
                advantages=strengths_text,
                challenges_section=weaknesses_section,
                forecast=pred_text,
                tactics=strategy_text,
                alliance_section=alliance_section,
                final_insight=final_insight
            )
            
            return result
            
        except Exception as e:
            return f"Error generando análisis: {str(e)}"
    
    def _generate_final_insight(self, score, momentum, num_advantages):
        """Genera insight final inteligente"""
        if score >= 90:
            return "Este equipo es una **FUERZA DOMINANTE** en su región. Material de campeón mundial."
        elif score >= 85:
            return "**ÉLITE COMPETITIVO** con alto potencial para Worlds. Candidato serio para playoffs."
        elif score >= 75:
            return "**SÓLIDO CONTENDIENTE** con capacidades probadas. Bien posicionado para éxito regional."
        elif score >= 65:
            return "**COMPETIDOR CONFIABLE** con margen de crecimiento. Enfoque en optimización."
        elif score >= 50:
            return "**EN RANGO COMPETITIVO**. Con mejoras focalizadas puede alcanzar nivel superior."
        else:
            return "**FASE DE DESARROLLO**. Enfoque en fundamentos para construir base sólida."
    
    def generate_comparison(self, team1_data, team2_data, comparison_result):
        """
        Genera comparación en texto natural
        
        Args:
            team1_data: Datos equipo 1
            team2_data: Datos equipo 2
            comparison_result: Resultado de comparación
            
        Returns:
            str: Comparación en texto natural
        """
        try:
            template = random.choice(self.templates_comparison)
            
            # Datos equipos
            team1_name = team1_data.get('name', f"Equipo {team1_data.get('team', '?')}")
            team2_name = team2_data.get('name', f"Equipo {team2_data.get('team', '?')}")
            team1_num = team1_data.get('team', 'N/A')
            team2_num = team2_data.get('team', 'N/A')
            
            # Análisis
            team1 = comparison_result.get('team1', {})
            team2 = comparison_result.get('team2', {})
            
            # Descripciones
            team1_desc = f"**Puntuación Global:** {team1.get('score', 0):.1f}/100\n"
            team1_desc += f"**Categoría:** {team1.get('category', 'N/A')}\n"
            team1_desc += f"**Probabilidad de Victoria:** {team1.get('win_probability', 50):.0f}%"
            
            team2_desc = f"**Puntuación Global:** {team2.get('score', 0):.1f}/100\n"
            team2_desc += f"**Categoría:** {team2.get('category', 'N/A')}\n"
            team2_desc += f"**Probabilidad de Victoria:** {team2.get('win_probability', 50):.0f}%"
            
            # Ventajas
            adv1 = team1.get('advantages', [])
            adv2 = team2.get('advantages', [])
            
            team1_strengths = "**Ventajas:**\n" + '\n'.join([f"✓ {a}" for a in adv1]) if adv1 else "Sin ventajas claras identificadas"
            team2_strengths = "**Ventajas:**\n" + '\n'.join([f"✓ {a}" for a in adv2]) if adv2 else "Sin ventajas claras identificadas"
            
            # Diferencias
            differences = []
            score_diff = abs(team1.get('score', 0) - team2.get('score', 0))
            if score_diff > 10:
                differences.append(f"• **Diferencia significativa:** {score_diff:.1f} puntos")
            elif score_diff > 5:
                differences.append(f"• **Diferencia moderada:** {score_diff:.1f} puntos")
            else:
                differences.append(f"• **Match muy parejo:** Solo {score_diff:.1f} puntos de diferencia")
            
            if adv1:
                differences.append(f"• **{team1_name}** tiene {len(adv1)} ventaja(s) identificada(s)")
            if adv2:
                differences.append(f"• **{team2_name}** tiene {len(adv2)} ventaja(s) identificada(s)")
            
            differences_text = '\n'.join(differences)
            
            # Balance
            if team1.get('win_probability', 50) > 60:
                balance = f"⚖️ **Ventaja clara para {team1_name}**\n\nLa diferencia de {score_diff:.1f} puntos sugiere un match favorable."
            elif team2.get('win_probability', 50) > 60:
                balance = f"⚖️ **Ventaja clara para {team2_name}**\n\nLa diferencia de {score_diff:.1f} puntos sugiere un match favorable."
            else:
                balance = f"⚖️ **Match equilibrado**\n\nAmbos equipos tienen posibilidades reales de victoria."
            
            # Veredicto y predicción
            verdict = comparison_result.get('verdict', 'Match competitivo')
            
            prob1 = team1.get('win_probability', 50)
            prob2 = team2.get('win_probability', 50)
            prediction = f"**{team1_name}:** {prob1:.0f}% probabilidad\n"
            prediction += f"**{team2_name}:** {prob2:.0f}% probabilidad\n\n"
            if prob1 > prob2:
                prediction += f"Se proyecta victoria de **{team1_name}**"
            elif prob2 > prob1:
                prediction += f"Se proyecta victoria de **{team2_name}**"
            else:
                prediction += "**Resultado incierto** - Dependerá de la ejecución"
            
            # Recomendación
            recommendations = comparison_result.get('recommendation', [])
            recommendation = '\n'.join([f"• {r}" for r in recommendations])
            
            # Formatear
            result = template.format(
                team1_name=team1_name,
                team2_name=team2_name,
                team1_num=team1_num,
                team2_num=team2_num,
                team1_desc=team1_desc,
                team2_desc=team2_desc,
                differences=differences_text,
                verdict=verdict,
                strategy=recommendation,
                team1_score=team1.get('score', 0),
                team2_score=team2.get('score', 0),
                team1_category=team1.get('category', 'N/A'),
                team2_category=team2.get('category', 'N/A'),
                team1_strengths=team1_strengths,
                team2_strengths=team2_strengths,
                balance=balance,
                prediction=prediction,
                recommendation=recommendation
            )
            
            return result
            
        except Exception as e:
            return f"Error generando comparación: {str(e)}"
    
    def _get_performance_adjective(self, wins, losses):
        """Obtiene adjetivo de rendimiento"""
        if wins + losses == 0:
            return "potencial aún por determinar"
        
        ratio = wins / (wins + losses)
        if ratio >= 0.75:
            return "**dominio consistente**"
        elif ratio >= 0.60:
            return "**sólida competitividad**"
        elif ratio >= 0.45:
            return "**resultados mixtos pero prometedores**"
        else:
            return "**margen de mejora significativo**"

# Instancia global
text_analyzer = TextAnalyzer()
