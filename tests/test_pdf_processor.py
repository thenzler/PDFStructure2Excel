#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests für die PDF-Verarbeitungsfunktionen
"""

import unittest
import os
import tempfile
from unittest.mock import MagicMock, patch

# Importiere die zu testenden Module
from src.pdf_processor import PDFProcessWorker
from src.structure_rules import get_structure_rules

class TestPDFProcessor(unittest.TestCase):
    """Testfälle für den PDF-Prozessor"""
    
    def setUp(self):
        """Testumgebung vorbereiten"""
        # Erstelle temporäre Testdatei
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_pdf_path = os.path.join(self.temp_dir.name, "test.pdf")
        
        # Mock für PyQt-Signale
        self.progress_signal_mock = MagicMock()
        self.result_signal_mock = MagicMock()
        self.error_signal_mock = MagicMock()
    
    def tearDown(self):
        """Testumgebung aufräumen"""
        self.temp_dir.cleanup()
    
    @patch('PyPDF2.PdfReader')
    def test_pdf_extraction_basic(self, mock_pdf_reader):
        """Test der grundlegenden PDF-Textextraktion"""
        # Mock für PDF-Reader konfigurieren
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "1 A Test-Titel: Dies ist ein Testinhalt"
        mock_pdf_reader.return_value.pages = [mock_page]
        
        # Worker erstellen und run-Methode direkt aufrufen (nicht als Thread)
        worker = PDFProcessWorker(self.test_pdf_path, "palliative_care")
        worker.progress_signal = self.progress_signal_mock
        worker.result_signal = self.result_signal_mock
        worker.error_signal = self.error_signal_mock
        
        # run-Methode ausführen
        worker.run()
        
        # Überprüfen, ob die Signale korrekt aufgerufen wurden
        self.progress_signal_mock.emit.assert_any_call(50)  # Erster Fortschritt nach Textextraktion
        self.result_signal_mock.emit.assert_called_once()  # Ergebnis wurde gesendet
        self.error_signal_mock.emit.assert_not_called()  # Kein Fehler aufgetreten
        
        # Überprüfen der extrahierten Daten
        result = self.result_signal_mock.emit.call_args[0][0]
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)  # Eine Zeile extrahiert
        
        item = result[0]
        self.assertEqual(item.get("Level"), "1")
        self.assertEqual(item.get("Symbol"), "A")
        self.assertEqual(item.get("Type"), "CHAPTER")
        self.assertEqual(item.get("Title_de"), "Test-Titel")
        self.assertEqual(item.get("Text_de"), "Dies ist ein Testinhalt")

    def test_determine_type(self):
        """Test der Typbestimmung basierend auf Symbolen"""
        worker = PDFProcessWorker(self.test_pdf_path, "palliative_care")
        
        # Teste verschiedene Symboltypen
        self.assertEqual(worker._determine_type("A", {}), "CHAPTER")
        self.assertEqual(worker._determine_type("A1", {}), "CHAPTER")
        self.assertEqual(worker._determine_type("A12", {}), "REQUIREMENT")
        self.assertEqual(worker._determine_type("A1.1", {}), "REQUIREMENT")
        
    def test_extract_title_and_text(self):
        """Test der Titel- und Textextraktion"""
        worker = PDFProcessWorker(self.test_pdf_path, "palliative_care")
        
        # Test mit Doppelpunkt als Trenner
        title, text = worker._extract_title_and_text("Testtitel: Dies ist der Inhalt", {})
        self.assertEqual(title, "Testtitel")
        self.assertEqual(text, "Dies ist der Inhalt")
        
        # Test ohne Doppelpunkt, kurzer Text
        title, text = worker._extract_title_and_text("Kurzer Titel ohne Inhalt", {})
        self.assertEqual(title, "Kurzer Titel ohne Inhalt")
        self.assertEqual(text, "")
        
        # Test ohne Doppelpunkt, langer Text
        title, text = worker._extract_title_and_text("Dies ist ein langer Titel der über fünf Wörter hinausgeht und eigentlich zu lang ist", {})
        self.assertEqual(title, "Dies ist ein langer Titel")
        self.assertEqual(text, "der über fünf Wörter hinausgeht und eigentlich zu lang ist")


if __name__ == "__main__":
    unittest.main()
