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
                            QToolButton, QHeaderView, QTextEdit, QSplitter)
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
        self.setMinimumSize(1200, 800)
        self._set_stylesheet()
        
        # Daten
        self.pdf_path = None
        self.structured_data = None
        self.extracted_text = None
        
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
            QTextEdit {
                font-family: Consolas, monospace;
                font-size: 12px;
                line-height: 1.5;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 5px;
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
            "Das Programm extrahiert zuerst den Text aus dem PDF und erkennt dann die Struktur "
            "basierend auf dem Muster: <b>Level Symbol Type Title_de Text_de</b>.<br>"
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
        
        # Tab 2: Konvertierungsergebnisse
        convert_tab = QWidget()
        convert_layout = QVBoxLayout(convert_tab)
        
        # Splitter zum Teilen des Tabs in Text und Strukturerkennung
        splitter = QSplitter(Qt.Vertical)
        
        # Bereich 1: Extrahierter Text
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        
        text_label = QLabel("<b>SCHRITT 1: Extrahierter Text aus dem PDF</b>")
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlaceholderText("Der extrahierte Text aus dem PDF wird hier angezeigt.")
        
        text_layout.addWidget(text_label)
        text_layout.addWidget(self.text_edit)
        
        # Bereich 2: Erkannte Struktur
        structure_widget = QWidget()
        structure_layout = QVBoxLayout(structure_widget)
        
        # Erklärung der Strukturelemente
        structure_label = QLabel("<b>SCHRITT 2: Erkannte Struktur (Level Symbol Type Title_de Text_de)</b>")
        
        # Strukturinformation
        structure_info = QGroupBox("Bedeutung der Spalten")
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
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(5)
        self.result_table.setHorizontalHeaderLabels(["Level", "Symbol", "Type", "Title_de", "Text_de"])
        self.result_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Interactive)
        self.result_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        
        structure_layout.addWidget(structure_label)
        structure_layout.addWidget(structure_info)
        structure_layout.addWidget(self.result_table)
        
        # Hinzufügen zum Splitter
        splitter.addWidget(text_widget)
        splitter.addWidget(structure_widget)
        splitter.setSizes([300, 500])  # Anfangsgröße
        
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
        convert_layout.addWidget(splitter)
        convert_layout.addWidget(export_group)
        
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
        tabs.addTab(convert_tab, "Konvertierungsergebnisse")
        tabs.addTab(settings_tab, "Erweiterte Einstellungen")
        
        # Hauptlayout
        main_layout.addWidget(tabs)
        main_layout.addWidget(self.progress_bar)
        
        self.setCentralWidget(central_widget)
        self.tabs = tabs  # Speichere Referenz auf Tabs
    
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

        # Fortschrittsbalken anzeigen
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        
        # Struktur-Vorlage auswählen
        template_type = self.structure_combo.currentData()
        
        # Optionen für die Verarbeitung
        options = {
            "remove_headers": self.remove_headers.isChecked(),
            "merge_lines": self.merge_lines.isChecked(),
            "level_pattern": self.level_pattern.text(),
            "symbol_pattern": self.symbol_pattern.text(),
            "template_type": template_type
        }
        
        # PDF-Verarbeitung starten (in einem separaten Thread)
        self.worker = PDFProcessWorker(self.pdf_path, options)
        self.worker.progress_signal.connect(self.progress_bar.setValue)
        self.worker.text_extracted_signal.connect(self._display_extracted_text)
        self.worker.result_signal.connect(self._display_structure)
        self.worker.finished.connect(self._on_conversion_finished)
        self.worker.error_signal.connect(self._on_conversion_error)
        self.worker.start()
        
        # Zur Ergebnisansicht wechseln
        self.tabs.setCurrentIndex(1)
    
    def _display_extracted_text(self, text):
        """Zeigt den extrahierten Text im TextEdit an"""
        self.extracted_text = text
        self.text_edit.setText(text)
    
    def _display_structure(self, data):
        """Zeigt die erkannte Struktur in der Tabelle an"""
        self.structured_data = data
        
        # Tabelle leeren
        self.result_table.setRowCount(0)
        
        # Daten einfüllen
        for row_idx, row_data in enumerate(data):
            self.result_table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data.values()):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.result_table.setItem(row_idx, col_idx, item)
        
        # Export-Buttons aktivieren
        self.normal_export_btn.setEnabled(True)
        self.template_export_btn.setEnabled(True)
    
    def _on_conversion_finished(self):
        """Wird aufgerufen, wenn die Konvertierung abgeschlossen ist"""
        self.progress_bar.setVisible(False)
        QMessageBox.information(
            self, 
            "Konvertierung abgeschlossen", 
            "Die PDF wurde erfolgreich konvertiert. Sie können die Daten jetzt exportieren."
        )
    
    def _on_conversion_error(self, error_msg):
        """Wird bei einem Fehler während der Konvertierung aufgerufen"""
        self.progress_bar.setVisible(False)
        QMessageBox.critical(self, "Fehler bei der Konvertierung", error_msg)
    
    def _export_to_excel(self, use_template=False):
        """Exportiert die Daten in eine Excel-Datei"""
        if not self.structured_data:
            QMessageBox.warning(self, "Keine Daten", "Es sind keine Daten zum Exportieren vorhanden.")
            return
        
        # Excel-Datei speichern
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Excel-Datei speichern", "", "Excel-Dateien (*.xlsx);;Alle Dateien (*.*)"
        )
        
        if not file_path:
            return
        
        if not file_path.endswith(".xlsx"):
            file_path += ".xlsx"
        
        try:
            # DataFrame aus strukturierten Daten erstellen
            df = pd.DataFrame(self.structured_data)
            
            if use_template:
                # Mit Formatvorlage exportieren
                create_excel_template(df, file_path)
            else:
                # Standard-Export
                df.to_excel(file_path, index=False)
            
            QMessageBox.information(
                self, 
                "Export erfolgreich", 
                f"Die Daten wurden erfolgreich nach {file_path} exportiert."
            )
        except Exception as e:
            QMessageBox.critical(self, "Fehler beim Export", f"Fehler beim Exportieren: {str(e)}")
    
    def _show_structure_examples(self):
        """Zeigt Beispiele für die verschiedenen Strukturmuster an"""
        examples = {
            "palliative_care": (
                "1 A CHAPTER Qualitätsrichtlinien: Beschreibung der Qualitätsanforderungen für die Palliativversorgung.\n"
                "2 A1 REQUIREMENT Dokumentation: Alle Maßnahmen müssen vollständig dokumentiert werden.\n"
                "3 A1.1 CRITERION Checkliste: Die Checkliste muss vollständig ausgefüllt werden."
            ),
            "iso_standard": (
                "1 4 CHAPTER Kontext der Organisation: Die Organisation muss externe und interne Themen bestimmen.\n"
                "2 4.1 REQUIREMENT Verstehen der Organisation: Die Organisation und ihr Kontext müssen definiert werden.\n"
                "3 4.1.1 NOTE Hinweis: Externe und interne Themen können positiv oder negativ sein."
            ),
            "general": (
                "1 1 SECTION Einleitung: Dieser Abschnitt enthält grundlegende Informationen.\n"
                "2 1.1 SUBSECTION Hintergrund: Hier werden die Hintergrundinformationen beschrieben.\n"
                "3 1.1.1 ITEM Wichtiger Punkt: Dieser Punkt ist besonders hervorzuheben."
            )
        }
        
        current_template = self.structure_combo.currentData()
        message = f"<h3>Beispiel für die Vorlage \"{self.structure_combo.currentText()}\":</h3>"
        
        if current_template in examples:
            message += f"<pre>{examples[current_template]}</pre>"
        else:
            message += (
                "<p>Für benutzerdefinierte Vorlagen können Sie die Erkennungsmuster "
                "im Tab \"Erweiterte Einstellungen\" anpassen.</p>"
            )
        
        QMessageBox.information(self, "Strukturbeispiele", message)
