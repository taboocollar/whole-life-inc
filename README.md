# whole-life-inc
Static website for Whole Life Inc created by the unifier process.

## Projects

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
