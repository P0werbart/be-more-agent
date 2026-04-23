# Star Trek Computer Agent — Project Context

This is a Raspberry Pi AI agent being converted from a BMO (Adventure Time) theme to a Star Trek LCARS computer theme.

## Project Structure
- agent.py — main Python script (core logic, GUI, audio)
- config.json — configuration (models, persona, hardware)
- personas/ — persona JSON files
- faces/ — PNG animation frames per state (idle, listening, thinking, speaking, error, warmup)
- sounds/ — WAV sound effects per category
- generate_lcars.py — LCARS image generator (create if not exists)

## Conversion Rules
- Wake word: change from "alexa" to "computer" (OpenWakeWord model)
- Persona: Star Trek computer — formal, precise, Starfleet style
- GUI: LCARS aesthetic — black background, orange/blue/purple panels
- Language: German (DE)
- Do NOT remove: Ollama, Whisper, Piper TTS, DuckDuckGo search
- Do NOT add cloud APIs
- Keep all existing functionality, only change theme and persona
