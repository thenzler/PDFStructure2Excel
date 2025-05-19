#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF-Verarbeitungsmodul für PDFStructure2Excel

Arbeitsablauf:
1. Text aus PDF extrahieren
2. Text bereinigen und vorverarbeiten
3. Strukturelemente anhand von Kennungen (Level, Symbol, etc.) identifizieren
4. Extrahierte Daten im Format "Level Symbol Type Title_de Text_de" zurückgeben
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
    text_extracted_signal = pyqtSignal(str)  # Neues Signal für extrahierten Text
    
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
        """
        Verarbeitet das PDF und extrahiert strukturierte Daten
        
        Schritte:
        1. Text aus PDF extrahieren
        2. Text bereinigen (Header entfernen, Zeilen zusammenführen)
        3. Struktur anhand von Kennungen erkennen
        4. Daten im Format "Level Symbol Type Title_de Text_de" zurückgeben
        """
        try:
            # SCHRITT 1: Lade Strukturregeln
            self.progress_signal.emit(1)
            if self.structure_type == 'custom' and self.custom_rules:
                rules = self.custom_rules
            else:
                rules = get_structure_rules(self.structure_type)
            
            # SCHRITT 2: Extrahiere Text aus dem PDF
            self.progress_signal.emit(5)
            extracted_text = self._extract_text_from_pdf()
            self.text_extracted_signal.emit(extracted_text)  # Signal mit extrahiertem Text
            
            # SCHRITT 3: Bereinige den Text
            self.progress_signal.emit(40)
            clean_text = self._preprocess_text(extracted_text, rules)
            
            # SCHRITT 4: Erkenne die Struktur anhand der Kennungen (Level, Symbol, etc.)
            self.progress_signal.emit(50)
            structured_data = self._identify_structure_elements(clean_text, rules)
            
            # SCHRITT 5: Sende das Ergebnis
            self.progress_signal.emit(95)
            self.result_signal.emit(structured_data)
            self.progress_signal.emit(100)
            
        except Exception as e:
            self.error_signal.emit(str(e))
    
    def _extract_text_from_pdf(self):
        """
        Schritt 1: Extrahiert den reinen Text aus der PDF-Datei
        
        Returns:
            str: Extrahierter Text aus dem PDF
        """
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            text = ""
            
            for i, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                text += page_text + "\n"
                progress = int(5 + (i + 1) / total_pages * 35)  # 5% bis 40% Fortschritt
                self.progress_signal.emit(progress)
        
        return text
    
    def _preprocess_text(self, text, rules):
        """
        Schritt 2: Bereinigt den Text für die Strukturerkennung
        
        Args:
            text (str): Extrahierter Text aus dem PDF
            rules (dict): Strukturregeln
            
        Returns:
            str: Bereinigter Text
        """
        # A) Entferne Kopf- und Fußzeilen, falls gewünscht
        if rules.get('remove_headers', True):
            text = self._remove_headers(text)
            
        # B) Führe zusammengehörige Zeilen zusammen, falls gewünscht
        if rules.get('merge_lines', True):
            text = self._merge_related_lines(text, rules)
        
        return text
    
    def _identify_structure_elements(self, text, rules):
        """
        Schritt 3: Identifiziert Strukturelemente anhand der Kennungen
        
        Args:
            text (str): Bereinigter Text
            rules (dict): Strukturregeln
            
        Returns:
            list: Liste von Dictionaries im Format "Level Symbol Type Title_de Text_de"
        """
        result = []
        lines = text.split('\n')
        total_lines = max(1, len(lines))
        
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            
            # Fortschritt aktualisieren: 50% bis 95%
            progress = 50 + int((i + 1) / total_lines * 45)
            self.progress_signal.emit(progress)
            
            # Spezialfall: qualité palliative
            if "qualité palliative" in line:
                result.append({
                    "Level": "1",
                    "Symbol": "Q",
                    "Type": "CHAPTER",
                    "Title_de": "qualité palliative SLZP:25",
                    "Text_de": "Auditkriterien stationäre Langzeitpflege mit allgemeiner Palliative Care"
                })
                continue
            
            # Hole die Muster für Level- und Symbol-Erkennung aus den Regeln
            level_pattern = rules.get('level_pattern', r'^\s*(\d+)')
            symbol_pattern = rules.get('symbol_pattern', r'^\s*(?:\d+\s+)?([A-Z](?:\d+(?:\.\d+)*)?)')
            
            # A) Suche nach Level-Kennung
            level_match = re.search(level_pattern, line)
            
            # B) Suche nach Symbol-Kennung
            symbol_match = re.search(symbol_pattern, line)
            
            if level_match and symbol_match:
                # Level und Symbol gefunden - extrahiere die Werte
                level = level_match.group(1)
                symbol = symbol_match.group(1)
                
                # C) Bestimme den Typ basierend auf Level und Symbol
                type_value = self._determine_type(symbol, level, rules)
                
                # D) Extrahiere Titel und Text aus dem Rest der Zeile
                rest_of_line = line[max(level_match.end(), symbol_match.end()):].strip()
                title, text = self._extract_title_and_text(rest_of_line, rules)
                
                # E) Füge das strukturierte Element dem Ergebnis hinzu
                result.append({
                    "Level": level,
                    "Symbol": symbol,
                    "Type": type_value,
                    "Title_de": title,
                    "Text_de": text
                })
        
        return result
    
    def _remove_headers(self, text):
        """
        Entfernt Kopf- und Fußzeilen aus dem Text
        
        Args:
            text (str): Extrahierter Text
            
        Returns:
            str: Text ohne Kopf- und Fußzeilen
        """
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
            
        if re.match(r'^[A-Z]\d+$', symbol):  # Buchstabe gefolgt von Zahl(en) (A1, B2)
            return type_mapping.get('letter_number', 'CHAPTER')
            
        if re.match(r'^[A-Z]\d+\.\d+$', symbol):  # Buchstabe, Zahl, Punkt, Zahl (A1.1, B2.3)
            return type_mapping.get('letter_number_dot_number', 'REQUIREMENT')
            
        if re.match(r'^\d+$', symbol):  # Nur eine Zahl (1, 2, 3)
            return type_mapping.get('single_number', 'CHAPTER')
            
        if re.match(r'^\d+\.\d+$', symbol):  # Zahl, Punkt, Zahl (1.1, 2.3)
            return type_mapping.get('number_dot_number', 'REQUIREMENT')
            
        # Entscheidung basierend auf Level
        if level == "1" or level == "2":
            return "CHAPTER"
            
        # Fallback für alle anderen Fälle
        return "REQUIREMENT"
    
    def _extract_title_and_text(self, content, rules):
        """
        Extrahiert Titel und Text aus dem Inhalt basierend auf den Regeln
        
        Args:
            content (str): Zu analysierender Inhalt
            rules (dict): Strukturregeln
            
        Returns:
            tuple: (Titel, Text)
        """
        # Primäre Methode: Trennung durch Doppelpunkt
        if ":" in content:
            parts = content.split(":", 1)
            return parts[0].strip(), parts[1].strip()
        
        # Sekundäre Methode: Manuelle Trennung
        title_words = rules.get('title_words', 5)  # Standardwert: 5 Wörter für Titel
        words = content.split()
        
        if len(words) <= title_words:
            return content, ""
        
        # Verwende die ersten X Wörter als Titel
        title = " ".join(words[:title_words])
        text = " ".join(words[title_words:])
        
        return title, text
