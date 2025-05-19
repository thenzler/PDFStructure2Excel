#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Definiert Strukturregeln für verschiedene Dokumenttypen

Die Strukturregeln legen fest, wie Dokumente im Format "Level Symbol Type Title_de Text_de"
erkannt und konvertiert werden.
"""

def get_structure_rules(structure_type):
    """
    Gibt die Strukturregeln für den angegebenen Dokumenttyp zurück
    
    Args:
        structure_type (str): Typ des Dokuments
        
    Returns:
        dict: Regeln für die Struktur
    """
    rules = {
        # Regeln für Palliative Care Dokumente
        'palliative_care': {
            # Erkennungsmuster für die einzelnen Strukturelemente
            'level_pattern': r'^\s*(\d+)',  # Erkennt Level-Nummern: 1, 2, 3, ...
            'symbol_pattern': r'^\s*(?:\d+\s+)?([A-Z](?:\d+(?:\.\d+)*)?)',  # Erkennt Symbole: A, B1, C2.1, ...
            'title_pattern': r'([^:]+)(?::|$)',  # Erkennt Titel: Text vor Doppelpunkt
            'text_pattern': r'(?::\s*)?(.+)$',  # Erkennt Text: Text nach Doppelpunkt
            
            # Vorverarbeitungsoptionen
            'remove_headers': True,  # Kopf- und Fußzeilen entfernen
            'merge_lines': True,  # Zusammengehörige Zeilen zusammenführen
            
            # Wörter für Titel, wenn kein Doppelpunkt gefunden wird
            'title_words': 5,  # Anzahl der Wörter für Titel
            
            # Zuordnung von Symbol-Mustern zu Typen
            'type_mapping': {
                'single_letter': 'CHAPTER',        # z.B. A, B, C
                'letter_number': 'CHAPTER',        # z.B. A1, B2
                'letter_number_dot_number': 'REQUIREMENT'  # z.B. A1.1, B2.3
            },
            
            # Beispieltext zur Veranschaulichung
            'example': """
1 A Einleitung: Qualitätsrichtlinien für Palliative Care
2 B1 Definition: Palliative Care ist ein Ansatz...
3 C2.1 Anforderung: Systematische Erfassung von Symptomen
"""
        },
        
        # Regeln für ISO-Normen
        'iso_standard': {
            # Erkennungsmuster für die einzelnen Strukturelemente
            'level_pattern': r'^\s*(\d+(?:\.\d+)*)',  # Erkennt Level-Nummern: 1, 1.1, 1.1.1, ...
            'symbol_pattern': r'^\s*(\d+(?:\.\d+)*)',  # Erkennt Symbole: 1, 1.1, 1.1.1, ...
            'title_pattern': r'([^:]+)(?::|$)',  # Erkennt Titel: Text vor Doppelpunkt
            'text_pattern': r'(?::\s*)?(.+)$',  # Erkennt Text: Text nach Doppelpunkt
            
            # Vorverarbeitungsoptionen
            'remove_headers': True,  # Kopf- und Fußzeilen entfernen
            'merge_lines': True,  # Zusammengehörige Zeilen zusammenführen
            
            # Wörter für Titel, wenn kein Doppelpunkt gefunden wird
            'title_words': 5,  # Anzahl der Wörter für Titel
            
            # Zuordnung von Symbol-Mustern zu Typen
            'type_mapping': {
                'single_number': 'CHAPTER',        # z.B. 1, 2, 3
                'number_dot_number': 'REQUIREMENT' # z.B. 1.1, 2.3
            },
            
            # Beispieltext zur Veranschaulichung
            'example': """
1 Anwendungsbereich
4.1 Verstehen der Organisation: Die Organisation muss...
5.2 Politik: Die oberste Leitung muss...
"""
        },
        
        # Allgemeine Regeln
        'general': {
            # Erkennungsmuster für die einzelnen Strukturelemente
            'level_pattern': r'^\s*(\d+)',  # Erkennt Level-Nummern: 1, 2, 3, ...
            'symbol_pattern': r'^\s*([A-Z0-9\.]+)',  # Erkennt Symbole: A, 1, A1, B.2, ...
            'title_pattern': r'([^:]+)(?::|$)',  # Erkennt Titel: Text vor Doppelpunkt
            'text_pattern': r'(?::\s*)?(.+)$',  # Erkennt Text: Text nach Doppelpunkt
            
            # Vorverarbeitungsoptionen
            'remove_headers': True,  # Kopf- und Fußzeilen entfernen
            'merge_lines': True,  # Zusammengehörige Zeilen zusammenführen
            
            # Wörter für Titel, wenn kein Doppelpunkt gefunden wird
            'title_words': 5,  # Anzahl der Wörter für Titel
            
            # Zuordnung von Symbol-Mustern zu Typen
            'type_mapping': {
                'single_letter': 'CHAPTER',  # z.B. A, B, C
                'single_number': 'CHAPTER',  # z.B. 1, 2, 3
                'letter_number': 'CHAPTER',  # z.B. A1, B2
                'number_dot_number': 'REQUIREMENT',  # z.B. 1.1, 2.3
                'letter_number_dot_number': 'REQUIREMENT'  # z.B. A1.1, B2.3
            },
            
            # Beispieltext zur Veranschaulichung
            'example': """
1 TEIL1 Einführung in das Thema
2 KAP2 Wichtige Grundlagen zum Verständnis
3 ABS3.1 Unterabschnitt mit Details
"""
        }
    }
    
    return rules.get(structure_type, rules['general'])
