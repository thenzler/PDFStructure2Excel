#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Hauptfenster für PDFStructure2Excel
"""

import os
import pandas as pd
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem,
                            QComboBox, QFormLayout, QTabWidget, QMessageBox,
                            QGroupBox, QProgressBar, QCheckBox, QStyle, QLineEdit,
                            QToolButton, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont

from src.ui.drop_area import DropArea
from src.pdf_processor import PDFProcessWorker
from src.excel_template import create_excel_template

class PDFtoExcelApp(QMainWindow):
    """Hauptfenster der Anwendung"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDFStructure2Excel")
        self.setMinimumSize(1024, 768)
        self._set_stylesheet()
        
        # Daten
        self.pdf_path = None
        self.structured_data = None
        
        # Setup UI
        self._setup_ui()
    
    def _set_stylesheet(self):
        """Setzt das Stylesheet für die Anwendung"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QLabel {
                font-size: 13px;
            }
            QTableWidget {
                gridline-color: #d0d0d0;
                font-size: 12px;
            }
            QTableWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 16px;
            }
            QTabWidget::pane {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #f0f0f0;
                border: 1px solid #d0d0d0;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 100px;
                padding: 8px 16px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 1px solid white;
            }
            QToolButton {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 4px;
                background-color: #f7f7f7;
            }
            QToolButton:hover {
                background-color: #e0e0e0;
            }
        """)
    
    def _setup_ui(self):
        """Erstellt die Benutzeroberfläche"""
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        # Fortschrittsbalken
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(True)
        
        # Tab-Widget für die Hauptfunktionen
        tabs = QTabWidget()
        
        # Tab 1: PDF auswählen und konvertieren
        import_tab = QWidget()
        import_layout = QVBoxLayout(import_tab)
        
        # PDF-Auswahl-Bereich
        pdf_group = QGroupBox("PDF-Datei auswählen")
        pdf_layout = QVBoxLayout(pdf_group)
        
        # Drop-Bereich für PDFs
        self.drop_area = DropArea(self)
        self.drop_area.mousePressEvent = lambda e: self._browse_pdf()
        pdf_layout.addWidget(self.drop_area)
        
        # Anzeige des ausgewählten PDF
        self.pdf_info = QLabel("Keine Datei ausgewählt")
        self.pdf_info.setAlignment(Qt.AlignCenter)
        pdf_layout.addWidget(self.pdf_info)
        
        # Struktur-Vorlagen
        structure_group = QGroupBox("Struktur-Vorlage auswählen")
        structure_layout = QVBoxLayout(structure_group)
        
        # Hinweis zum Strukturmuster
        structure_hint = QLabel(
            "Das Programm erkennt die Struktur basierend auf dem Muster: <b>Level Symbol Type Title_de Text_de</b>.<br>"
            "Beispiel: '1 A Einleitung: Qualitätsrichtlinien' wird als Level=1, Symbol=A, Type=CHAPTER, "
            "Title_de=Einleitung, Text_de=Qualitätsrichtlinien erkannt."
        )
        structure_hint.setWordWrap(True)
        structure_layout.addWidget(structure_hint)
        
        # Auswahl der Strukturvorlage
        template_layout = QHBoxLayout()
        template_label = QLabel("Wählen Sie eine vordefinierte Vorlage:")
        self.structure_combo = QComboBox()
        self.structure_combo.addItem("Palliative Care - Auditkriterien", "palliative_care")
        self.structure_combo.addItem("ISO-Norm", "iso_standard")
        self.structure_combo.addItem("Allgemeine Struktur", "general")
        self.structure_combo.addItem("Benutzerdefiniert", "custom")
        
        # Hilfe-Button für Struktur-Beispiele
        help_btn = QToolButton()
        help_btn.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxQuestion))
        help_btn.setToolTip("Beispiele für Strukturmuster anzeigen")
        help_btn.clicked.connect(self._show_structure_examples)
        
        template_layout.addWidget(template_label)
        template_layout.addWidget(self.structure_combo)
        template_layout.addWidget(help_btn)
        structure_layout.addLayout(template_layout)
        
        # Konvertierungsbutton
        convert_btn = QPushButton("PDF konvertieren")
        convert_btn.setIcon(self.style().standardIcon(QStyle.SP_ArrowForward))
        convert_btn.clicked.connect(self._convert_pdf)
        
        # Layout für Tab 1
        import_layout.addWidget(pdf_group)
        import_layout.addWidget(structure_group)
        import_layout.addWidget(convert_btn)
        import_layout.addStretch()
        
        # Tab 2: Ergebnis-Ansicht
        result_tab = QWidget()
        result_layout = QVBoxLayout(result_tab)
        
        # Erklärung der Strukturelemente
        structure_info = QGroupBox("Strukturelement-Erklärung")
        structure_info_layout = QVBoxLayout(structure_info)
        
        structure_info_text = QLabel(
            "<b>Level:</b> Hierarchische Ebene im Dokument (1, 2, 3, ...)<br>"
            "<b>Symbol:</b> Identifikator eines Elements (A, B1, C2.1, ...)<br>"
            "<b>Type:</b> Elementtyp (CHAPTER, REQUIREMENT, ...)<br>"
            "<b>Title_de:</b> Titel oder Überschrift<br>"
            "<b>Text_de:</b> Textinhalt oder Beschreibung"
        )
        structure_info_text.setWordWrap(True)
        structure_info_layout.addWidget(structure_info_text)
        
        # Ergebnistabelle
        result_label = QLabel("Extrahierte Struktur:")
        result_label.setFont(QFont("", -1, QFont.Bold))
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(5)
        self.result_table.setHorizontalHeaderLabels(["Level", "Symbol", "Type", "Title_de", "Text_de"])
        self.result_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Interactive)
        self.result_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        
        # Exportbereich
        export_group = QGroupBox("Daten exportieren")
        export_layout = QHBoxLayout(export_group)
        
        export_label = QLabel("Exportieren als:")
        self.normal_export_btn = QPushButton("Standard Excel")
        self.normal_export_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.normal_export_btn.clicked.connect(lambda: self._export_to_excel(use_template=False))
        self.normal_export_btn.setEnabled(False)
        
        self.template_export_btn = QPushButton("Formatiertes Excel")
        self.template_export_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.template_export_btn.clicked.connect(lambda: self._export_to_excel(use_template=True))
        self.template_export_btn.setEnabled(False)
        
        export_layout.addWidget(export_label)
        export_layout.addWidget(self.normal_export_btn)
        export_layout.addWidget(self.template_export_btn)
        export_layout.addStretch()
        
        # Layout für Tab 2
        result_layout.addWidget(structure_info)
        result_layout.addWidget(result_label)
        result_layout.addWidget(self.result_table)
        result_layout.addWidget(export_group)
        
        # Tab 3: Erweiterte Einstellungen
        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)
        
        # Strukturregeln
        rules_group = QGroupBox("Strukturregeln anpassen")
        rules_layout = QFormLayout(rules_group)
        
        self.level_pattern = QLineEdit(r"^\s*(\d+)")
        self.symbol_pattern = QLineEdit(r"^\s*(?:\d+\s+)?([A-Z](?:\d+(?:\.\d+)*)?)")
        
        level_help = QLabel("Erkennungsmuster für die Level-Nummer (z.B. 1, 2, 3, ...)")
        symbol_help = QLabel("Erkennungsmuster für das Symbol (z.B. A, B1, C2.1, ...)")
        level_help.setStyleSheet("font-size: 11px; color: #666;")
        symbol_help.setStyleSheet("font-size: 11px; color: #666;")
        
        rules_layout.addRow("Level-Muster:", self.level_pattern)
        rules_layout.addRow("", level_help)
        rules_layout.addRow("Symbol-Muster:", self.symbol_pattern)
        rules_layout.addRow("", symbol_help)
        
        # Vorverarbeitungsoptionen
        preprocess_group = QGroupBox("Vorverarbeitung")
        preprocess_layout = QVBoxLayout(preprocess_group)
        
        self.remove_headers = QCheckBox("Entferne Kopf- und Fußzeilen")
        self.remove_headers.setChecked(True)
        self.merge_lines = QCheckBox("Zusammenhängende Zeilen zusammenführen")
        self.merge_lines.setChecked(True)
        
        preprocess_layout.addWidget(self.remove_headers)
        preprocess_layout.addWidget(self.merge_lines)
        
        # Layout für Tab 3
        settings_layout.addWidget(rules_group)
        settings_layout.addWidget(preprocess_group)
        settings_layout.addStretch()
        
        # Tabs hinzufügen
        tabs.addTab(import_tab, "PDF importieren")
        tabs.addTab(result_tab, "Ergebnisse")
        tabs.addTab(settings_tab, "Erweiterte Einstellungen")
        
        # Hauptlayout
        main_layout.addWidget(tabs)
        main_layout.addWidget(self.progress_bar)
        
        self.setCentralWidget(central_widget)
    
    def _browse_pdf(self):
        """Öffnet den Datei-Dialog zum Auswählen einer PDF"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "PDF-Datei auswählen", "", "PDF-Dateien (*.pdf);;Alle Dateien (*.*)"
        )
        if file_path:
            self.load_pdf(file_path)
    
    def load_pdf(self, file_path):
        """Lädt eine PDF-Datei"""
        self.pdf_path = file_path
        base_name = os.path.basename(file_path)
        self.pdf_info.setText(f"Ausgewählte Datei: {base_name}")
    
    def _convert_pdf(self):
        """Startet die Konvertierung der PDF"""
        if not self.pdf_path:
            QMessageBox.warning(self, "Keine Datei", "Bitte wählen Sie zuerst eine PDF-Datei aus.")
            return
        
        # Zeige Fortschrittsbalken
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        
        # Struktur-Regeln sammeln
        structure_type = self.structure_combo.currentData()
        
        # Benutzerdefinierte Regeln, wenn ausgewählt
        custom_rules = None
        if structure_type == "custom":
            custom_rules = {
                'level_pattern': self.level_pattern.text(),
                'symbol_pattern': self.symbol_pattern.text(),
                'remove_headers': self.remove_headers.isChecked(),
                'merge_lines': self.merge_lines.isChecked()
            }
        
        # Worker-Thread für die Verarbeitung starten
        self.worker = PDFProcessWorker(self.pdf_path, structure_type, custom_rules)
        self.worker.progress_signal.connect(self._update_progress)
        self.worker.result_signal.connect(self._handle_result)
        self.worker.error_signal.connect(self._handle_error)
        self.worker.start()
    
    def _update_progress(self, value):
        """Aktualisiert den Fortschrittsbalken"""
        self.progress_bar.setValue(value)
    
    def _handle_result(self, result):
        """Verarbeitet das Ergebnis der PDF-Konvertierung"""
        self.structured_data = result
        self._display_result()
        self.progress_bar.setVisible(False)
        # Wechsel zum Ergebnis-Tab
        self.centralWidget().findChild(QTabWidget).setCurrentIndex(1)
        self.normal_export_btn.setEnabled(True)
        self.template_export_btn.setEnabled(True)
    
    def _handle_error(self, error_msg):
        """Behandelt Fehler bei der Konvertierung"""
        self.progress_bar.setVisible(False)
        QMessageBox.critical(self, "Fehler", f"Ein Fehler ist aufgetreten: {error_msg}")
    
    def _display_result(self):
        """Zeigt die Ergebnisse in der Tabelle an"""
        data = self.structured_data
        self.result_table.setRowCount(len(data))
        
        for row, item in enumerate(data):
            level = str(item.get("Level", ""))
            symbol = str(item.get("Symbol", ""))
            type_value = str(item.get("Type", ""))
            title = str(item.get("Title_de", ""))
            text = str(item.get("Text_de", ""))
            
            # Farbe je nach Typ
            is_chapter = type_value == "CHAPTER"
            
            # Items erstellen
            level_item = QTableWidgetItem(level)
            symbol_item = QTableWidgetItem(symbol)
            type_item = QTableWidgetItem(type_value)
            title_item = QTableWidgetItem(title)
            text_item = QTableWidgetItem(text)
            
            # Schriftart basierend auf Hierarchie
            font = QFont()
            if level == "1":
                font.setBold(True)
                font.setPointSize(12)
            elif level == "2":
                font.setBold(True)
            
            # Schriftart für alle Zellen in der Zeile setzen
            for item in [level_item, symbol_item, type_item, title_item, text_item]:
                item.setFont(font)
                
                # Hintergrundfarbe für Kapitel
                if is_chapter:
                    item.setBackground(Qt.lightGray)
            
            # Items einfügen
            self.result_table.setItem(row, 0, level_item)
            self.result_table.setItem(row, 1, symbol_item)
            self.result_table.setItem(row, 2, type_item)
            self.result_table.setItem(row, 3, title_item)
            self.result_table.setItem(row, 4, text_item)
        
        # Spaltenbreiten anpassen
        self.result_table.resizeColumnsToContents()
    
    def _export_to_excel(self, use_template=False):
        """Exportiert die Ergebnisse als Excel-Datei"""
        if not self.structured_data:
            return
        
        # Dialog zum Speichern der Excel-Datei
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Excel-Datei speichern", "", "Excel-Dateien (*.xlsx);;Alle Dateien (*.*)"
        )
        
        if file_path:
            try:
                if use_template:
                    # Verwende den Excel-Template-Generator
                    create_excel_template(self.structured_data, file_path)
                else:
                    # Einfacher Excel-Export
                    df = pd.DataFrame(self.structured_data)
                    df.to_excel(file_path, index=False)
                
                QMessageBox.information(
                    self, 
                    "Erfolg", 
                    f"Daten wurden erfolgreich nach {file_path} exportiert."
                )
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Fehler beim Exportieren: {str(e)}")
    
    def _show_structure_examples(self):
        """Zeigt Beispiele für Strukturmuster an"""
        example_text = """
<h3>Beispiele für Strukturmuster</h3>

<b>Palliative Care (aktuell ausgewählt):</b>
<pre>
1 A Einleitung: Qualitätsrichtlinien für Palliative Care
2 B1 Definition: Palliative Care ist ein Ansatz...
3 C2.1 Anforderung: Systematische Erfassung von Symptomen
</pre>

<b>ISO-Norm:</b>
<pre>
1 Anwendungsbereich
4.1 Verstehen der Organisation: Die Organisation muss...
5.2 Politik: Die oberste Leitung muss...
</pre>

<b>Allgemeine Struktur:</b>
<pre>
1 TEIL1 Einführung in das Thema
2 KAP2 Wichtige Grundlagen zum Verständnis
3 ABS3.1 Unterabschnitt mit Details
</pre>

<b>Das Strukturmuster enthält 5 Elemente:</b>
1. <b>Level:</b> Hierarchische Ebene (1, 2, 3, ...)
2. <b>Symbol:</b> Identifikator (A, B1, C2.1, ...)
3. <b>Type:</b> Automatisch erkannt (CHAPTER, REQUIREMENT)
4. <b>Title_de:</b> Titel vor dem Doppelpunkt
5. <b>Text_de:</b> Text nach dem Doppelpunkt
"""
        
        QMessageBox.information(self, "Strukturmuster-Beispiele", example_text)
