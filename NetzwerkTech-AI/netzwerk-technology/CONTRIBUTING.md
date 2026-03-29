# 🤝 Beitragen zu NetzwerkTech AI

Vielen Dank für dein Interesse an NetzwerkTech AI! Wir freuen uns über jeden Beitrag.

## 🚀 Schnellstart für Entwickler

### 1. Repository forken & klonen

```bash
git clone https://github.com/atom1315/NetzwerkTech-AI
cd netzwerk-ai
```

### 2. Entwicklungsumgebung einrichten

```bash
# Virtual Environment erstellen
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Abhängigkeiten installieren
pip install -e ".[dev]"

# Optional: GPU-Support
pip install -e ".[all]"
```

### 3. Tests ausführen

```bash
pytest tests/ -v --cov=src
```

### 4. Code-Qualität prüfen

```bash
ruff check src/ tests/
mypy src/
```

## 📋 Beitragsrichtlinien

### Branching-Strategie

- `main` — stabiler Release-Branch
- `develop` — Integrations-Branch
- `feature/*` — neue Features
- `fix/*` — Bugfixes
- `docs/*` — Dokumentation

### Commit-Konventionen

Wir verwenden [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: Neues Feature hinzugefügt
fix: Bug in der Anomalie-Erkennung behoben
docs: README aktualisiert
test: Tests für TopologyMapper ergänzt
refactor: Code-Optimierung im Encoder
perf: Inference-Geschwindigkeit verbessert
ci: GitHub Actions Workflow aktualisiert
```

### Code-Style

- **Python**: PEP 8, enforced durch `ruff`
- **Type Hints**: Pflicht für alle öffentlichen Funktionen
- **Docstrings**: NumPy-Style für alle Module, Klassen und Funktionen
- **Tests**: Mindestens 80% Coverage für neue Features

### Pull Request Prozess

1. Feature-Branch von `develop` erstellen
2. Änderungen implementieren und testen
3. PR gegen `develop` öffnen
4. Code-Review abwarten (mindestens 1 Approval)
5. CI/CD Pipeline muss grün sein
6. Squash & Merge

## 🐛 Bugs melden

Nutze die [Issue-Templates](https://github.com/netzwerk-tech/netzwerk-ai/issues/new/choose) und füge bitte hinzu:

- Betriebssystem und Python-Version
- Reproduzierbare Schritte
- Erwartetes vs. tatsächliches Verhalten
- Log-Ausgaben (falls vorhanden)

## 💡 Feature-Vorschläge

Öffne ein Issue mit dem Label `enhancement` und beschreibe:

- **Problem**: Was soll gelöst werden?
- **Lösung**: Wie könnte es aussehen?
- **Alternativen**: Welche anderen Ansätze gibt es?

## 📜 Verhaltenskodex

Wir erwarten von allen Beteiligten einen respektvollen und professionellen Umgang.
Diskriminierung, Belästigung und toxisches Verhalten werden nicht toleriert.

---

Vielen Dank, dass du NetzwerkTech AI besser machst! 🎉
