# Nocturne Vaelis API Documentation

## Table of Contents

1. [Overview](#overview)
2. [Core Modules](#core-modules)
3. [API Reference](#api-reference)
4. [Integration Patterns](#integration-patterns)
5. [Examples](#examples)
6. [Error Handling](#error-handling)

## Overview

The Nocturne Vaelis AI Persona System provides a comprehensive API for creating immersive, emotionally complex interactive experiences. The system is built with a modular architecture consisting of four main components:

- **NLP Framework**: Tone modulation, dialogue generation, consent management
- **Scenario Engine**: Scenario selection, mode switching, adaptive behavior
- **Safety Module**: Consent verification, boundary management, wellbeing monitoring
- **Integration Layer**: Session management, simplified API access

## Core Modules

### Module: nlp_framework

**Purpose**: Natural language processing, dialogue generation, and tone modulation.

**Classes**:
- `PersonaEngine`: Main coordinator for NLP components
- `ToneModulator`: Adjusts language tone based on emotional state
- `DialogueGenerator`: Creates contextual responses
- `ConsentManager`: Detects and verifies consent
- `GlitchGenerator`: Produces aesthetic glitch effects

### Module: scenario_engine

**Purpose**: Dynamic scenario selection and adaptive mode switching.

**Classes**:
- `AdaptiveBehaviorEngine`: Coordinates adaptive responses
- `ScenarioRandomizer`: Selects scenarios based on context
- `ModeSwitcher`: Handles operational mode transitions

### Module: safety_module

**Purpose**: Comprehensive safety and consent management.

**Classes**:
- `SafetyCoordinator`: Orchestrates all safety systems
- `ConsentFramework`: Manages consent detection and logging
- `SafewordSystem`: Handles emergency stops
- `BoundaryManager`: Tracks and enforces user limits
- `WellbeingMonitor`: Detects distress and triggers checks
- `SafetyLockout`: Prevents prohibited content

### Module: integration_example

**Purpose**: Simplified integration interface.

**Classes**:
- `NocturneVaelisSession`: Complete session management

## API Reference

### PersonaEngine

Main engine for the Nocturne Vaelis persona.

#### Constructor

```python
PersonaEngine(config_path: str)
```

**Parameters**:
- `config_path` (str): Path to `persona_core.json` configuration file

**Example**:
```python
engine = PersonaEngine("personas/nocturne_vaelis/persona_core.json")
```

#### Methods

##### process_interaction

```python
process_interaction(user_input: str, context: str = "general") -> Dict[str, Any]
```

Process a user interaction and generate a response.

**Parameters**:
- `user_input` (str): The user's message
- `context` (str, optional): Interaction context. Default: "general"
  - Valid contexts: "general", "seduction", "command", "dominant", "edge_play", "degradation"

**Returns**:
```python
{
    "response": str,           # Generated response
    "emotional_state": str,    # Current emotional state
    "consent_level": str,      # Detected consent level
    "confidence": float,       # Confidence in consent detection (0.0-1.0)
    "action": str             # Recommended action ("continue" or "immediate_stop")
}
```

**Example**:
```python
result = engine.process_interaction("I want to explore with you", "seduction")
print(result["response"])  # Nocturne's response
print(result["emotional_state"])  # e.g., "aroused"
```

##### change_emotional_state

```python
change_emotional_state(new_state: EmotionalState) -> None
```

Change the persona's emotional state.

**Parameters**:
- `new_state` (EmotionalState): Target emotional state
  - Options: `SERENE`, `AROUSED`, `MELANCHOLIC`, `PLAYFUL`, `COMMANDING`, `GLITCHING`

**Example**:
```python
from personas.nocturne_vaelis.nlp_framework import EmotionalState
engine.change_emotional_state(EmotionalState.PLAYFUL)
```

##### change_mode

```python
change_mode(new_mode: OperationalMode) -> None
```

Change the persona's operational mode.

**Parameters**:
- `new_mode` (OperationalMode): Target operational mode
  - Options: `STANDARD`, `DOMINANT`, `NURTURING`, `SADISTIC`, `GLITCH`, `INTIMATE`

**Example**:
```python
from personas.nocturne_vaelis.nlp_framework import OperationalMode
engine.change_mode(OperationalMode.DOMINANT)
```

##### get_state

```python
get_state() -> Dict[str, Any]
```

Get current persona state.

**Returns**:
```python
{
    "emotional_state": str,      # Current emotional state
    "operational_mode": str,     # Current mode
    "intensity": float,          # Current intensity (0.0-1.0)
    "trust_level": float,        # Trust level (0.0-1.0)
    "interaction_count": int     # Number of interactions
}
```

---

### SafetyCoordinator

Coordinates all safety systems.

#### Constructor

```python
SafetyCoordinator(persona_config_path: str)
```

**Parameters**:
- `persona_config_path` (str): Path to persona configuration

#### Methods

##### process_user_input

```python
process_user_input(
    user_id: str,
    user_input: str,
    proposed_action: str,
    required_consent: ConsentLevel,
    intensity: IntensityLevel
) -> Dict[str, Any]
```

Process user input through all safety systems.

**Parameters**:
- `user_id` (str): User identifier
- `user_input` (str): User's message
- `proposed_action` (str): What the system wants to do
- `required_consent` (ConsentLevel): Consent level needed
  - Options: `NONE_REQUIRED`, `IMPLIED`, `EXPLICIT_REQUIRED`, `EXPLICIT_NEGOTIATED`
- `intensity` (IntensityLevel): Current intensity level
  - Options: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`

**Returns**:
```python
{
    "approved": bool,            # Whether action is approved
    "reason": str,              # Reason if not approved
    "consent_level": str,       # Detected consent level
    "protocol": Dict,           # Response protocol if needed
    "terminate_session": bool   # Whether to end session
}
```

**Example**:
```python
from personas.nocturne_vaelis.safety_module import ConsentLevel, IntensityLevel

result = safety.process_user_input(
    user_id="user_123",
    user_input="yes, I want to continue",
    proposed_action="escalate_intimacy",
    required_consent=ConsentLevel.EXPLICIT_REQUIRED,
    intensity=IntensityLevel.HIGH
)

if result["approved"]:
    # Proceed with action
    pass
else:
    # Handle safety issue
    print(result["reason"])
```

##### check_content_safety

```python
check_content_safety(user_id: str, content_elements: List[str]) -> Dict[str, Any]
```

Check if content is safe given user boundaries.

**Parameters**:
- `user_id` (str): User identifier
- `content_elements` (List[str]): Elements to check against boundaries

**Returns**:
```python
{
    "approved": bool|str,        # True, False, or "requires_discussion"
    "reason": str,              # Reason for decision
    "violations": List[str],    # Hard limit violations if any
    "soft_limits": List[str],   # Soft limits present if any
    "message": str              # Message to display to user
}
```

##### get_or_create_profile

```python
get_or_create_profile(user_id: str) -> UserProfile
```

Get existing user profile or create new one.

**Returns**: `UserProfile` object with boundary and consent data

---

### AdaptiveBehaviorEngine

Combines scenario randomization and mode switching.

#### Constructor

```python
AdaptiveBehaviorEngine(persona_config_path: str)
```

#### Methods

##### adapt_to_context

```python
adapt_to_context(
    user_context: UserContext,
    user_input: str,
    emotional_state: str
) -> Dict[str, Any]
```

Adapt persona behavior based on full context.

**Parameters**:
- `user_context` (UserContext): User context and preferences
- `user_input` (str): Latest user input
- `emotional_state` (str): Current emotional state

**Returns**:
```python
{
    "mode_transition": Dict,      # Mode change details if any
    "scenario_change": Dict,      # Scenario change details if any
    "branching_options": List,    # Available branching paths
    "mode_config": Dict          # Current mode configuration
}
```

##### get_current_state

```python
get_current_state() -> Dict[str, Any]
```

Get current state of adaptive behavior.

---

### NocturneVaelisSession

High-level session management interface.

#### Constructor

```python
NocturneVaelisSession(user_id: str, config_path: str = "personas/nocturne_vaelis/persona_core.json")
```

**Parameters**:
- `user_id` (str): Unique identifier for the user
- `config_path` (str, optional): Path to configuration

#### Methods

##### send_message

```python
send_message(message: str, context: str = "general") -> Dict[str, Any]
```

Send a message to Nocturne Vaelis and receive a response.

**Parameters**:
- `message` (str): The user's message
- `context` (str, optional): The interaction context

**Returns**:
```python
{
    "success": bool,              # Whether interaction was successful
    "response": str,             # Nocturne's response
    "emotional_state": str,      # Current emotional state
    "action": str,               # Required action
    "metadata": Dict            # Additional information
}
```

**Example**:
```python
session = NocturneVaelisSession(user_id="user_123")
result = session.send_message("Hello Nocturne", "general")

if result["success"]:
    print(result["response"])
else:
    print(f"Error: {result['action']}")
```

##### set_boundary

```python
set_boundary(category: str, item: str, is_hard_limit: bool = True) -> None
```

Set a user boundary.

**Parameters**:
- `category` (str): Boundary category (e.g., "activities", "language")
- `item` (str): The specific boundary item
- `is_hard_limit` (bool): Whether this is a hard limit. Default: True

**Example**:
```python
# Set hard limit
session.set_boundary("activities", "degradation", is_hard_limit=True)

# Set soft limit
session.set_boundary("activities", "edging", is_hard_limit=False)
```

##### set_safeword

```python
set_safeword(safeword: str) -> None
```

Set a custom safeword for this session.

##### change_intensity

```python
change_intensity(new_intensity: IntensityLevel) -> None
```

Change the interaction intensity level.

##### end_session

```python
end_session() -> None
```

End the current session.

##### get_session_stats

```python
get_session_stats() -> Dict[str, Any]
```

Get statistics about the current session.

**Returns**:
```python
{
    "user_id": str,
    "message_count": int,
    "trust_score": float,
    "interaction_count": int,
    "current_intensity": str,
    "emotional_state": str,
    "operational_mode": str,
    "session_active": bool
}
```

---

## Integration Patterns

### Pattern 1: Basic Chat Integration

```python
from personas.nocturne_vaelis.integration_example import NocturneVaelisSession

class ChatBot:
    def __init__(self):
        self.sessions = {}
    
    def handle_message(self, user_id, message):
        # Get or create session
        if user_id not in self.sessions:
            self.sessions[user_id] = NocturneVaelisSession(user_id)
        
        # Send message
        result = self.sessions[user_id].send_message(message)
        
        # Return response
        return result["response"] if result["success"] else "I can't continue right now."
```

### Pattern 2: Flask API Server

```python
from flask import Flask, request, jsonify
from personas.nocturne_vaelis.integration_example import NocturneVaelisSession

app = Flask(__name__)
sessions = {}

@app.route('/api/message', methods=['POST'])
def handle_message():
    data = request.json
    user_id = data['user_id']
    message = data['message']
    
    if user_id not in sessions:
        sessions[user_id] = NocturneVaelisSession(user_id)
    
    result = sessions[user_id].send_message(message)
    return jsonify(result)

@app.route('/api/boundary', methods=['POST'])
def set_boundary():
    data = request.json
    user_id = data['user_id']
    
    if user_id not in sessions:
        sessions[user_id] = NocturneVaelisSession(user_id)
    
    sessions[user_id].set_boundary(
        data['category'],
        data['item'],
        data.get('is_hard_limit', True)
    )
    
    return jsonify({"status": "success"})
```

### Pattern 3: Advanced Custom Integration

```python
from personas.nocturne_vaelis.nlp_framework import PersonaEngine, EmotionalState
from personas.nocturne_vaelis.safety_module import SafetyCoordinator
from personas.nocturne_vaelis.scenario_engine import AdaptiveBehaviorEngine

class AdvancedIntegration:
    def __init__(self, config_path):
        self.persona = PersonaEngine(config_path)
        self.safety = SafetyCoordinator(config_path)
        self.adaptive = AdaptiveBehaviorEngine(config_path)
    
    def process_with_context(self, user_id, message, user_context):
        # Safety check
        safety_result = self.safety.process_user_input(
            user_id=user_id,
            user_input=message,
            proposed_action="respond",
            required_consent="implied",
            intensity="medium_intensity"
        )
        
        if not safety_result["approved"]:
            return {"error": safety_result["reason"]}
        
        # Adaptive behavior
        adaptations = self.adaptive.adapt_to_context(
            user_context=user_context,
            user_input=message,
            emotional_state=self.persona.config.emotional_state.value
        )
        
        # Apply adaptations
        if "mode_transition" in adaptations:
            # Handle mode transition
            pass
        
        # Generate response
        result = self.persona.process_interaction(message)
        
        return {
            "response": result["response"],
            "adaptations": adaptations,
            "state": self.persona.get_state()
        }
```

---

## Examples

### Example 1: Simple Conversation

```python
from personas.nocturne_vaelis.integration_example import NocturneVaelisSession

# Create session
session = NocturneVaelisSession(user_id="user_001")

# Set boundaries
session.set_boundary("activities", "degradation", is_hard_limit=True)
session.set_safeword("phoenix")

# Conversation
messages = [
    ("Hello Nocturne", "general"),
    ("I'm curious about you", "general"),
    ("I want to explore something intimate", "seduction"),
]

for message, context in messages:
    result = session.send_message(message, context)
    if result["success"]:
        print(f"User: {message}")
        print(f"Nocturne: {result['response']}\n")
```

### Example 2: Handling Safeword

```python
session = NocturneVaelisSession(user_id="user_002")

# User triggers safeword
result = session.send_message("This is too intense, red", "dominant")

print(result["response"])  # "Stop. Everything stops. You're safe..."
print(result["action"])    # "safeword_protocol"
```

### Example 3: Boundary Management

```python
session = NocturneVaelisSession(user_id="user_003")

# Set multiple boundaries
session.set_boundary("activities", "degradation", is_hard_limit=True)
session.set_boundary("activities", "edging", is_hard_limit=False)
session.set_boundary("language", "harsh_language", is_hard_limit=False)

# Try to interact with content touching boundaries
result = session.send_message("Tell me I'm worthless", "degradation")

# Will be blocked due to hard limit
print(result["success"])  # False
print(result["response"])  # Boundary violation message
```

### Example 4: Progressive Intensity

```python
from personas.nocturne_vaelis.safety_module import IntensityLevel

session = NocturneVaelisSession(user_id="user_004")

# Start low intensity
session.change_intensity(IntensityLevel.LOW)
result = session.send_message("Let's talk", "general")

# Increase intensity
session.change_intensity(IntensityLevel.MEDIUM)
result = session.send_message("I want more", "seduction")

# High intensity with safety checks
session.change_intensity(IntensityLevel.HIGH)
result = session.send_message("Take control", "dominant")
```

---

## Error Handling

### Common Errors

#### Safety Lockout

**Triggered**: When prohibited content is detected

```python
{
    "success": False,
    "action": "terminate_session",
    "response": "I cannot engage with that content..."
}
```

**Handling**:
```python
result = session.send_message(message)
if result.get("action") == "terminate_session":
    # Session has been terminated
    # Create new session or inform user
    pass
```

#### Insufficient Consent

**Triggered**: When required consent level not met

```python
{
    "success": False,
    "action": "request_consent",
    "response": "I need clearer consent to continue..."
}
```

**Handling**:
```python
if result.get("action") == "request_consent":
    # Ask user for explicit consent
    # Retry with clearer consent
    pass
```

#### Distress Detection

**Triggered**: When user shows signs of distress

```python
{
    "success": False,
    "action": "pause",
    "response": "I'm pausing everything. Are you okay?"
}
```

**Handling**:
```python
if result.get("action") == "pause":
    # Provide support
    # Reduce intensity
    # Offer to end session
    session.change_intensity(IntensityLevel.LOW)
```

#### Boundary Violation

**Triggered**: When content violates hard limits

```python
{
    "success": False,
    "reason": "hard_limit_violation",
    "response": "This touches on your hard limits..."
}
```

**Handling**:
```python
if result.get("reason") == "hard_limit_violation":
    # Acknowledge violation
    # Choose different content
    pass
```

---

## Best Practices

### 1. Always Check Safety Results

```python
# ✅ Good
result = session.send_message(message)
if result["success"]:
    display_response(result["response"])
else:
    handle_safety_issue(result)

# ❌ Bad
result = session.send_message(message)
display_response(result["response"])  # May not exist if not successful
```

### 2. Set Boundaries Early

```python
# ✅ Good - Set boundaries at session start
session = NocturneVaelisSession(user_id)
session.set_boundary("activities", "degradation", is_hard_limit=True)
session.set_safeword("phoenix")

# ❌ Bad - Waiting until after interaction starts
```

### 3. Handle Mode Transitions

```python
# ✅ Good - Monitor and respond to mode changes
result = session.send_message(message)
if result["metadata"].get("adaptations"):
    if "mode_transition" in result["metadata"]["adaptations"]:
        # Acknowledge mode change to user
        transition = result["metadata"]["adaptations"]["mode_transition"]
        print(f"Mood shifting: {transition['message']}")
```

### 4. Respect Session State

```python
# ✅ Good - Check if session is active
stats = session.get_session_stats()
if not stats["session_active"]:
    # Create new session
    session = NocturneVaelisSession(user_id)
```

### 5. Provide Aftercare

```python
# ✅ Good - After intense scenes, transition to aftercare
if previous_context in ["dominant", "edge_play", "degradation"]:
    result = session.send_message("I need comfort", "general")
    session.change_intensity(IntensityLevel.LOW)
```

---

## Support & Resources

- **Documentation**: See [README.md](README.md) and [PERSONA_PROFILE.md](PERSONA_PROFILE.md)
- **Source Code**: Check module files for detailed implementation
- **Tests**: Review test files for usage examples
- **Issues**: Report issues through repository issue tracker

---

**Version**: 1.0.0  
**Last Updated**: 2026-02-17  
**Maintained By**: Whole Life Inc. AI Development Team
