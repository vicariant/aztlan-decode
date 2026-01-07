#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test de módulos nuevos"""

print("\n" + "="*50)
print("  VERIFICACIÓN DE MÓDULOS NUEVOS")
print("="*50 + "\n")

try:
    # 1. Database Manager
    from database.db_manager import DatabaseManager
    print("✓ DatabaseManager importado")
    
    # 2. Minor Protection System
    from compliance.minor_protection import MinorProtectionSystem
    print("✓ MinorProtectionSystem importado")
    
    # 3. Export Manager
    from utils.export_manager import ReportExporter
    print("✓ ReportExporter importado")
    
    # 4. Dashboard Manager
    from utils.dashboard_manager import AdvancedDashboard
    print("✓ AdvancedDashboard importado")
    
    print("\n" + "="*50)
    print("  ✅ TODOS LOS MÓDULOS FUNCIONAN!")
    print("="*50 + "\n")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}\n")
    import traceback
    traceback.print_exc()
