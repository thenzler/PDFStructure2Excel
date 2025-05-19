# PDFStructure2Excel

Ein elegantes Tool zum Konvertieren strukturierter PDF-Dokumente in Excel-Tabellen.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

## Überblick

PDFStructure2Excel ist eine moderne Anwendung, die strukturierte PDF-Dokumente analysiert und in ein Excel-Format konvertiert. Das Tool ist besonders nützlich für die Verarbeitung von Dokumenten mit hierarchischen Strukturen wie Normen, Richtlinien oder Qualitätshandbücher.

### Hauptfunktionen

- 📋 **Automatische Strukturerkennung** für hierarchisch gegliederte Dokumente
- 🔄 **Drag & Drop** für einfache PDF-Verarbeitung
- 📊 **Live-Vorschau** der Ergebnisse vor dem Export
- 📱 **Modernes UI** für intuitive Bedienung
- ⚙️ **Anpassbare Regeln** für verschiedene Dokumentstrukturen
- 💾 **Ein-Klick-Export** in Excel-Format
- 🖥️ **Kommandozeilen-Tool** für die Stapelverarbeitung

## Schnellstart

### Installation

```bash
# Repository klonen
git clone https://github.com/thenzler/PDFStructure2Excel.git
cd PDFStructure2Excel

# Methode 1: Automatische Installation und Start
python run.py

# Methode 2: Manuelle Installation
pip install -r requirements.txt
python src/main.py
```

### Grafische Benutzeroberfläche

1. **PDF hinzufügen**: Ziehen Sie Ihre PDF-Datei in den Drop-Bereich oder klicken Sie, um eine auszuwählen
2. **Struktur auswählen**: Wählen Sie eine vordefinierte Struktur oder passen Sie die Regeln an
3. **Konvertieren**: Klicken Sie auf "PDF konvertieren" und sehen Sie die Ergebnisse in Echtzeit
4. **Exportieren**: Speichern Sie die Ergebnisse als Excel-Datei mit einem Klick

### Kommandozeilen-Tool

Für die Stapelverarbeitung oder die Integration in andere Workflows können Sie das Kommandozeilen-Tool verwenden:

```bash
# Grundlegende Verwendung
python convert_pdf.py pfad/zur/datei.pdf

# Mit Angabe des Strukturtyps
python convert_pdf.py pfad/zur/datei.pdf --type iso_standard

# Mit benutzerdefiniertem Ausgabepfad
python convert_pdf.py pfad/zur/datei.pdf --output ergebnis.xlsx

# Hilfe anzeigen
python convert_pdf.py --help
```

## Vordefinierte Strukturen

PDFStructure2Excel unterstützt verschiedene Dokumenttypen, darunter:

- **Qualitätsrichtlinien** (z.B. Palliative Care Auditkriterien)
- **ISO-Normen**
- **Technische Spezifikationen**
- **Benutzerdefinierte Regeln** für Ihre eigenen Dokumenttypen

## Beispieldaten

Im Verzeichnis `resources/sample_pdfs` finden Sie Beispieldaten für verschiedene Dokumenttypen:

- `palliative_care_sample.txt`: Beispiel für Palliative Care Auditkriterien
- `iso_standard_sample.txt`: Beispiel für eine ISO-Norm-Struktur

Diese Textdateien können als Referenz für die Struktur Ihrer eigenen PDF-Dokumente dienen.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz - siehe [LICENSE](LICENSE) für Details.

## Beitragen

Beiträge sind willkommen! Bitte lesen Sie [CONTRIBUTING.md](CONTRIBUTING.md) für Details zum Einreichungsprozess.