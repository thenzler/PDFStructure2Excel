#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Definiert Strukturregeln für verschiedene Dokumenttypen
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
            'level_pattern': r'^\s*(\d+)',
            'symbol_pattern': r'^\s*(?:\d+\s+)?([A-Z](?:\d+(?:\.\d+)*)?)',
            'title_pattern': r'([^:]+)(?::|$)',
            'text_pattern': r'(?::\s*)?(.+)$',
            'remove_headers': True,
            'merge_lines': True,
            'type_mapping': {
                'single_letter': 'CHAPTER',        # z.B. A, B, C
                'letter_number': 'CHAPTER',        # z.B. A1, B2
                'letter_number_dot_number': 'REQUIREMENT'  # z.B. A1.1, B2.3
            }
        },
        
        # Regeln für ISO-Normen
        'iso_standard': {
            'level_pattern': r'^\s*(\d+(?:\.\d+)*)',
            'symbol_pattern': r'^\s*(\d+(?:\.\d+)*)',
            'title_pattern': r'([^:]+)(?::|$)',
            'text_pattern': r'(?::\s*)?(.+)$',
            'remove_headers': True,
            'merge_lines': True,
            'type_mapping': {
                'single_number': 'CHAPTER',        # z.B. 1, 2, 3
                'number_dot_number': 'REQUIREMENT' # z.B. 1.1, 2.3
            }
        },
        
        # Allgemeine Regeln
        'general': {
            'level_pattern': r'^\s*(\d+)',
            'symbol_pattern': r'^\s*([A-Z0-9\.]+)',
            'title_pattern': r'([^:]+)(?::|$)',
            'text_pattern': r'(?::\s*)?(.+)$',
            'remove_headers': True,
            'merge_lines': True
        }
    }
    
    return rules.get(structure_type, rules['general'])
