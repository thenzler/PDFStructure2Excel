#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Drag & Drop-Bereich für PDFStructure2Excel
"""

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent

class DropArea(QLabel):
    """Drag & Drop-Bereich für PDF-Dateien"""
    
    def __init__(self, parent=None):
        super(DropArea, self).__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setText("Drag & Drop PDF hier\noder klicken, um Datei auszuwählen")
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaaaaa;
                border-radius: 10px;
                padding: 20px;
                background-color: #f8f8f8;
                font-size: 14px;
                min-height: 150px;
            }
            QLabel:hover {
                background-color: #f0f0f0;
                border-color: #666666;
            }
        """)
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Behandelt das Drag-Enter-Ereignis"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if any(url.toLocalFile().endswith('.pdf') for url in urls):
                event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Behandelt das Drop-Ereignis"""
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith('.pdf'):
                self.parent().load_pdf(file_path)
                break
