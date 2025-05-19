#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kommandozeilen-Tool für PDFStructure2Excel
"""

import os
import sys
import argparse
import pandas as pd

# Notwendig, um Module aus dem src-Verzeichnis zu importieren
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.insert(0, project_dir)

from src.pdf_processor import PDFProcessWorker
from src.structure_rules import get_structure_rules

class FakeSignal:
    """Fake-Signal für die Verwendung mit PDFProcessWorker ohne PyQt"""
    
    def __init__(self):
        self.value = None
    
    def emit(self, value):
        """Emittiert ein Signal (speichert den Wert)"""
        self.value = value
        
        # Bei Progress-Signal Fortschritt anzeigen
        if hasattr(self, 'progress_bar') and self.progress_bar:
            sys.stdout.write(f"\rFortschritt: {value}%")
            sys.stdout.flush()

def convert_pdf(pdf_path, structure_type, output_path=None):
    """
    Konvertiert ein PDF zu Excel
    
    Args:
        pdf_path (str): Pfad zur PDF-Datei
        structure_type (str): Typ der Struktur (palliative_care, iso_standard, ...)
        output_path (str, optional): Pfad zur Ausgabedatei. Defaults to None.
    
    Returns:
        bool: True bei Erfolg, False bei Fehler
    """
    if not os.path.exists(pdf_path):
        print(f"Fehler: PDF-Datei {pdf_path} nicht gefunden")
        return False
    
    # Worker erstellen
    worker = PDFProcessWorker(pdf_path, structure_type)
    
    # Fake-Signale erstellen
    progress_signal = FakeSignal()
    progress_signal.progress_bar = True
    result_signal = FakeSignal()
    error_signal = FakeSignal()
    
    # Signale zuweisen
    worker.progress_signal = progress_signal
    worker.result_signal = result_signal
    worker.error_signal = error_signal
    
    # Worker ausführen
    print(f"Konvertiere {pdf_path} mit Struktur {structure_type}...")
    worker.run()
    
    # Ergebnis überprüfen
    if error_signal.value:
        print(f"\nFehler bei der Konvertierung: {error_signal.value}")
        return False
    
    if not result_signal.value:
        print("\nKeine Daten extrahiert")
        return False
    
    # Excel-Datei erstellen
    if not output_path:
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = f"{base_name}_converted.xlsx"
    
    try:
        df = pd.DataFrame(result_signal.value)
        df.to_excel(output_path, index=False)
        print(f"\nErfolgreich konvertiert und gespeichert als {output_path}")
        return True
    except Exception as e:
        print(f"\nFehler beim Speichern der Excel-Datei: {str(e)}")
        return False

def main():
    """Hauptfunktion des Kommandozeilen-Tools"""
    parser = argparse.ArgumentParser(description='Konvertiert strukturierte PDF-Dokumente in Excel')
    parser.add_argument('pdf_path', help='Pfad zur PDF-Datei')
    parser.add_argument('--type', '-t', choices=['palliative_care', 'iso_standard', 'general'],
                        default='palliative_care', help='Typ der Dokumentstruktur')
    parser.add_argument('--output', '-o', help='Pfad zur Ausgabedatei (optional)')
    
    args = parser.parse_args()
    
    convert_pdf(args.pdf_path, args.type, args.output)

if __name__ == "__main__":
    main()
