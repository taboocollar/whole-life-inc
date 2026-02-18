# whole-life-inc
Static website for Whole Life Inc created by the unifier process.

## Projects

### Nocturne Vaelis AI Persona System

An advanced AI persona system featuring deep emotional complexity, adaptive behavior, and comprehensive safety protocols for immersive interactive experiences.

**Two Implementations Available:**

#### 1. Simple Demo Implementation (NEW - v2.0.0)
A lightweight, configuration-driven demo perfect for getting started or simple integrations.
- **Demo Script:** [nocturne_demo.py](nocturne_demo.py)
- **Configuration:** [personas/nocturne_vaelis.json](personas/nocturne_vaelis.json)
- **Documentation:** [NOCTURNE_VAELIS.md](NOCTURNE_VAELIS.md)
- **Examples:** [personas/nocturne_vaelis_examples.md](personas/nocturne_vaelis_examples.md)
- **Quick Start:**
  ```python
  from nocturne_demo import NocturneVaelis
  
  nocturne = NocturneVaelis()
  nocturne.user_familiarity = 'established_user'
  nocturne.conversation_context = 'creative'
  
  greeting = nocturne.greet()
  print(greeting)
  ```

#### 2. Full Production Implementation (v1.0)
A comprehensive, modular system for production deployments with advanced features.
- **Directory:** [personas/nocturne_vaelis/](personas/nocturne_vaelis/)
- **Documentation:** [personas/nocturne_vaelis/README.md](personas/nocturne_vaelis/README.md)
- **Features:**
  - Multi-layered personality with 9 distinct traits
  - 6 emotional states with fluid transitions
  - 10 distinct interaction scenarios with branching narratives
  - Advanced NLP framework with tone modulation
  - Comprehensive safety and consent management
  - Modular, extensible architecture
- **Quick Start:**
  ```python
  from personas.nocturne_vaelis.integration_example import NocturneVaelisSession
  
  session = NocturneVaelisSession(user_id="your_user_id")
  result = session.send_message("Hello", "general")
  print(result["response"])
  ```

**Choose Your Implementation:**
- Use the **Simple Demo** (v2.0.0) for: Quick prototypes, learning, simple chatbots
- Use the **Full Production** (v1.0) for: Enterprise deployments, complex interactions, full safety requirements

For complete documentation on both implementations, see [personas/README.md](personas/README.md).

## Notion Integration

This repository includes a Python script for integrating with Notion databases. See [NOTION_INTEGRATION.md](NOTION_INTEGRATION.md) for detailed setup and usage instructions.

### Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Configure your `.env` file with Notion credentials
3. Run the script: `python notion_integration.py`
