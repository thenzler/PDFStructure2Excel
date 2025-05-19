#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests für die Strukturregeln
"""

import unittest
from src.structure_rules import get_structure_rules

class TestStructureRules(unittest.TestCase):
    """Testfälle für die Strukturregeln"""
    
    def test_palliative_care_rules(self):
        """Test der Regeln für Palliative Care Dokumente"""
        rules = get_structure_rules("palliative_care")
        
        # Überprüfe, ob alle erwarteten Schlüssel vorhanden sind
        expected_keys = [
            'level_pattern', 'symbol_pattern', 'title_pattern', 'text_pattern',
            'remove_headers', 'merge_lines', 'type_mapping'
        ]
        for key in expected_keys:
            self.assertIn(key, rules)
        
        # Überprüfe spezifische Werte
        self.assertEqual(rules['level_pattern'], r'^\s*(\d+)')
        self.assertEqual(rules['symbol_pattern'], r'^\s*(?:\d+\s+)?([A-Z](?:\d+(?:\.\d+)*)?)')
        self.assertTrue(rules['remove_headers'])
        self.assertTrue(rules['merge_lines'])
        
        # Überprüfe Type-Mapping
        type_mapping = rules['type_mapping']
        self.assertEqual(type_mapping['single_letter'], 'CHAPTER')
        self.assertEqual(type_mapping['letter_number'], 'CHAPTER')
        self.assertEqual(type_mapping['letter_number_dot_number'], 'REQUIREMENT')
    
    def test_iso_standard_rules(self):
        """Test der Regeln für ISO-Normen"""
        rules = get_structure_rules("iso_standard")
        
        # Überprüfe, ob alle erwarteten Schlüssel vorhanden sind
        expected_keys = [
            'level_pattern', 'symbol_pattern', 'title_pattern', 'text_pattern',
            'remove_headers', 'merge_lines', 'type_mapping'
        ]
        for key in expected_keys:
            self.assertIn(key, rules)
        
        # Überprüfe spezifische Werte
        self.assertEqual(rules['level_pattern'], r'^\s*(\d+(?:\.\d+)*)')
        self.assertEqual(rules['symbol_pattern'], r'^\s*(\d+(?:\.\d+)*)')
        self.assertTrue(rules['remove_headers'])
        self.assertTrue(rules['merge_lines'])
        
        # Überprüfe Type-Mapping
        type_mapping = rules['type_mapping']
        self.assertEqual(type_mapping['single_number'], 'CHAPTER')
        self.assertEqual(type_mapping['number_dot_number'], 'REQUIREMENT')
    
    def test_general_rules(self):
        """Test der allgemeinen Regeln"""
        rules = get_structure_rules("general")
        
        # Überprüfe, ob alle erwarteten Schlüssel vorhanden sind
        expected_keys = [
            'level_pattern', 'symbol_pattern', 'title_pattern', 'text_pattern',
            'remove_headers', 'merge_lines'
        ]
        for key in expected_keys:
            self.assertIn(key, rules)
        
        # Überprüfe spezifische Werte
        self.assertEqual(rules['level_pattern'], r'^\s*(\d+)')
        self.assertEqual(rules['symbol_pattern'], r'^\s*([A-Z0-9\.]+)')
        self.assertTrue(rules['remove_headers'])
        self.assertTrue(rules['merge_lines'])
    
    def test_unknown_rule_type(self):
        """Test für unbekannten Regeltyp (sollte auf general zurückfallen)"""
        rules = get_structure_rules("unknown_type")
        
        # Sollte die allgemeinen Regeln zurückgeben
        self.assertEqual(rules['level_pattern'], r'^\s*(\d+)')
        self.assertEqual(rules['symbol_pattern'], r'^\s*([A-Z0-9\.]+)')


if __name__ == "__main__":
    unittest.main()
