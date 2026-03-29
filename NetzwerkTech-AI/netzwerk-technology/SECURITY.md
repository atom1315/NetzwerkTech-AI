# Sicherheitsrichtlinie

## Unterstützte Versionen

| Version | Unterstützt |
|---------|:-----------:|
| 2.0.x   | ✅          |
| 1.0.x   | ⚠️ nur kritische Fixes |
| < 1.0   | ❌          |

## Sicherheitspraktiken

- Alle Abhängigkeiten werden regelmäßig mit `pip-audit` geprüft
- Dependabot ist für automatische Updates aktiviert
- Container-Images werden mit Trivy gescannt
- API-Endpunkte erfordern Authentifizierung (JWT)
- Daten werden in Transit (TLS 1.3) und at Rest (AES-256) verschlüsselt
