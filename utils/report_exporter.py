# -*- coding: utf-8 -*-
"""
EXPORTADOR DE REPORTES - AZTLÁN DECODE
Genera PDFs y CSVs de análisis
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import pandas as pd
import io
import os

class ReportExporter:
    """Exporta análisis a diferentes formatos"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Define estilos personalizados"""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#FFD700'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#00A86B'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Texto normal
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
    
    # =============================================================
    # EXPORTACIÓN A PDF
    # =============================================================
    
    def export_team_analysis_pdf(self, team_data, filename=None):
        """
        Exporta análisis de equipo a PDF
        
        Args:
            team_data: Dict con datos del equipo
            filename: Nombre del archivo (opcional)
        
        Returns:
            BytesIO object con el PDF o ruta del archivo
        """
        if filename is None:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter,
                                   rightMargin=72, leftMargin=72,
                                   topMargin=72, bottomMargin=18)
        else:
            doc = SimpleDocTemplate(filename, pagesize=letter,
                                   rightMargin=72, leftMargin=72,
                                   topMargin=72, bottomMargin=18)
        
        # Contenedor de elementos
        story = []
        
        # Encabezado
        title = Paragraph(
            f"🏺 ANÁLISIS AZTLÁN DECODE<br/>Equipo #{team_data.get('team_number', 'N/A')}",
            self.styles['CustomTitle']
        )
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Información básica
        story.append(Paragraph("📊 INFORMACIÓN DEL EQUIPO", self.styles['CustomHeading']))
        
        info_data = [
            ['Nombre:', team_data.get('team_name', 'N/A')],
            ['Número:', str(team_data.get('team_number', 'N/A'))],
            ['Ciudad:', team_data.get('city', 'N/A')],
            ['Estado:', team_data.get('state', 'N/A')],
            ['País:', team_data.get('country', 'N/A')],
            ['Fecha de análisis:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F0F0F0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Métricas de rendimiento
        if any(key in team_data for key in ['ranking', 'opr', 'win_rate']):
            story.append(Paragraph("⚡ MÉTRICAS DE RENDIMIENTO", self.styles['CustomHeading']))
            
            metrics_data = [['Métrica', 'Valor']]
            if 'ranking' in team_data:
                metrics_data.append(['Ranking', f"#{team_data['ranking']}"])
            if 'opr' in team_data:
                metrics_data.append(['OPR', f"{team_data['opr']:.2f}"])
            if 'win_rate' in team_data:
                metrics_data.append(['Win Rate', f"{team_data['win_rate']:.1f}%"])
            if 'matches_played' in team_data:
                metrics_data.append(['Partidos jugados', str(team_data['matches_played'])])
            
            metrics_table = Table(metrics_data, colWidths=[3*inch, 3*inch])
            metrics_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00A86B')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')])
            ]))
            story.append(metrics_table)
            story.append(Spacer(1, 20))
        
        # Análisis IA
        if 'ai_analysis' in team_data and team_data['ai_analysis']:
            story.append(Paragraph("🤖 ANÁLISIS DE INTELIGENCIA ARTIFICIAL", self.styles['CustomHeading']))
            ai_text = Paragraph(team_data['ai_analysis'], self.styles['CustomBody'])
            story.append(ai_text)
            story.append(Spacer(1, 20))
        
        # Recomendaciones estratégicas
        if 'recommendations' in team_data and team_data['recommendations']:
            story.append(Paragraph("⚔️ RECOMENDACIONES ESTRATÉGICAS", self.styles['CustomHeading']))
            rec_text = Paragraph(team_data['recommendations'], self.styles['CustomBody'])
            story.append(rec_text)
            story.append(Spacer(1, 20))
        
        # Consenso TRIDENTE
        if 'consensus' in team_data and team_data['consensus']:
            story.append(Paragraph("🔱 CONSENSO TRIDENTE", self.styles['CustomHeading']))
            consensus_text = Paragraph(team_data['consensus'], self.styles['CustomBody'])
            story.append(consensus_text)
        
        # Footer
        story.append(Spacer(1, 40))
        footer = Paragraph(
            "<i>Generado por AZTLÁN DECODE - Sistema de Análisis FTC</i><br/>"
            f"<i>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>",
            self.styles['Normal']
        )
        story.append(footer)
        
        # Generar PDF
        doc.build(story)
        
        if filename is None:
            buffer.seek(0)
            return buffer
        return filename
    
    def export_comparison_pdf(self, team1_data, team2_data, comparison_data, filename=None):
        """Exporta comparación de equipos a PDF"""
        if filename is None:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
        else:
            doc = SimpleDocTemplate(filename, pagesize=letter)
        
        story = []
        
        # Título
        title = Paragraph(
            f"⚔️ COMPARACIÓN DE EQUIPOS<br/>"
            f"#{team1_data.get('team_number')} vs #{team2_data.get('team_number')}",
            self.styles['CustomTitle']
        )
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Tabla comparativa
        comp_data = [
            ['Métrica', f"Equipo {team1_data.get('team_number')}", f"Equipo {team2_data.get('team_number')}"],
            ['Nombre', team1_data.get('team_name', 'N/A'), team2_data.get('team_name', 'N/A')],
            ['Ranking', f"#{team1_data.get('ranking', 'N/A')}", f"#{team2_data.get('ranking', 'N/A')}"],
            ['OPR', f"{team1_data.get('opr', 0):.2f}", f"{team2_data.get('opr', 0):.2f}"],
            ['Win Rate', f"{team1_data.get('win_rate', 0):.1f}%", f"{team2_data.get('win_rate', 0):.1f}%"],
        ]
        
        comp_table = Table(comp_data, colWidths=[2*inch, 2*inch, 2*inch])
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFD700')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')])
        ]))
        story.append(comp_table)
        story.append(Spacer(1, 20))
        
        # Análisis IA
        if comparison_data.get('ai_analysis'):
            story.append(Paragraph("🤖 ANÁLISIS ESTRATÉGICO", self.styles['CustomHeading']))
            story.append(Paragraph(comparison_data['ai_analysis'], self.styles['CustomBody']))
        
        doc.build(story)
        
        if filename is None:
            buffer.seek(0)
            return buffer
        return filename
    
    # =============================================================
    # EXPORTACIÓN A CSV/EXCEL
    # =============================================================
    
    def export_team_analysis_csv(self, team_data, filename=None):
        """Exporta análisis de equipo a CSV"""
        # Crear DataFrame
        df = pd.DataFrame([{
            'team_number': team_data.get('team_number'),
            'team_name': team_data.get('team_name'),
            'city': team_data.get('city'),
            'state': team_data.get('state'),
            'country': team_data.get('country'),
            'ranking': team_data.get('ranking'),
            'opr': team_data.get('opr'),
            'win_rate': team_data.get('win_rate'),
            'matches_played': team_data.get('matches_played'),
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }])
        
        if filename is None:
            return df.to_csv(index=False)
        else:
            df.to_csv(filename, index=False)
            return filename
    
    def export_multiple_teams_csv(self, teams_data, filename=None):
        """Exporta múltiples equipos a CSV"""
        df = pd.DataFrame(teams_data)
        
        if filename is None:
            return df.to_csv(index=False)
        else:
            df.to_csv(filename, index=False)
            return filename
    
    def export_to_excel(self, teams_data, filename='teams_analysis.xlsx'):
        """Exporta a Excel con múltiples hojas"""
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Hoja principal con resumen
            df_summary = pd.DataFrame(teams_data)
            df_summary.to_excel(writer, sheet_name='Resumen', index=False)
            
            # Hoja con estadísticas
            if len(teams_data) > 0:
                stats = {
                    'Total equipos analizados': len(teams_data),
                    'OPR promedio': df_summary['opr'].mean() if 'opr' in df_summary else 0,
                    'Win rate promedio': df_summary['win_rate'].mean() if 'win_rate' in df_summary else 0,
                }
                df_stats = pd.DataFrame([stats])
                df_stats.to_excel(writer, sheet_name='Estadísticas', index=False)
        
        return filename
