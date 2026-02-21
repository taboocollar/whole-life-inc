# whole-life-inc
Static website for Whole Life Inc created by the unifier process.

## Projects

### Video Computer Analyzer

A tool that reads short videos (≤60 seconds) containing computers, uses
**OpenAI Vision (GPT-4o)** to identify hardware specs of every machine visible
in the footage, and produces a structured evaluation report covering:

- Current specs of each computer
- Whether each machine meets your stated workload requirements
- Itemised upgrade plan with estimated USD cost ranges
- Future-proofing score and overall buy/upgrade/replace recommendation

The server exposes a REST API that can be registered as a **ChatGPT custom action**,
letting you ask ChatGPT to evaluate your computers directly from a short video.

See [video_analyzer/README.md](video_analyzer/README.md) for full documentation.

**Quick Start:**
```bash
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."
uvicorn video_analyzer.server:app --reload --port 8000
# Then POST a video to http://localhost:8000/analyze-video
```

**ChatGPT Integration:**
Upload [`video_analyzer/chatgpt_tool_schema.json`](video_analyzer/chatgpt_tool_schema.json)
as a custom action in GPT Builder (after deploying the server publicly).

---

### Nocturne Vaelis AI Persona System

An advanced AI persona system featuring deep emotional complexity, adaptive behavior, and comprehensive safety protocols for immersive interactive experiences. See [personas/nocturne_vaelis/README.md](personas/nocturne_vaelis/README.md) for complete documentation.

**Key Features:**
- Multi-layered personality with 9 distinct traits
- 6 emotional states with fluid transitions
- 10 distinct interaction scenarios with branching narratives
- Advanced NLP framework with tone modulation
- Comprehensive safety and consent management
- Modular, extensible architecture

**Quick Start:**
```python
from personas.nocturne_vaelis.integration_example import NocturneVaelisSession

session = NocturneVaelisSession(user_id="your_user_id")
result = session.send_message("Hello", "general")
print(result["response"])
```

See [personas/nocturne_vaelis/PERSONA_PROFILE.md](personas/nocturne_vaelis/PERSONA_PROFILE.md) for detailed persona documentation.

## Notion Integration

This repository includes a Python script for integrating with Notion databases. See [NOTION_INTEGRATION.md](NOTION_INTEGRATION.md) for detailed setup and usage instructions.

### Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Configure your `.env` file with Notion credentials
3. Run the script: `python notion_integration.py`
