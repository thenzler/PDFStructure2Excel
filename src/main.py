#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDFStructure2Excel - Konvertiert strukturierte PDF-Dokumente in Excel-Format
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

# Füge das Projektverzeichnis zum Systempfad hinzu
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.insert(0, project_dir)

from src.ui.main_window import PDFtoExcelApp

def main():
    """Hauptfunktion der Anwendung"""
    app = QApplication(sys.argv)
    app.setApplicationName("PDFStructure2Excel")
    app.setApplicationVersion("1.0.0")
    
    # Setze das App-Icon
    icon_path = os.path.join(project_dir, 'resources', 'icons', 'app_icon.png')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    window = PDFtoExcelApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
