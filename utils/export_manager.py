#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AZTLÁN DECODE - EXPORTADOR PDF/EXCEL
Sistema de exportación profesional de reportes
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import pandas as pd
from datetime import datetime
import io
import os

class ReportExporter:
    """Exportador de reportes en múltiples formatos"""
    
    def __init__(self, output_dir='exports'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Crear estilos personalizados"""
        self.styles.add(ParagraphStyle(
            name='AztlanTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=1  # Center
        ))
        
        self.styles.add(ParagraphStyle(
            name='AztlanSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#3b82f6'),
            spaceAfter=12
        ))
    
    def export_team_analysis_pdf(self, team_number, analysis_data, comparison_data=None):
        """
        Exportar análisis de equipo a PDF profesional
        
        Args:
            team_number: Número del equipo
            analysis_data: Datos del análisis completo
            comparison_data: (Opcional) Datos de comparación con otro equipo
        """
        filename = f"team_{team_number}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        
        story = []
        
        # Título principal
        story.append(Paragraph(f"🤖 ANÁLISIS FTC - EQUIPO {team_number}", self.styles['AztlanTitle']))
        story.append(Spacer(1, 12))
        
        # Información general
        story.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", self.styles['Normal']))
        story.append(Paragraph(f"Sistema: Aztlán Decode IA Ultra Potente", self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Sección: Resumen ejecutivo
        story.append(Paragraph("📊 RESUMEN EJECUTIVO", self.styles['AztlanSubtitle']))
        
        summary_data = [
            ['Métrica', 'Valor'],
            ['Score Global', f"{analysis_data.get('global_score', 0):.1f}/100"],
            ['Categoría', analysis_data.get('category', 'N/A')],
            ['Momentum', analysis_data.get('momentum_desc', 'N/A')],
            ['Score Futuro', f"{analysis_data.get('future_score', 0):.1f}/100"],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Sección: Fortalezas
        if analysis_data.get('strengths'):
            story.append(Paragraph("💪 FORTALEZAS", self.styles['AztlanSubtitle']))
            for strength in analysis_data['strengths']:
                story.append(Paragraph(f"• {strength}", self.styles['Normal']))
            story.append(Spacer(1, 12))
        
        # Sección: Debilidades
        if analysis_data.get('weaknesses'):
            story.append(Paragraph("⚠️ ÁREAS DE MEJORA", self.styles['AztlanSubtitle']))
            for weakness in analysis_data['weaknesses']:
                story.append(Paragraph(f"• {weakness}", self.styles['Normal']))
            story.append(Spacer(1, 12))
        
        # Sección: Estrategia
        if analysis_data.get('strategy'):
            story.append(Paragraph("🎯 ESTRATEGIA RECOMENDADA", self.styles['AztlanSubtitle']))
            for strategy in analysis_data['strategy']:
                priority = strategy.get('priority', 2)
                priority_text = "🔴 CRÍTICO" if priority == 1 else "🟡 IMPORTANTE" if priority == 2 else "🟢 OPCIONAL"
                story.append(Paragraph(f"[{priority_text}] {strategy.get('action', '')}", self.styles['Normal']))
            story.append(Spacer(1, 12))
        
        # Sección: Métricas detalladas
        story.append(PageBreak())
        story.append(Paragraph("📈 MÉTRICAS DETALLADAS", self.styles['AztlanSubtitle']))
        
        metrics = analysis_data.get('metrics', {})
        metrics_data = [
            ['Métrica', 'Valor'],
            ['Ranking Points', f"{metrics.get('ranking_points', 0)}"],
            ['Win Rate', f"{metrics.get('win_rate', 0):.1f}%"],
            ['OPR', f"{metrics.get('opr', 0):.2f}"],
            ['Consistency', f"{metrics.get('consistency', 0):.2f}"],
            ['Peak Performance', f"{metrics.get('peak_performance', 0)}"]
        ]
        
        metrics_table = Table(metrics_data, colWidths=[3*inch, 2*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(metrics_table)
        story.append(Spacer(1, 20))
        
        # Sección: Predicciones
        if analysis_data.get('prediction'):
            story.append(Paragraph("🔮 PREDICCIONES", self.styles['AztlanSubtitle']))
            pred = analysis_data['prediction']
            story.append(Paragraph(f"Outlook: {pred.get('outlook', 'N/A')}", self.styles['Normal']))
            story.append(Paragraph(f"Prob. Worlds: {pred.get('worlds_probability', 0):.1f}%", self.styles['Normal']))
            story.append(Paragraph(f"Prob. Victoria Regional: {pred.get('regional_win_probability', 0):.1f}%", self.styles['Normal']))
        
        # Sección: Comparación (si existe)
        if comparison_data:
            story.append(PageBreak())
            story.append(Paragraph("⚔️ COMPARACIÓN CON OTRO EQUIPO", self.styles['AztlanSubtitle']))
            
            comp_data = [
                ['Métrica', f"Equipo {team_number}", f"Equipo {comparison_data.get('team2_number', 'N/A')}"],
                ['Score', f"{comparison_data.get('team1_score', 0):.1f}", f"{comparison_data.get('team2_score', 0):.1f}"],
                ['Momentum', comparison_data.get('team1_momentum', 'N/A'), comparison_data.get('team2_momentum', 'N/A')],
                ['Win Prob.', f"{comparison_data.get('team1_win_prob', 0):.1f}%", f"{comparison_data.get('team2_win_prob', 0):.1f}%"]
            ]
            
            comp_table = Table(comp_data, colWidths=[2*inch, 2*inch, 2*inch])
            comp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f59e0b')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(comp_table)
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph("━" * 80, self.styles['Normal']))
        story.append(Paragraph("Aztlán Decode © 2026 - Sistema de IA Ultra Potente para FTC", self.styles['Normal']))
        
        # Construir PDF
        doc.build(story)
        
        return filepath
    
    def export_to_excel(self, team_number, analysis_data, historical_data=None):
        """
        Exportar datos a Excel con múltiples hojas
        
        Args:
            team_number: Número del equipo
            analysis_data: Datos del análisis
            historical_data: (Opcional) Datos históricos del equipo
        """
        filename = f"team_{team_number}_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join(self.output_dir, filename)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            
            # Hoja 1: Resumen
            summary_df = pd.DataFrame({
                'Métrica': ['Score Global', 'Categoría', 'Momentum', 'Score Futuro', 'Win Rate'],
                'Valor': [
                    analysis_data.get('global_score', 0),
                    analysis_data.get('category', 'N/A'),
                    analysis_data.get('momentum_desc', 'N/A'),
                    analysis_data.get('future_score', 0),
                    analysis_data.get('metrics', {}).get('win_rate', 0)
                ]
            })
            summary_df.to_excel(writer, sheet_name='Resumen', index=False)
            
            # Hoja 2: Fortalezas y Debilidades
            strengths_weaknesses_df = pd.DataFrame({
                'Tipo': ['Fortaleza'] * len(analysis_data.get('strengths', [])) +
                        ['Debilidad'] * len(analysis_data.get('weaknesses', [])),
                'Descripción': analysis_data.get('strengths', []) + analysis_data.get('weaknesses', [])
            })
            strengths_weaknesses_df.to_excel(writer, sheet_name='Análisis', index=False)
            
            # Hoja 3: Estrategia
            if analysis_data.get('strategy'):
                strategy_df = pd.DataFrame(analysis_data['strategy'])
                strategy_df.to_excel(writer, sheet_name='Estrategia', index=False)
            
            # Hoja 4: Métricas
            metrics = analysis_data.get('metrics', {})
            metrics_df = pd.DataFrame([metrics])
            metrics_df.to_excel(writer, sheet_name='Métricas', index=False)
            
            # Hoja 5: Datos históricos (si existen)
            if historical_data:
                historical_df = pd.DataFrame(historical_data)
                historical_df.to_excel(writer, sheet_name='Histórico', index=False)
        
        return filepath
    
    def export_comparison_csv(self, comparison_data):
        """Exportar comparación a CSV simple"""
        filename = f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(self.output_dir, filename)
        
        df = pd.DataFrame([comparison_data])
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        
        return filepath
    
    def export_regional_predictions_excel(self, regional_name, predictions):
        """Exportar predicciones de regional a Excel"""
        filename = f"regional_{regional_name}_{datetime.now().strftime('%Y%m%d')}.xlsx"
        filepath = os.path.join(self.output_dir, filename)
        
        df = pd.DataFrame(predictions)
        df.to_excel(filepath, index=False, engine='openpyxl')
        
        return filepath

# Instancia global
exporter = ReportExporter()
