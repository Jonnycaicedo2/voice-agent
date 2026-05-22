# Voice Agent — Conversational Voice Agent in pure Python

A minimal real-time conversational voice agent built from scratch with **Python 3.10+** and **asyncio**, designed to deeply understand the architecture behind frameworks like Pipecat and LiveKit Agents.

## Overview

This project implements a complete voice pipeline — from microphone capture to LLM processing to audio playback — without relying on external agent frameworks. The goal is educational: learn how each stage works by building it yourself.

```
Microphone → STT → LLM → TTS → Speaker
```

## Features

- **Real-time audio capture** via microphone using asyncio
- **Speech-to-Text** transcription
- **LLM-based response generation**
- **Text-to-Speech** synthesis
- **Audio playback** through speaker
- **Web UI** to start/stop conversations, view real-time transcripts, and monitor pipeline status

## Project Structure

```
src/
├── backend/
│   ├── audio/          # Audio capture and playback
│   ├── stt/            # Speech-to-Text
│   ├── llm/            # LLM processing
│   ├── tts/            # Text-to-Speech
│   └── pipeline/       # Pipeline orchestrator
├── frontend/           # Web UI
│   └── static/
tests/                  # Test suite
```

## Requirements

- Python 3.10 or higher
- See `pyproject.toml` for dependencies

## Installation

```bash
git clone <repo-url>
cd voice-agent
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -e .
```

## Usage

```bash
python src/backend/main.py
```

Open the web UI at `http://localhost:8000` (or the configured port).

## License

## Development Workflow: Running Your AFK Agent

This project follows the **AFK Agent** workflow described in [Running Your AFK Agent](https://your-article-link). 
The goal is to offload implementation work to an AI agent (OpenCode/Claude Code) and review its output as a senior engineer.

### The Workflow

1. **Spec-first**: Before any code, we write a detailed spec (`CLIENT_BRIEF.md`) defining what to build
2. **Atomic Issues**: Break the spec into self-contained, individually testable GitHub Issues
3. **TDD Loop**: The agent runs a `Red → Green → Refactor` cycle for each issue
4. **Human QA at the Seam**: After each issue, we review the agent's code for complexity leaks, shallow modules, and coupling before merging
5. **Continuous Cleanup**: Run `/improve-codebase-architecture` every 2-3 issues to keep the codebase deep and maintainable
6. **Handoff**: Use `/handoff` to summarize context and avoid token rot between sessions

### How We Execute

```bash
# Each issue is implemented autonomously by the agent
./ralph/once.sh <issue-id>

# After 2-3 issues, we audit the architecture
/improve-codebase-architecture

# Between sessions, we clean the context
/handoff

MIT
