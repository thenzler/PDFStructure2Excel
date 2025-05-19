# PDFStructure2Excel

Ein elegantes Tool zum Konvertieren strukturierter PDF-Dokumente in Excel-Tabellen im Format "Level Symbol Type Title_de Text_de".

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

## Überblick

PDFStructure2Excel ist eine moderne Anwendung, die strukturierte PDF-Dokumente analysiert und in ein Excel-Format konvertiert. Das Tool extrahiert die 5 Grundelemente der Struktur (Level, Symbol, Type, Title_de, Text_de) und ist besonders nützlich für die Verarbeitung von Dokumenten wie Normen, Richtlinien oder Qualitätshandbücher.

### Hauptfunktionen

- 📋 **Automatische Strukturerkennung** für hierarchisch gegliederte Dokumente
- 🔄 **Drag & Drop** für einfache PDF-Verarbeitung
- 📊 **Live-Vorschau** der Ergebnisse vor dem Export
- 📱 **Modernes UI** mit klarer Darstellung des Strukturmusters
- ⚙️ **Anpassbare Regeln** für verschiedene Dokumentstrukturen
- 💾 **Formatierter Excel-Export** mit automatischer Hierarchie-Darstellung
- 🖥️ **Kommandozeilen-Tool** für die Stapelverarbeitung

## Das Strukturmuster: Level Symbol Type Title_de Text_de

PDFStructure2Excel verwendet ein einheitliches 5-Spalten-Format, um strukturierte Dokumente zu repräsentieren:

1. **Level:** Hierarchieebene im Dokument (z.B. 1, 2, 3, ...)
2. **Symbol:** Identifikator eines Elements (z.B. A, B1, C2.1, ...)
3. **Type:** Art des Elements (CHAPTER, REQUIREMENT, ...)
4. **Title_de:** Titel oder Überschrift
5. **Text_de:** Textinhalt oder Beschreibung

Weitere Informationen zu diesem Strukturmuster finden Sie in der [Dokumentation zu strukturierten Dokumenten](docs/STRUKTURIERTE_DOKUMENTE.md).

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
4. **Exportieren**: Speichern Sie die Ergebnisse als formatierte Excel-Datei mit einem Klick

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

- **Palliative Care - Auditkriterien** (z.B. "1 A Einleitung: Qualitätsrichtlinien...")
- **ISO-Normen** (z.B. "4.1 Verstehen der Organisation: Die Organisation muss...")
- **Allgemeine Strukturen** (z.B. "1 TEIL1 Einführung in das Thema...")
- **Benutzerdefinierte Regeln** für Ihre eigenen Dokumenttypen

Für jede Struktur gibt es dokumentierte Erkennungsmuster, die angepasst werden können. Weitere Details finden Sie im [Strukturmuster-Dokument](docs/STRUCTURE_PATTERN.md).

## Beispieldaten

Im Verzeichnis `resources/sample_pdfs` finden Sie Beispieldaten für verschiedene Dokumenttypen:

- `palliative_care_sample.txt`: Beispiel für Palliative Care Auditkriterien
- `iso_standard_sample.txt`: Beispiel für eine ISO-Norm-Struktur

Diese Textdateien können als Referenz für die Struktur Ihrer eigenen PDF-Dokumente dienen.

## Dokumentation

- [Struktur-Muster Erklärung](docs/STRUCTURE_PATTERN.md): Detaillierte Erklärung des "Level Symbol Type Title_de Text_de" Formats
- [Grundlagen strukturierter Dokumente](docs/STRUKTURIERTE_DOKUMENTE.md): Einführung in hierarchisch strukturierte Dokumente
- [Beitrags-Richtlinien](CONTRIBUTING.md): Anleitung für Entwickler, die zum Projekt beitragen möchten

## Anwendungsbeispiele

PDFStructure2Excel ist besonders nützlich für:

- **Qualitätsmanager**: Extraktion und Vergleich von Normen und Richtlinien
- **Auditoren**: Strukturierte Aufbereitung von Auditkriterien
- **Dokumentenmanager**: Konvertierung von hierarchischen PDF-Dokumenten in bearbeitbare Formate
- **Projektleiter**: Extraktion von Anforderungen aus strukturierten Spezifikationen
- **Compliance-Beauftragte**: Vergleich und Abgleich von Regelwerken

## Excel-Ausgabe

Die Ausgabe in Excel erfolgt in zwei Formaten:

1. **Standard Excel**: Einfache tabellarische Darstellung mit den 5 Spalten
2. **Formatiertes Excel**: Verbesserte Darstellung mit:
   - Hierarchischer Formatierung (Schriftgröße und Fettdruck)
   - Farbkodierung für verschiedene Elementtypen
   - Automatischer Spaltenbreitenanpassung
   - Filter- und Sortierfunktionalität

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz - siehe [LICENSE](LICENSE) für Details.

## Beitragen

Beiträge sind willkommen! Bitte lesen Sie [CONTRIBUTING.md](CONTRIBUTING.md) für Details zum Einreichungsprozess.
