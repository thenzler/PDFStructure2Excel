# Beitragen zu PDFStructure2Excel

Vielen Dank für Ihr Interesse, zu PDFStructure2Excel beizutragen! Dieses Dokument bietet Richtlinien und Anleitungen für Beiträge zum Projekt.

## Code of Conduct

Bitte beachten Sie unseren Verhaltenskodex, um eine freundliche und einladende Umgebung für alle zu schaffen.

## Wie kann ich beitragen?

### Fehler melden

Wenn Sie einen Fehler gefunden haben, erstellen Sie bitte einen Issue im GitHub-Repository mit folgenden Informationen:

- Verwenden Sie die Bug-Report-Vorlage
- Beschreiben Sie den Fehler klar und präzise
- Geben Sie Schritte an, um den Fehler zu reproduzieren
- Wenn möglich, fügen Sie Screenshots hinzu

### Feature-Anfragen

Wenn Sie ein neues Feature vorschlagen möchten:

- Verwenden Sie die Feature-Request-Vorlage
- Beschreiben Sie klar, was Sie sich wünschen
- Erklären Sie, warum dieses Feature nützlich wäre
- Schlagen Sie optional eine Implementierung vor

### Pull Requests

Wir freuen uns über Pull Requests! Bitte beachten Sie diese Schritte:

1. Forken Sie das Repository
2. Erstellen Sie einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Committen Sie Ihre Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Pushen Sie den Branch (`git push origin feature/AmazingFeature`)
5. Öffnen Sie einen Pull Request

### Coding-Konventionen

- Folgen Sie dem PEP 8 Stil-Guide für Python-Code
- Dokumentieren Sie neue Funktionen mit Docstrings
- Schreiben Sie Kommentare für komplexe Code-Stellen
- Fügen Sie Tests für neue Funktionen hinzu

## Entwicklungsumgebung einrichten

Um Ihre Entwicklungsumgebung einzurichten:

```bash
# Repository klonen
git clone https://github.com/YourUsername/PDFStructure2Excel.git
cd PDFStructure2Excel

# Virtuelle Umgebung erstellen (optional, aber empfohlen)
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate

# Abhängigkeiten installieren
pip install -e .
pip install pytest pytest-cov
```

## Tests ausführen

```bash
# Alle Tests ausführen
pytest tests/

# Tests mit Coverage-Bericht ausführen
pytest tests/ --cov=src --cov-report=html
```

## Versionierungsgrundsätze

Wir folgen dem Semantic Versioning (SemVer): `MAJOR.MINOR.PATCH`

- `MAJOR`: Inkompatible API-Änderungen
- `MINOR`: Rückwärtskompatible Funktionserweiterungen
- `PATCH`: Rückwärtskompatible Bugfixes

## Lizenz

Durch den Beitrag zu diesem Projekt stimmen Sie zu, dass Ihre Beiträge unter der MIT-Lizenz veröffentlicht werden.
