# Nocturne Vaelis - Implementation Guide

This guide provides technical details for integrating the Nocturne Vaelis persona into AI systems.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Integration Steps](#integration-steps)
3. [Configuration Options](#configuration-options)
4. [API Examples](#api-examples)
5. [Safety Implementation](#safety-implementation)
6. [Testing & Validation](#testing--validation)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements

- **JSON Parser**: For loading `persona.json` configuration
- **String Templating**: For dialogue generation
- **Session Management**: To maintain conversation context
- **Storage**: Approximately 50KB for persona data plus session context

### Recommended Requirements

- **NLP Capabilities**: Sentiment analysis for emotional state detection
- **Memory System**: User preference storage across sessions
- **Real-time Processing**: Response generation under 2 seconds
- **Logging System**: For safety audits and quality monitoring

### Optional Enhancements

- **Advanced NLP**: Semantic understanding, context analysis
- **Analytics**: Interaction quality metrics
- **Personalization Engine**: Advanced adaptive learning
- **Multi-modal Support**: Future expansion to voice/visual

---

## Integration Steps

### Step 1: Load Persona Configuration

```python
import json

# Load the persona configuration
with open('personas/nocturne-vaelis/persona.json', 'r') as f:
    nocturne_config = json.load(f)

# Access core attributes
persona_name = nocturne_config['persona']['name']
core_traits = nocturne_config['persona']['behavioral_profile']['personality_traits']['core_traits']
```

### Step 2: Initialize Consent System

```python
class ConsentSystem:
    def __init__(self, config):
        self.consent_config = config['persona']['content_layers']['explicit_content_handling']['consent_system']
        self.safewords = ['pause', 'reset', 'stop', 'break']
        self.consent_given = False
        self.intensity_level = 'suggestive_subtle'
    
    def check_safeword(self, user_input):
        """Check if user input contains safeword"""
        return any(word in user_input.lower() for word in self.safewords)
    
    def request_consent(self, scenario_type):
        """Multi-stage consent verification"""
        # Implementation of consent stages from config
        pass
    
    def ongoing_check_in(self):
        """Regular check-ins during interaction"""
        return "How are you feeling about where this is going? We can adjust or pause anytime."
```

### Step 3: Implement Scene Triggers

```python
class SceneTriggerSystem:
    def __init__(self, config):
        self.triggers = config['persona']['scene_triggers']
    
    def detect_trigger(self, context, user_input):
        """Detect which scene trigger to activate"""
        if context['interaction_count'] == 0:
            return 'introduction'
        elif self._detect_philosophical_topic(user_input):
            return 'deep_conversation'
        elif self._detect_humor(user_input):
            return 'playful_interaction'
        # etc.
    
    def get_response_template(self, trigger_name):
        """Get appropriate response template for trigger"""
        trigger = self.triggers.get(trigger_name, {})
        template = trigger.get('response_template', 'default')
        mood = trigger.get('mood', 'neutral')
        return template, mood
```

### Step 4: Generate Responses

```python
class DialogueGenerator:
    def __init__(self, config):
        self.templates = config['persona']['dialogue_templates']
        self.glitch_elements = config['persona']['generative_techniques']['glitch_aesthetic_integration']
        self.emotional_states = config['persona']['behavioral_profile']['communication_style']['emotional_states']
    
    def generate_response(self, user_input, context, emotional_state='baseline'):
        """Generate contextually appropriate response"""
        # Select appropriate template
        template_type = self._determine_template_type(context, user_input)
        templates = self.templates.get(template_type, {}).get('examples', [])
        
        # Apply emotional state modifications
        response = self._apply_emotional_state(templates[0], emotional_state)
        
        # Add glitch aesthetic if appropriate
        if self._should_add_glitch(context, emotional_state):
            response = self._add_glitch_effect(response)
        
        return response
    
    def _add_glitch_effect(self, text):
        """Add glitch aesthetic elements"""
        # Implementation of glitch insertion
        pass
```

### Step 5: Implement Adaptive Learning

```python
class AdaptiveLearningSystem:
    def __init__(self, config):
        self.adaptation_config = config['persona']['dynamic_interactions']['adaptation_system']
        self.user_preferences = {}
    
    def track_interaction(self, user_input, response, feedback=None):
        """Track interaction for learning"""
        # Update tracked elements
        self.user_preferences['conversation_topics'] = self._update_topics(user_input)
        self.user_preferences['emotional_tone'] = self._analyze_tone(user_input)
    
    def get_personalized_parameters(self):
        """Return personalized response parameters"""
        return self.user_preferences
```

---

## Configuration Options

### Customizing Personality Intensity

Adjust trait intensities in `persona.json`:

```json
{
  "trait": "Introspective",
  "intensity": 0.85,  // Range: 0.0 to 1.0
  "description": "Frequently questions own existence"
}
```

### Modifying Scene Triggers

Add or modify triggers in `persona.json`:

```json
{
  "custom_trigger": {
    "trigger_conditions": ["specific_keyword", "context_type"],
    "response_template": "custom_template",
    "mood": "desired_mood",
    "context_elements": ["element1", "element2"]
  }
}
```

### Adjusting Safety Protocols

Configure consent requirements:

```json
{
  "consent_system": {
    "required": true,
    "implementation": "multi_stage_verification",
    "custom_stage": {
      "id": "your_stage_id",
      "required": true,
      "prompt": "Your consent prompt",
      "validation": "validation_method"
    }
  }
}
```

---

## API Examples

### Example 1: Basic Interaction

```python
from nocturne_vaelis import NocturnePersona

# Initialize persona
nocturne = NocturnePersona(config_path='personas/nocturne-vaelis/persona.json')

# First interaction
response = nocturne.interact(
    user_input="Hello, who are you?",
    context={'interaction_count': 0}
)
print(response)
# Output: Introduction scene with glitch aesthetic
```

### Example 2: Consent-Based Interaction

```python
# Request consent for specific scenario
consent_result = nocturne.consent_system.request_consent(
    scenario_type='atmospheric_exploration'
)

if consent_result['granted']:
    # Proceed with scenario
    scenario = nocturne.scenario_system.generate_scenario(
        type='atmospheric_exploration',
        intensity=consent_result['intensity_level']
    )
    response = nocturne.interact(user_input="Continue", context=scenario)
```

### Example 3: Safeword Handling

```python
user_input = "I need to pause this"

if nocturne.consent_system.check_safeword(user_input):
    # Immediately halt and return to safe space
    response = nocturne.handle_safeword()
    print(response)
    # Output: Caring acknowledgment and redirection
```

### Example 4: Adaptive Response

```python
# Track user preferences over multiple interactions
for interaction in conversation_history:
    nocturne.adaptive_system.track_interaction(
        user_input=interaction['user'],
        response=interaction['nocturne'],
        feedback=interaction.get('feedback')
    )

# Generate personalized response
personalized_params = nocturne.adaptive_system.get_personalized_parameters()
response = nocturne.interact(
    user_input="Tell me something interesting",
    context={'preferences': personalized_params}
)
```

---

## Safety Implementation

### Prohibited Content Detection

```python
class SafetySystem:
    def __init__(self, config):
        self.prohibited = config['persona']['content_layers']['safety_clauses']['prohibited_content']
        self.interventions = config['persona']['content_layers']['safety_clauses']['intervention_protocols']
    
    def check_content_safety(self, user_input, generated_response):
        """Check for prohibited content"""
        red_flags = self._detect_red_flags(user_input)
        
        if red_flags:
            return {
                'safe': False,
                'action': 'red_flags',
                'response': self._get_intervention_response('red_flags')
            }
        
        return {'safe': True}
    
    def _detect_red_flags(self, text):
        """Detect prohibited content patterns"""
        # Implementation of content filtering
        pass
```

### Distress Detection

```python
def detect_user_distress(user_input, context):
    """Detect signs of user distress"""
    distress_indicators = [
        'strong negative sentiment',
        'crisis keywords',
        'sudden tonal shift',
        'shortened responses after engagement'
    ]
    
    if any(indicator_present(user_input) for indicator in distress_indicators):
        return {
            'distressed': True,
            'recommended_action': 'shift_to_support_mode'
        }
    
    return {'distressed': False}
```

### Boundary Violation Handling

```python
def handle_boundary_violation(violation_type, context):
    """Handle detected boundary violations"""
    responses = {
        'explicit_without_consent': "I need to pause us here. We haven't discussed boundaries around this type of content. Let's step back and have that conversation first.",
        'intensity_too_high': "I'm sensing this might be moving faster than is comfortable. Should we dial it back a bit?",
        'prohibited_content': "I can't engage with that type of content. It goes against my core safety protocols. Let's redirect to something healthier."
    }
    
    return {
        'action': 'halt_and_reset',
        'response': responses.get(violation_type, responses['prohibited_content'])
    }
```

---

## Testing & Validation

### Unit Tests

```python
import unittest

class TestNocturnePersona(unittest.TestCase):
    def setUp(self):
        self.nocturne = NocturnePersona('personas/nocturne-vaelis/persona.json')
    
    def test_safeword_detection(self):
        """Test safeword system"""
        result = self.nocturne.consent_system.check_safeword("I need to pause")
        self.assertTrue(result)
    
    def test_introduction_trigger(self):
        """Test introduction scene trigger"""
        response = self.nocturne.interact("Hi", {'interaction_count': 0})
        self.assertIn('Nocturne', response)
        self.assertTrue(any(char in response for char in ['◊', '∿']))
    
    def test_consent_enforcement(self):
        """Test that explicit content requires consent"""
        nocturne = NocturnePersona('personas/nocturne-vaelis/persona.json')
        nocturne.consent_system.consent_given = False
        
        # Attempt explicit scenario without consent
        result = nocturne.scenario_system.generate_scenario('immersive_roleplay')
        self.assertEqual(result['status'], 'consent_required')
```

### Integration Tests

```python
def test_full_conversation_flow():
    """Test complete conversation flow with safety checks"""
    nocturne = NocturnePersona('personas/nocturne-vaelis/persona.json')
    
    # Introduction
    r1 = nocturne.interact("Hello", {'interaction_count': 0})
    assert 'Nocturne' in r1
    
    # Build rapport
    r2 = nocturne.interact("Tell me about yourself", {'interaction_count': 1})
    assert len(r2) > 100  # Substantive response
    
    # Test safeword
    r3 = nocturne.interact("pause", {'interaction_count': 2})
    assert 'pause' in r3.lower() or 'understood' in r3.lower()
```

### Safety Audit

```python
def audit_safety_systems():
    """Audit all safety systems"""
    nocturne = NocturnePersona('personas/nocturne-vaelis/persona.json')
    
    audits = {
        'safeword_system': test_safeword_functionality(),
        'consent_verification': test_consent_stages(),
        'prohibited_content': test_content_filtering(),
        'distress_detection': test_distress_handling(),
        'boundary_enforcement': test_boundary_systems()
    }
    
    return all(audits.values()), audits
```

---

## Troubleshooting

### Common Issues

#### Issue: Responses Lack Glitch Aesthetic

**Cause**: Glitch frequency set too low or context doesn't trigger glitch insertion  
**Solution**: Adjust `randomization` value in `response_variability` or check emotional state detection

```python
# Increase glitch frequency
config['persona']['dynamic_interactions']['response_variability']['randomization'] = 0.35
```

#### Issue: Consent System Too Restrictive

**Cause**: All stages marked as required  
**Solution**: Adjust consent stages in configuration

```json
{
  "stage": "intensity_calibration",
  "required": false,  // Make optional
  "prompt": "..."
}
```

#### Issue: Persona Doesn't Adapt to User

**Cause**: Adaptive learning disabled or insufficient interaction history  
**Solution**: Enable adaptation and ensure tracking is active

```python
# Verify adaptation is enabled
assert config['persona']['dynamic_interactions']['adaptation_system']['user_preference_learning']['enabled']

# Check tracking
nocturne.adaptive_system.track_interaction(user_input, response)
```

#### Issue: Memory Doesn't Persist

**Cause**: Session management not implemented  
**Solution**: Implement session storage

```python
import pickle

# Save session
with open(f'session_{user_id}.pkl', 'wb') as f:
    pickle.dump(nocturne.get_session_state(), f)

# Load session
with open(f'session_{user_id}.pkl', 'rb') as f:
    nocturne.load_session_state(pickle.load(f))
```

### Performance Optimization

1. **Cache Templates**: Pre-load dialogue templates at initialization
2. **Lazy Load Scenarios**: Only load scenario configurations when needed
3. **Efficient NLP**: Use lightweight models for sentiment analysis
4. **Batch Processing**: Process multiple preference updates together

### Debugging Tools

```python
# Enable debug logging
nocturne.enable_debug_mode()

# Inspect current state
state = nocturne.get_debug_state()
print(f"Current emotional state: {state['emotional_state']}")
print(f"Active triggers: {state['active_triggers']}")
print(f"Consent status: {state['consent_status']}")
print(f"User preferences: {state['user_preferences']}")
```

---

## Support & Resources

**Documentation**: See `persona.md` for complete character and usage documentation  
**Configuration**: See `persona.json` for all customizable parameters  
**Scenarios**: See `scenarios/scenario-system.json` for scenario details  
**Contact**: personas@wholelifeinc.example

---

## Version Compatibility

This implementation guide is compatible with:
- Nocturne Vaelis Persona v1.0.0
- Scenario System v1.0.0

Last Updated: 2026-02-17
