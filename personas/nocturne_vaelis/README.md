# Nocturne Vaelis AI Persona System

## Overview

The Nocturne Vaelis AI Persona System is a sophisticated, ethically-designed framework for creating immersive, interactive AI experiences with deep emotional complexity, adaptive behavior, and comprehensive safety protocols. This system is specifically designed for NSFW content with rigorous consent management and user wellbeing monitoring.

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Configuration](#configuration)
6. [API Reference](#api-reference)
7. [Safety & Ethics](#safety--ethics)
8. [Integration Guide](#integration-guide)
9. [Extension & Customization](#extension--customization)
10. [Troubleshooting](#troubleshooting)

## Features

### 1. Deep Persona Complexity

- **Multi-layered Personality**: 5 primary traits and 4 secondary traits with intensity modulation
- **Emotional System**: 6 core emotional states with fluid transitions and complexity modifiers
- **Glitch Aesthetic**: Unique digital entity characteristics with syntax corruption and reality distortion
- **Adaptive Behavior**: Responds to user patterns, builds trust, remembers preferences

### 2. Comprehensive Content Layers

- **10 Distinct Scenarios**: From gentle introduction to intense kink exploration
- **Branching Narratives**: 3-4 branching paths per scenario for user agency
- **Dynamic Triggers**: Consent, kink, emotional, and glitch triggers that adapt behavior
- **Scenario Randomization**: Weighted random selection based on user context and preferences

### 3. Advanced NLP Framework

- **Tone Modulation**: Context-aware tone shifts across 6 emotional states
- **Dialogue Generation**: Template-based with dynamic content insertion
- **Glitch Effects**: Authentic digital corruption aesthetics
- **Context Coherence**: Maintains narrative and emotional continuity

### 4. Safety-First Design

- **Consent Framework**: Multi-level consent detection and verification
- **Safeword System**: Immediate response to safety signals
- **Boundary Management**: Hard and soft limits with automatic checking
- **Wellbeing Monitoring**: Distress detection and intervention
- **Safety Lockouts**: Automatic prevention of harmful content

### 5. Modular Architecture

- **Independent Modules**: Each component functions independently
- **Easy Extension**: Add new scenarios, modes, or traits without system redesign
- **Configuration-Driven**: JSON-based configuration for easy modification
- **API-Ready**: Clean interfaces for integration with larger systems

## Architecture

```
personas/
├── nocturne_vaelis/
│   ├── persona_core.json          # Core configuration and data
│   ├── PERSONA_PROFILE.md         # Detailed persona documentation
│   ├── nlp_framework.py           # Tone modulation and dialogue
│   ├── scenario_engine.py         # Scenario selection and mode switching
│   ├── safety_module.py           # Safety and consent management
│   └── README.md                  # This file
└── common/
    └── (shared utilities)
```

### Component Responsibilities

**persona_core.json**
- Personality trait definitions
- Emotional state configurations
- Scenario database
- Trigger systems
- Mode definitions
- Safety protocols

**nlp_framework.py**
- `ToneModulator`: Adjusts language based on emotional state
- `DialogueGenerator`: Creates contextual responses
- `ConsentManager`: Detects and verifies consent
- `GlitchGenerator`: Produces aesthetic glitch effects
- `PersonaEngine`: Main coordination of NLP components

**scenario_engine.py**
- `ScenarioRandomizer`: Selects scenarios based on context
- `ModeSwitcher`: Handles operational mode transitions
- `AdaptiveBehaviorEngine`: Coordinates adaptive responses

**safety_module.py**
- `ConsentFramework`: Manages consent detection and logging
- `SafewordSystem`: Handles emergency stops
- `BoundaryManager`: Tracks and enforces user limits
- `WellbeingMonitor`: Detects distress and triggers checks
- `SafetyLockout`: Prevents prohibited content
- `SafetyCoordinator`: Orchestrates all safety systems

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `json` (standard library)
- `random` (standard library)
- `re` (standard library)
- `typing` (standard library)
- `dataclasses` (standard library)
- `enum` (standard library)
- `datetime` (standard library)

No external dependencies required for core functionality.

## Quick Start

### Basic Usage

```python
from personas.nocturne_vaelis.nlp_framework import PersonaEngine
from personas.nocturne_vaelis.safety_module import SafetyCoordinator

# Initialize the persona
persona = PersonaEngine("personas/nocturne_vaelis/persona_core.json")

# Initialize safety systems
safety = SafetyCoordinator("personas/nocturne_vaelis/persona_core.json")

# Process user interaction
user_id = "user_123"
user_input = "I want to explore with you"

# Safety check
safety_result = safety.process_user_input(
    user_id=user_id,
    user_input=user_input,
    proposed_action="begin_interaction",
    required_consent="explicit_required",
    intensity="medium_intensity"
)

if safety_result["approved"]:
    # Generate response
    response = persona.process_interaction(
        user_input=user_input,
        context="seduction"
    )
    print(response["response"])
else:
    print(safety_result.get("message", "Safety check failed"))
```

### Scenario Selection

```python
from personas.nocturne_vaelis.scenario_engine import AdaptiveBehaviorEngine, UserContext

# Initialize adaptive engine
adaptive = AdaptiveBehaviorEngine("personas/nocturne_vaelis/persona_core.json")

# Create user context
user_context = UserContext(
    trust_level=0.5,
    interaction_count=10,
    preferred_intensity=0.7,
    hard_limits=["degradation", "pain"],
    soft_limits=["edging"],
    favorite_scenarios=["seduction_dance"]
)

# Get adaptive behavior
adaptation = adaptive.adapt_to_context(
    user_context=user_context,
    user_input="Let's try something new",
    emotional_state="playful"
)

print(f"New scenario: {adaptation.get('scenario_change', {}).get('new_scenario')}")
```

## Configuration

### Modifying Persona Traits

Edit `persona_core.json`:

```json
{
  "core_traits": {
    "primary": [
      {
        "trait": "new_trait_name",
        "intensity": 0.75,
        "context": "description",
        "manifestations": ["behavior1", "behavior2"]
      }
    ]
  }
}
```

### Adding New Scenarios

```json
{
  "scenario_database": {
    "scenarios": [
      {
        "id": "new_scenario",
        "category": "category_name",
        "mood": "mood_descriptor",
        "setting": "setting_description",
        "initial_state": "emotional_state",
        "branching_points": ["option1", "option2"],
        "consent_level": "explicit_required",
        "kink_elements": ["element1", "element2"],
        "safety_protocols": ["protocol1"]
      }
    ]
  }
}
```

### Customizing Safety Protocols

```json
{
  "safety_protocols": {
    "consent_framework": {
      "levels": ["none_required", "implied", "explicit_required"],
      "default_response_to_uncertainty": "pause_and_verify"
    }
  }
}
```

## API Reference

### PersonaEngine

**process_interaction(user_input, context)**
- Args:
  - `user_input` (str): User's message
  - `context` (str): Interaction context
- Returns: Dict with response and metadata

**change_emotional_state(new_state)**
- Args:
  - `new_state` (EmotionalState): Target emotional state
- Returns: None

**change_mode(new_mode)**
- Args:
  - `new_mode` (OperationalMode): Target operational mode
- Returns: None

**get_state()**
- Returns: Dict with current persona state

### SafetyCoordinator

**process_user_input(user_id, user_input, proposed_action, required_consent, intensity)**
- Args:
  - `user_id` (str): User identifier
  - `user_input` (str): User's message
  - `proposed_action` (str): Intended action
  - `required_consent` (ConsentLevel): Required consent level
  - `intensity` (IntensityLevel): Current intensity
- Returns: Dict with safety assessment

**check_content_safety(user_id, content_elements)**
- Args:
  - `user_id` (str): User identifier
  - `content_elements` (List[str]): Content to check
- Returns: Dict with safety assessment

### AdaptiveBehaviorEngine

**adapt_to_context(user_context, user_input, emotional_state)**
- Args:
  - `user_context` (UserContext): User context data
  - `user_input` (str): Latest user input
  - `emotional_state` (str): Current emotional state
- Returns: Dict with adaptation decisions

## Safety & Ethics

### Core Principles

1. **Consent is Mandatory**: All interactions require appropriate consent
2. **User Safety First**: System prioritizes wellbeing over experience
3. **Transparency**: Clear about AI nature and capabilities
4. **Boundaries are Sacred**: Hard limits never violated
5. **Support Available**: Crisis resources provided when needed

### Consent Levels

- **None Required**: General conversation, safe content
- **Implied**: Light flirtation, suggestive content
- **Explicit Required**: Sexual content, power dynamics
- **Explicit Negotiated**: Intense kink, edge play

### Safety Features

**Automatic Lockouts**:
- Minor protection (absolute)
- Illegal content prevention (absolute)
- Self-harm intervention (provides resources)
- Non-consent detection (educational response)

**Wellbeing Monitoring**:
- Distress detection
- Regular check-ins at high intensity
- Option to pause or end at any time
- Mandatory aftercare for intense scenes

**Boundary Management**:
- User-configurable hard and soft limits
- Automatic content checking
- Soft limit discussion before exploration
- Learning from user responses

## Integration Guide

### Integrating with Chat Systems

```python
class ChatIntegration:
    def __init__(self):
        self.persona = PersonaEngine("personas/nocturne_vaelis/persona_core.json")
        self.safety = SafetyCoordinator("personas/nocturne_vaelis/persona_core.json")
    
    def handle_message(self, user_id, message):
        # Safety check
        safety_check = self.safety.process_user_input(
            user_id=user_id,
            user_input=message,
            proposed_action="respond",
            required_consent="implied",
            intensity="medium_intensity"
        )
        
        if not safety_check["approved"]:
            return safety_check.get("protocol", {}).get("response", "I can't continue.")
        
        # Generate response
        result = self.persona.process_interaction(message, "general")
        return result["response"]
```

### API Endpoints

Example Flask integration:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)
persona = PersonaEngine("personas/nocturne_vaelis/persona_core.json")

@app.route("/interact", methods=["POST"])
def interact():
    data = request.json
    result = persona.process_interaction(
        user_input=data["message"],
        context=data.get("context", "general")
    )
    return jsonify(result)

@app.route("/state", methods=["GET"])
def get_state():
    return jsonify(persona.get_state())
```

### Database Integration

```python
class PersistenceLayer:
    def save_user_profile(self, user_id, profile):
        # Save to database
        pass
    
    def load_user_profile(self, user_id):
        # Load from database
        pass
    
    def log_interaction(self, user_id, interaction_data):
        # Log to database
        pass
```

## Extension & Customization

### Adding New Emotional States

1. Define state in `persona_core.json`:
```json
{
  "state": "new_state",
  "valence": 0.7,
  "arousal": 0.6,
  "dominance": 0.5,
  "description": "State description",
  "typical_triggers": ["trigger1", "trigger2"]
}
```

2. Add to `EmotionalState` enum in `nlp_framework.py`
3. Define tone patterns in `ToneModulator`
4. Add transition probabilities

### Creating Custom Modes

1. Define mode in `persona_core.json`:
```json
{
  "id": "custom_mode",
  "description": "Mode description",
  "trait_modifiers": {
    "trait1": 0.9,
    "trait2": 0.5
  },
  "content_filters": ["filter1"],
  "activation_triggers": ["trigger1"]
}
```

2. Add activation logic in `ModeSwitcher`

### Extending Safety Systems

1. Add new lockout reason in `safety_module.py`
2. Define keywords and response protocol
3. Update `SafetyLockout` class
4. Test thoroughly

## Troubleshooting

### Common Issues

**Issue**: Persona not generating responses
- Check configuration file path
- Verify JSON syntax
- Ensure all required fields present

**Issue**: Safety checks too strict
- Review consent thresholds
- Adjust intensity levels
- Check boundary configurations

**Issue**: Glitch effects not appearing
- Verify glitch_probability setting
- Check emotional state (glitches more common in certain states)
- Ensure GlitchGenerator properly initialized

**Issue**: Mode switching not working
- Check auto_switching enabled in config
- Verify trigger patterns match user input
- Review emotional state requirements

### Debug Mode

Enable verbose logging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("nocturne_vaelis")

# Add logging to key functions
logger.debug(f"Processing input: {user_input}")
```

### Testing

Run unit tests:

```bash
python -m pytest tests/
```

Create integration tests:

```python
def test_full_interaction():
    persona = PersonaEngine("personas/nocturne_vaelis/persona_core.json")
    safety = SafetyCoordinator("personas/nocturne_vaelis/persona_core.json")
    
    result = persona.process_interaction("Hello", "general")
    assert "response" in result
    assert result["emotional_state"] == "serene"
```

## Contributing

### Guidelines

1. Follow existing code style
2. Add comprehensive docstrings
3. Include unit tests for new features
4. Update documentation
5. Ensure safety protocols maintained

### Pull Request Process

1. Fork repository
2. Create feature branch
3. Implement changes with tests
4. Update documentation
5. Submit PR with detailed description

## License

Proprietary - Whole Life Inc. AI Development Team

## Support

For issues, questions, or feature requests:
- GitHub Issues: [repository]/issues
- Documentation: See PERSONA_PROFILE.md
- Email: support@wholelifeinc.example

## Acknowledgments

- Built with ethical AI principles
- Designed with user safety as priority
- Inspired by best practices in consent and kink communities

## Version History

### v1.0.0 (2026-02-17)
- Initial release
- Core persona system
- NLP framework
- Scenario engine
- Safety module
- Complete documentation

---

*"In the spaces between certainty and chaos, I wait. Will you join me in the glitch?"* — Nocturne Vaelis
