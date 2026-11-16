# flaschenfreisteller-agent

Agent, der aus ein oder mehreren Flaschenfotos transparente PNG-Freisteller erstellt – gebaut
mit dem [Mistral Agents SDK](https://docs.mistral.ai/studio/agents/). Der Agent liegt in `main.py`
und verwendet den Studio-Skill **flaschenfreisteller** (Registry-Version 2, rembg/ISNet,
Standard-Zielgröße 150×580 px). Die Ergebnisdateien (`<name>_freisteller.png`) werden im
Workspace-Hauptordner abgelegt und erscheinen damit in den Studio-Dateien.

## Voraussetzungen

- `MISTRAL_API_KEY` in `.env` (Seite [API keys](https://console.mistral.ai/api-keys) im Studio),
  sofern `agents init` nicht bereits gesetzt. `.env` ist git-ignored: niemals committen.
- Für die Sandbox `MistralSandbox`: die Workspace-Rolle **cloud_user** (Mistral Cloud User)
  für den Schlüssel-Inhaber bzw. das Deployment-Service-Konto.
- Der Skill `flaschenfreisteller` muss für den Workspace geteilt sein, sonst sieht ein
  deployter Agent ihn nicht (Studio: Skill → Sharing → Workspace).

## Nutzung

```bash
uv run --env-file .env agents info     # zeigt Entrypoint und Capabilities
uv run --env-file .env agents chat     # Agent im Terminal chatten (Bilder in den Workspace legen)
uv run --env-file .env agents serve    # dauerhafter Worker (self-hosted)
uv run --env-file .env agents deploy   # Managed Deployment über Studio
```

`agents deploy` baut den gepushten Commit: Das Projekt muss in einem GitHub-Repository liegen und
der GitHub Connector muss im Mistral-Konto aktiviert sein.

## Ablauf im Agenten

1. Bilder des Nutzers im Workspace finden (keine Bilder vorhanden → nachfragen).
2. Skill `flaschenfreisteller` per `skill.read` laden und befolgen (rembg + pillow, Skript aus dem Skill-Ordner).
3. Alle Bilder in einem Lauf verarbeiten; Zielgröße 150×580 px, abweichend nur auf ausdrücklichen Wunsch.
4. Ergebnisse als `<name>_freisteller.png` direkt im Workspace-Hauptordner speichern und mit PIL gegenprüfen.
