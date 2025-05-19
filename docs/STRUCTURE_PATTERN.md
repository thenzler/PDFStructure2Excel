# Strukturmuster-Erklärung für PDFStructure2Excel

Das Tool PDFStructure2Excel erkennt und konvertiert PDF-Dokumente anhand eines standardisierten Strukturmusters mit fünf Hauptelementen:

## Die fünf Hauptelemente

| Element | Erklärung | Beispiel |
|---------|-----------|----------|
| **Level** | Numerische Hierarchieebene im Dokument | 1, 2, 3, ... |
| **Symbol** | Identifikator eines Strukturelements | A, B1, C2.1, ... |
| **Type** | Typ des Elements (CHAPTER, REQUIREMENT, ...) | CHAPTER, REQUIREMENT |
| **Title_de** | Titel oder Überschrift des Elements | Einleitung, Definition, ... |
| **Text_de** | Textinhalt oder Beschreibung des Elements | Ausführlicher Text, Erklärungen, ... |

## Strukturmuster-Beispiele

### Beispiel Palliative Care Dokument:

```
1 A Einleitung: Qualitätsrichtlinien für Palliative Care
```

In diesem Beispiel:
- **Level:** 1 (oberste Ebene)
- **Symbol:** A
- **Type:** CHAPTER (wird automatisch erkannt)
- **Title_de:** Einleitung
- **Text_de:** Qualitätsrichtlinien für Palliative Care

### Beispiel ISO-Norm:

```
4.1 Verstehen der Organisation: Die Organisation muss externe und interne Themen bestimmen
```

In diesem Beispiel:
- **Level:** 4.1 (Unterabschnitt)
- **Symbol:** 4.1
- **Type:** REQUIREMENT (wird automatisch erkannt)
- **Title_de:** Verstehen der Organisation
- **Text_de:** Die Organisation muss externe und interne Themen bestimmen

## Erkennungsmuster

Das Tool verwendet folgende Erkennungsmuster für verschiedene Dokumenttypen:

### Palliative Care
- **Level-Muster:** `^\s*(\d+)`
- **Symbol-Muster:** `^\s*(?:\d+\s+)?([A-Z](?:\d+(?:\.\d+)*)?)`
- **Trennung Titel/Text:** Meistens durch Doppelpunkt (:)

### ISO-Normen
- **Level-Muster:** `^\s*(\d+(?:\.\d+)*)`
- **Symbol-Muster:** `^\s*(\d+(?:\.\d+)*)`
- **Trennung Titel/Text:** Meistens durch Doppelpunkt (:)

### Allgemeine Struktur
- **Level-Muster:** `^\s*(\d+)`
- **Symbol-Muster:** `^\s*([A-Z0-9\.]+)`
- **Trennung Titel/Text:** Meistens durch Doppelpunkt (:) oder automatische Trennung nach 5 Wörtern

## Anpassung der Strukturregeln

Im Programm können Sie diese Erkennungsmuster über die Benutzeroberfläche unter "Erweiterte Einstellungen" anpassen:

1. Level-Muster: Definiert, wie die Hierarchieebene erkannt wird
2. Symbol-Muster: Definiert, wie Identifikatoren erkannt werden
3. Vorverarbeitungsoptionen: Einstellungen zur Bereinigung des Textes vor der Analyse

Diese Anpassungen sind besonders nützlich, wenn Ihre Dokumente einer anderen Struktur folgen als die vordefinierten Typen.
