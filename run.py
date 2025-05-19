#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Start-Skript für PDFStructure2Excel
"""

import os
import sys
import subprocess
import platform

def main():
    """Startet das Programm und installiert fehlende Abhängigkeiten"""
    
    # Prüfe Python-Version
    if sys.version_info < (3, 7):
        print("Fehler: Python 3.7 oder höher wird benötigt")
        sys.exit(1)
    
    # Stelle sicher, dass das Skript aus dem richtigen Verzeichnis aufgerufen wird
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(script_dir) != "PDFStructure2Excel":
        print("Bitte starten Sie das Skript aus dem PDFStructure2Excel-Verzeichnis")
        sys.exit(1)
    
    # Installiere Abhängigkeiten
    try:
        print("Überprüfe und installiere Abhängigkeiten...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError:
        print("Fehler bei der Installation der Abhängigkeiten")
        sys.exit(1)
    
    # Starte das Programm
    try:
        print("Starte PDFStructure2Excel...")
        os.environ["PYTHONPATH"] = script_dir
        
        if platform.system() == "Windows":
            subprocess.check_call([sys.executable, os.path.join("src", "main.py")])
        else:
            subprocess.check_call([sys.executable, os.path.join("src", "main.py")])
    except subprocess.CalledProcessError:
        print("Fehler beim Starten des Programms")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nProgramm beendet")

if __name__ == "__main__":
    main()
