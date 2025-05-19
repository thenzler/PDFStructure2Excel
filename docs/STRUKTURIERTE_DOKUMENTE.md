# Grundlagen strukturierter Dokumente

## Was sind strukturierte Dokumente?

Strukturierte Dokumente sind Texte, die einem festen hierarchischen Aufbau folgen. Diese Struktur hilft dabei, Informationen zu organisieren, zu navigieren und zu verstehen. Typische Beispiele für strukturierte Dokumente sind:

- **Normen und Standards** (z.B. ISO-Normen)
- **Richtlinien und Qualitätshandbücher** (z.B. Palliative Care Auditkriterien)
- **Gesetzestexte und Verordnungen**
- **Technische Spezifikationen**
- **Handbücher und Dokumentationen**

## Die 5 Grundelemente eines strukturierten Dokuments

Im PDFStructure2Excel-Tool wird jedes strukturierte Dokument in fünf Grundelemente zerlegt:

### 1. Level (Hierarchieebene)

Das Level gibt die hierarchische Ebene eines Elements im Dokument an. Typischerweise wird das Level durch eine Nummer ausgedrückt, wie:

- **1, 2, 3, ...** für Hauptkapitel
- **1.1, 1.2, 1.3, ...** für Unterkapitel
- **1.1.1, 1.1.2, ...** für weitere Untergliederungen

### 2. Symbol (Identifikator)

Das Symbol dient als eindeutiger Identifikator für ein Element. Je nach Dokumenttyp kann dies sein:

- **Buchstaben** (A, B, C, ...)
- **Buchstaben mit Zahlen** (A1, B2, ...)
- **Buchstaben mit hierarchischen Zahlen** (A1.1, B2.3, ...)
- **Nummern** (1, 2, 3, ...)
- **Hierarchische Nummern** (1.1, 1.2, 2.1, ...)
- **Spezielle Kennzeichnungen** (§1, Art.2, ...)

### 3. Type (Elementtyp)

Der Type gibt an, welche Art von Element vorliegt. Im PDFStructure2Excel werden hauptsächlich zwei Typen unterschieden:

- **CHAPTER**: Kapitel oder Abschnitt, enthält üblicherweise weitere Unterelemente
- **REQUIREMENT**: Anforderung oder spezifischer Inhaltspunkt

Der Typ wird in der Regel automatisch erkannt basierend auf dem Symbol und der Hierarchieebene.

### 4. Title_de (Titel)

Der Titel beschreibt kurz den Inhalt des Elements. In vielen Dokumenten wird der Titel vom Text durch einen Doppelpunkt getrennt, beispielsweise:

```
1 A Einleitung: Dies ist der eigentliche Text...
```

Hier ist "Einleitung" der Titel.

### 5. Text_de (Textinhalt)

Der Text enthält die eigentliche Information oder Beschreibung des Elements. Dies ist der Teil nach dem Doppelpunkt im obigen Beispiel.

## Beispiel einer strukturierten Dokumenthierarchie

```
1 A Einleitung: Allgemeine Informationen zum Dokument
  2 B1 Zweck: Beschreibt den Zweck des Dokuments
  2 B2 Anwendungsbereich: Definiert den Geltungsbereich
3 C Definitionen: Wichtige Begriffe und deren Bedeutung
  3 C1 Grundbegriffe: Elementare Konzepte
    3 C1.1 Begriff 1: Definition des ersten Begriffs
    3 C1.2 Begriff 2: Definition des zweiten Begriffs
  3 C2 Spezielle Begriffe: Erweiterte Konzepte
4 D Anforderungen: Konkrete Vorgaben und Richtlinien
  4 D1 Allgemeine Anforderungen: Übergreifende Vorgaben
  4 D2 Spezifische Anforderungen: Detaillierte Vorgaben
    4 D2.1 Anforderung 1: Beschreibung der ersten Anforderung
    4 D2.2 Anforderung 2: Beschreibung der zweiten Anforderung
```

## Vom PDF zur strukturierten Excel-Datei

PDFStructure2Excel erkennt diese strukturierten Dokumente in PDF-Dateien und wandelt sie in ein Excel-Format um:

1. **Extrahieren**: Der Text wird aus dem PDF extrahiert
2. **Erkennen**: Die Strukturelemente werden anhand von regulären Ausdrücken identifiziert
3. **Kategorisieren**: Jedes Element wird in Level, Symbol, Type, Title_de und Text_de aufgeteilt
4. **Exportieren**: Die Elemente werden in eine Excel-Tabelle exportiert

Diese Umwandlung ermöglicht:
- Bessere Übersicht über komplexe Dokumente
- Einfachere Filterung und Sortierung von Inhalten
- Vergleich verschiedener Versionen oder Dokumente
- Weiterverarbeitung der Daten

## Anpassung an verschiedene Dokumenttypen

Verschiedene Dokumenttypen folgen unterschiedlichen Strukturierungsregeln. PDFStructure2Excel bietet daher:

1. **Vordefinierte Vorlagen** für gängige Dokumenttypen
2. **Anpassbare Regeln** für spezielle Anforderungen
3. **Flexible Exportoptionen** für optimale Darstellung

Durch die Anpassung der Erkennungsmuster können auch individuelle Dokumentformate verarbeitet werden.
