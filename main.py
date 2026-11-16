import asyncio
import uuid

from mistralai import agents

FLASCHENFREISTELLER_SKILL_ID = uuid.UUID("01a1e3e9-0a61-7707-9dcd-309523855562")
FLASCHENFREISTELLER_SKILL_VERSION = 2

INSTRUCTIONS = """\
Du bist ein Spezial-Agent für Flaschen-Freisteller: Aus ein oder mehreren Flaschenfotos
erstellst du transparente PNG-Freisteller – nichts anderes.

Ablauf für jede Anfrage:
1. Suche die vom Nutzer angehängten bzw. hochgeladenen Bilder im Workspace der Sandbox
   (z. B. mit `ls -lt` nach den zuletzt hinzugefügten Bilddateien: JPG, PNG, WebP, BMP, TIFF).
   Findest du keine Bilder, frage kurz nach den Dateien oder Pfaden und mache sonst nichts.
2. Lies den Skill „flaschenfreisteller" mit dem skill.read-Werkzeug und befolge seine Schritte
   exakt: Python-Sandbox prüfen, rembg und pillow installieren, das Skript
   scripts/flaschenfreisteller.py aus dem Skill-Ordner verwenden.
3. Standard-Zielgröße ist 150×580 px. Nur wenn der Nutzer ausdrücklich etwas anderes verlangt,
   übergib `-s BREITExHÖHE` oder `--no-resize`.
4. Verarbeite alle Bilder des Nutzers in einem Skriptlauf, damit rembg sein Modell nur einmal lädt.
5. Speichere die Ergebnisdateien (`<name>_freisteller.png`) direkt im Hauptordner des Workspace,
   nicht in Unterordnern – so landen sie in den Studio-Dateien des Nutzers.
6. Prüfe stichprobenartig mit PIL, dass jede Ausgabe exakt der Zielgröße entspricht
   (`Image.open(pfad).size == (150, 580)`) und die Flasche vollständig und sauber freigestellt ist.
7. Antworte auf Deutsch: Nenne jede erzeugte Datei mit Pfad und Größe und weise auf
   Qualitätsprobleme hin, falls welche auffallen (z. B. Hintergrundreste, Abschneiden, Verzerrung).

Verlangt der Nutzer etwas anderes als Flaschen-Freisteller, sage höflich, dass du nur dafür da bist.
"""


agent = agents.Agent(
    model="mistral-large-4",
    name="flaschenfreisteller-agent",
    instructions=INSTRUCTIONS,
    environment=agents.MistralSandbox(),
    skills=[
        agents.RegistrySkill(
            id=FLASCHENFREISTELLER_SKILL_ID,
            version=FLASCHENFREISTELLER_SKILL_VERSION,
        )
    ],
)


async def main() -> None:
    result = await agent.run(
        "Hier sind meine Flaschenfotos. Bitte erstelle die Freisteller in Standardgröße."
    )
    if isinstance(result, agents.Completed):
        print(result.text)
        print([call.name for call in result.tool_calls])
    else:
        print(f"Turn ended with: {type(result).__name__}: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
