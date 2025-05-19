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
                text = self._merge_related_lines(text, rules)
            
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
    
    def _merge_related_lines(self, text, rules):
        """
        Führt zusammengehörige Zeilen zusammen
        
        Args:
            text (str): Zu verarbeitender Text
            rules (dict): Strukturregeln mit regulären Ausdrücken
            
        Returns:
            str: Text mit zusammengeführten Zeilen
        """
        result = []
        lines = text.split('\n')
        i = 0
        
        # Verwende das Strukturmuster aus den Regeln als Erkennungsmerklmal für neue Einträge
        level_pattern = rules.get('level_pattern', r'^\s*(\d+)')
        symbol_pattern = rules.get('symbol_pattern', r'^\s*(?:\d+\s+)?([A-Z](?:\d+(?:\.\d+)*)?)')
        
        # Kombiniertes Muster zur Erkennung neuer Strukturelemente
        structure_pattern = f"({level_pattern}.*?{symbol_pattern})"
        
        while i < len(lines):
            if not lines[i].strip():
                i += 1
                continue
                
            current_line = lines[i]
            i += 1
            
            # Wenn die nächste Zeile nicht mit einem Strukturelement beginnt,
            # füge sie zur aktuellen Zeile hinzu
            while i < len(lines) and lines[i].strip() and not re.search(structure_pattern, lines[i]):
                current_line += " " + lines[i].strip()
                i += 1
                
            result.append(current_line)
            
        return '\n'.join(result)
    
    def _extract_structure(self, text, rules):
        """
        Extrahiert strukturierte Daten aus dem Text basierend auf den Regeln
        
        Args:
            text (str): Zu analysierender Text
            rules (dict): Strukturregeln
            
        Returns:
            list: Liste von Dictionaries mit den strukturierten Daten (Level, Symbol, Type, Title_de, Text_de)
        """
        result = []
        lines = text.split('\n')
        
        # Fortschritt initialisieren
        total_lines = max(1, len(lines))
        
        for i, line in enumerate(lines):
            if not line.strip():
                continue
                
            # Fortschritt aktualisieren
            self.progress_signal.emit(50 + int((i + 1) / total_lines * 50))
            
            # Spezielle Behandlung für die erste Zeile mit "qualité palliative"
            if "qualité palliative" in line:
                result.append({
                    "Level": "1",
                    "Symbol": "Q",  # Besser erkennbares Symbol
                    "Type": "CHAPTER",
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
                level = level_match.group(1)
                symbol = symbol_match.group(1)
                type_value = self._determine_type(symbol, level, rules)
                
                # Extrahiere Titel und Text
                rest_of_line = line[max(level_match.end(), symbol_match.end()):].strip()
                title, text = self._extract_title_and_text(rest_of_line, rules)
                
                result.append({
                    "Level": level,
                    "Symbol": symbol,
                    "Type": type_value,
                    "Title_de": title,
                    "Text_de": text
                })
        
        return result
    
    def _determine_type(self, symbol, level, rules):
        """
        Bestimmt den Typ basierend auf dem Symbol, Level und den Regeln
        
        Args:
            symbol (str): Symbol des Elements (A, B1, C2.1, ...)
            level (str): Level des Elements (1, 2, 3, ...)
            rules (dict): Strukturregeln
            
        Returns:
            str: Typ des Elements (CHAPTER, REQUIREMENT, ...)
        """
        # Type-Mapping aus den Regeln
        type_mapping = rules.get('type_mapping', {})
        
        # Prüfe auf bekannte Muster
        if len(symbol) == 1 and symbol.isalpha():  # Einzelner Buchstabe (A, B, C)
            return type_mapping.get('single_letter', 'CHAPTER')
            
        if re.match(r'^[A-Z]\d+$', symbol):  # Buchstabe + Zahl (A1, B2)
            return type_mapping.get('letter_number', 'CHAPTER')
            
        if re.match(r'^[A-Z]\d+\.\d+$', symbol):  # Buchstabe + Zahl + Punkt + Zahl (A1.1, B2.3)
            return type_mapping.get('letter_number_dot_number', 'REQUIREMENT')
            
        if symbol.isdigit():  # Reine Zahl (1, 2, 3)
            return type_mapping.get('single_number', 'CHAPTER')
            
        if re.match(r'^\d+\.\d+$', symbol):  # Zahl + Punkt + Zahl (1.1, 2.3)
            return type_mapping.get('number_dot_number', 'REQUIREMENT')
        
        # Basierend auf Level entscheiden
        if int(level) <= 2:  # Annahme: Niedriges Level = Kapitel
            return 'CHAPTER'
        else:
            return 'REQUIREMENT'
    
    def _extract_title_and_text(self, content, rules):
        """
        Extrahiert Titel und Text aus dem Inhalt
        
        Args:
            content (str): Inhalt nach Entfernung von Level und Symbol
            rules (dict): Strukturregeln
            
        Returns:
            tuple: (title, text) Titel und Text des Elements
        """
        # Verwende Muster aus den Regeln, falls vorhanden
        title_pattern = rules.get('title_pattern')
        text_pattern = rules.get('text_pattern')
        
        # Verwende Doppelpunkt als Standardtrenner
        if ":" in content:
            parts = content.split(":", 1)
            return parts[0].strip(), parts[1].strip()
        
        # Versuche, die Muster anzuwenden, falls vorhanden
        if title_pattern and text_pattern:
            title_match = re.search(title_pattern, content)
            text_match = re.search(text_pattern, content)
            
            if title_match and text_match:
                return title_match.group(1).strip(), text_match.group(1).strip()
        
        # Fallback: Heuristik basierend auf Wortanzahl
        words = content.split()
        
        # Wenn wenige Wörter, wahrscheinlich ein Titel ohne Text
        if len(words) <= 5:
            return content, ""
        
        # Andernfalls: Ersten paar Wörter als Titel, Rest als Text
        title_word_count = min(5, len(words) // 3 + 2)  # Dynamisch basierend auf Gesamtwortanzahl
        title = " ".join(words[:title_word_count])
        text = " ".join(words[title_word_count:])
        
        return title, text
