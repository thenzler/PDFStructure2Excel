#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF-Verarbeitungsmodul für PDFStructure2Excel
"""

import re
import PyPDF2
from PyQt5.QtCore import QThread, pyqtSignal
from src.structure_rules import get_structure_rules

class PDFProcessWorker(QThread):
    """Worker-Thread für die PDF-Verarbeitung"""
    
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(object)
    error_signal = pyqtSignal(str)
    
    def __init__(self, pdf_path, structure_type='palliative_care', custom_rules=None):
        """
        Initialisiert den Worker
        
        Args:
            pdf_path (str): Pfad zur PDF-Datei
            structure_type (str): Typ der Dokumentstruktur
            custom_rules (dict, optional): Benutzerdefinierte Regeln
        """
        super().__init__()
        self.pdf_path = pdf_path
        self.structure_type = structure_type
        self.custom_rules = custom_rules
        
    def run(self):
        """Verarbeitet das PDF und extrahiert strukturierte Daten"""
        try:
            # Hole die Regeln für den ausgewählten Strukturtyp
            if self.structure_type == 'custom' and self.custom_rules:
                rules = self.custom_rules
            else:
                rules = get_structure_rules(self.structure_type)
                
            # Öffne das PDF und extrahiere Text
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                text = ""
                for i, page in enumerate(pdf_reader.pages):
                    text += page.extract_text() + "\n"
                    self.progress_signal.emit(int((i + 1) / total_pages * 50))
            
            # Vorverarbeitung
            if rules.get('remove_headers', True):
                text = self._remove_headers(text)
                
            if rules.get('merge_lines', True):
                text = self._merge_related_lines(text)
            
            # Extrahiere strukturierte Daten
            data = self._extract_structure(text, rules)
            self.result_signal.emit(data)
            
        except Exception as e:
            self.error_signal.emit(str(e))
    
    def _remove_headers(self, text):
        """Entfernt Kopf- und Fußzeilen aus dem Text"""
        lines = text.split('\n')
        filtered_lines = []
        
        for line in lines:
            # Überspringe typische Kopf- und Fußzeilen
            if re.match(r'^\s*\d+\s*$', line) or re.match(r'^\s*page\s+\d+\s*$', line, re.IGNORECASE):
                continue
            if "Kriterienliste für die stationäre Langzeitpflege" in line:
                continue
            filtered_lines.append(line)
        
        return '\n'.join(filtered_lines)
    
    def _merge_related_lines(self, text):
        """Führt zusammengehörige Zeilen zusammen"""
        # Vereinfachte Version - kann je nach Dokument angepasst werden
        # Verbindet Zeilen, wenn eine Zeile nicht mit einem strukturierten Element beginnt
        result = []
        lines = text.split('\n')
        i = 0
        
        while i < len(lines):
            if not lines[i].strip():
                i += 1
                continue
                
            current_line = lines[i]
            i += 1
            
            # Wenn die nächste Zeile nicht mit einer Nummer oder einem Symbol beginnt,
            # könnte sie zur aktuellen Zeile gehören
            while i < len(lines) and lines[i].strip() and not re.match(r'^\s*(\d+\s+[A-Z]|\d+\s+qualité|\s*[A-Z]\d+)', lines[i]):
                current_line += " " + lines[i].strip()
                i += 1
                
            result.append(current_line)
            
        return '\n'.join(result)
    
    def _extract_structure(self, text, rules):
        """Extrahiert strukturierte Daten aus dem Text basierend auf den Regeln"""
        result = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if not line.strip():
                continue
                
            self.progress_signal.emit(50 + int((i + 1) / len(lines) * 50))
            
            # Spezielle Behandlung für die erste Zeile mit "qualité palliative"
            if "qualité palliative" in line:
                result.append({
                    "Level": "1",
                    "Symbol": "qualité palliative SLZP:25",
                    "Type": "25",
                    "Title_de": "qualité palliative SLZP:25",
                    "Text_de": "Auditkriterien stationäre Langzeitpflege mit allgemeiner Palliative Care"
                })
                continue
            
            # Reguläre Strukturextraktion
            level_pattern = rules.get('level_pattern', r'^\s*(\d+)')
            symbol_pattern = rules.get('symbol_pattern', r'^\s*(?:\d+\s+)?([A-Z](?:\d+(?:\.\d+)*)?)')
            
            level_match = re.search(level_pattern, line)
            symbol_match = re.search(symbol_pattern, line)
            
            if level_match and symbol_match:
                # Extrahiere Symbol und bestimme den Typ
                symbol = symbol_match.group(1)
                type_value = self._determine_type(symbol, rules)
                
                # Extrahiere Titel und Text
                rest_of_line = line[max(level_match.end(), symbol_match.end()):].strip()
                title, text = self._extract_title_and_text(rest_of_line, rules)
                
                result.append({
                    "Level": level_match.group(1),
                    "Symbol": symbol,
                    "Type": type_value,
                    "Title_de": title,
                    "Text_de": text
                })
        
        return result
    
    def _determine_type(self, symbol, rules):
        """Bestimmt den Typ basierend auf dem Symbol und den Regeln"""
        # Für Palliative Care
        if self.structure_type == 'palliative_care':
            # Vorbestimmte Typen basierend auf der bekannten Struktur
            if len(symbol) == 1:  # z.B. "A", "B", "C"
                return "CHAPTER"
                
            if "." in symbol:  # z.B. "A1.1", "B2.3"
                return "REQUIREMENT"
                
            # Für Symbole wie A1, B2, etc.
            if any(c.isdigit() for c in symbol):
                if len(symbol) == 2:  # z.B. "A1"
                    return "CHAPTER"
                return "REQUIREMENT"
                
            return "CHAPTER"
        
        # Für andere Strukturtypen können hier spezifische Regeln hinzugefügt werden
        type_mapping = rules.get('type_mapping', {})
        
        # Basierend auf Symbolmuster bestimmen
        if len(symbol) == 1 and symbol.isalpha():
            return type_mapping.get('single_letter', 'CHAPTER')
            
        if re.match(r'^[A-Z]\d+$', symbol):
            return type_mapping.get('letter_number', 'CHAPTER')
            
        if re.match(r'^[A-Z]\d+\.\d+$', symbol):
            return type_mapping.get('letter_number_dot_number', 'REQUIREMENT')
            
        # Fallback
        return "REQUIREMENT"
    
    def _extract_title_and_text(self, content, rules):
        """Extrahiert Titel und Text aus dem Inhalt"""
        if ":" in content:
            parts = content.split(":", 1)
            return parts[0].strip(), parts[1].strip()
        
        # Fallback: Heuristik basierend auf Wortanzahl
        words = content.split()
        if len(words) <= 5:
            return content, ""
        
        # Verwende die ersten paar Wörter als Titel
        title = " ".join(words[:5])
        text = " ".join(words[5:])
        
        return title, text
