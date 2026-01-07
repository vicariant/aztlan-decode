#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AZTLAN DECODE - EXPORTADOR AVANZADO
PDF y Excel con graficos profesionales
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from datetime import datetime
import os

class AdvancedExporter:
    """Exportador profesional de reportes"""
    
    def __init__(self, output_dir='exports'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._add_custom_styles()
    
    def _add_custom_styles(self):
        """Agregar estilos personalizados"""
        self.styles.add(ParagraphStyle(
            name='AztlanTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#FFD700'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='AztlanSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#4A90E2'),
            spaceBefore=20,
            spaceAfter=10
        ))
    
    # ==========================================
    # EXPORTAR PDF - ANALISIS DE EQUIPO
    # ==========================================
    
    def export_team_analysis_pdf(self, team_data: dict, filename: str = None) -> str:
        """Exportar analisis completo de equipo a PDF"""
        if not filename:
            filename = f"team_{team_data.get('number', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        filepath = os.path.join(self.output_dir, filename)
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        
        # Titulo
        title = Paragraph(
            f"🏛️ AZTLAN DECODE - Analisis de Equipo #{team_data.get('number', 'N/A')}",
            self.styles['AztlanTitle']
        )
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Informacion basica
        info_text = f"""
        <b>Nombre:</b> {team_data.get('name', 'N/A')}<br/>
        <b>Region:</b> {team_data.get('region', 'N/A')}<br/>
        <b>Temporada:</b> {team_data.get('season', '2024-2025')}<br/>
        <b>Fecha de Reporte:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}
        """
        story.append(Paragraph(info_text, self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Estadisticas
        if 'stats' in team_data:
            story.append(Paragraph("📊 ESTADISTICAS", self.styles['AztlanSubtitle']))
            stats_table = self._create_stats_table(team_data['stats'])
            story.append(stats_table)
            story.append(Spacer(1, 0.2*inch))
        
        # Grafica de radar si hay datos
        if 'radar_data' in team_data:
            radar_img = self._create_radar_chart(team_data['radar_data'])
            if radar_img:
                story.append(Paragraph("🕸️ ANALISIS MULTIDIMENSIONAL", self.styles['AztlanSubtitle']))
                story.append(radar_img)
                story.append(Spacer(1, 0.2*inch))
        
        # Predicciones
        if 'predictions' in team_data:
            story.append(Paragraph("🔮 PREDICCIONES IA", self.styles['AztlanSubtitle']))
            pred_text = f"""
            <b>OPR Estimado:</b> {team_data['predictions'].get('opr', 'N/A')}<br/>
            <b>Ranking Predicho:</b> {team_data['predictions'].get('rank', 'N/A')}<br/>
            <b>Probabilidad de Avanzar:</b> {team_data['predictions'].get('advance_prob', 'N/A')}%
            """
            story.append(Paragraph(pred_text, self.styles['Normal']))
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer = Paragraph(
            "<i>Generado por AZTLAN DECODE - Sistema Tridente de Analisis FTC</i>",
            self.styles['Normal']
        )
        story.append(footer)
        
        # Generar PDF
        doc.build(story)
        return filepath
    
    def _create_stats_table(self, stats: dict) -> Table:
        """Crear tabla de estadisticas"""
        data = [['Metrica', 'Valor']]
        for key, value in stats.items():
            data.append([key.replace('_', ' ').title(), str(value)])
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4A90E2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        return table
    
    def _create_radar_chart(self, radar_data: dict) -> Image:
        """Crear grafico de radar"""
        categories = list(radar_data.keys())
        values = list(radar_data.values())
        
        # Crear grafico
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='polar'))
        
        angles = [n / float(len(categories)) * 2 * 3.14159 for n in range(len(categories))]
        values += values[:1]
        angles += angles[:1]
        
        ax.plot(angles, values, 'o-', linewidth=2, color='#4A90E2')
        ax.fill(angles, values, alpha=0.25, color='#4A90E2')
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 100)
        
        # Guardar en memoria
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return Image(img_buffer, width=4*inch, height=4*inch)
    
    # ==========================================
    # EXPORTAR EXCEL
    # ==========================================
    
    def export_to_excel(self, data: dict, filename: str = None) -> str:
        """Exportar datos a Excel con formato"""
        if not filename:
            filename = f"aztlan_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Hoja de resumen
            if 'summary' in data:
                df_summary = pd.DataFrame([data['summary']])
                df_summary.to_excel(writer, sheet_name='Resumen', index=False)
            
            # Hoja de equipos
            if 'teams' in data:
                df_teams = pd.DataFrame(data['teams'])
                df_teams.to_excel(writer, sheet_name='Equipos', index=False)
            
            # Hoja de estadisticas
            if 'stats' in data:
                df_stats = pd.DataFrame(data['stats'])
                df_stats.to_excel(writer, sheet_name='Estadisticas', index=False)
        
        return filepath
    
    # ==========================================
    # EXPORTAR CSV
    # ==========================================
    
    def export_to_csv(self, data: list, filename: str = None) -> str:
        """Exportar datos a CSV"""
        if not filename:
            filename = f"aztlan_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        return filepath
    
    # ==========================================
    # EXPORTAR REPORTE COMPLETO DE EVENTO
    # ==========================================
    
    def export_event_report_pdf(self, event_data: dict, filename: str = None) -> str:
        """Exportar reporte completo de evento"""
        if not filename:
            filename = f"event_{event_data.get('code', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        filepath = os.path.join(self.output_dir, filename)
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        
        # Portada
        title = Paragraph(
            f"🏛️ REPORTE DE EVENTO FTC<br/>{event_data.get('name', 'N/A')}",
            self.styles['AztlanTitle']
        )
        story.append(title)
        story.append(Spacer(1, 1*inch))
        
        # Informacion del evento
        info = f"""
        <b>Codigo:</b> {event_data.get('code', 'N/A')}<br/>
        <b>Fecha:</b> {event_data.get('date', 'N/A')}<br/>
        <b>Ubicacion:</b> {event_data.get('location', 'N/A')}<br/>
        <b>Equipos Participantes:</b> {event_data.get('team_count', 'N/A')}
        """
        story.append(Paragraph(info, self.styles['Normal']))
        story.append(PageBreak())
        
        # Rankings
        if 'rankings' in event_data:
            story.append(Paragraph("🏆 RANKINGS FINALES", self.styles['AztlanSubtitle']))
            rankings_table = self._create_rankings_table(event_data['rankings'])
            story.append(rankings_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Premios
        if 'awards' in event_data:
            story.append(Paragraph("🎖️ PREMIOS", self.styles['AztlanSubtitle']))
            for award in event_data['awards']:
                award_text = f"<b>{award['name']}:</b> Team {award['team']}"
                story.append(Paragraph(award_text, self.styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
        
        doc.build(story)
        return filepath
    
    def _create_rankings_table(self, rankings: list) -> Table:
        """Crear tabla de rankings"""
        data = [['Rank', 'Team', 'W-L-T', 'RP', 'TBP']]
        for rank in rankings[:20]:  # Top 20
            data.append([
                rank.get('rank', '-'),
                rank.get('team', '-'),
                rank.get('record', '-'),
                rank.get('rp', '-'),
                rank.get('tbp', '-')
            ])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFD700')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        return table


# Instancia global
exporter = AdvancedExporter()
