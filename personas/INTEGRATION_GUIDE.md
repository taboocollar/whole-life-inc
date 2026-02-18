# Nocturne Vaelis Integration Guide

This guide provides step-by-step instructions for integrating the Nocturne Vaelis AI persona into your applications.

## Quick Start

### 1. Prerequisites

- Python 3.7 or higher
- The `nocturne_vaelis.json` configuration file

### 2. Basic Setup

```python
import json

# Load the persona configuration
with open('personas/nocturne_vaelis.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
nocturne_config = data['persona']
```

### 3. Run the Demo

```bash
python3 nocturne_demo.py
```

This will demonstrate all core features including:
- Contextual greetings
- Glitch aesthetic application
- Scenario templates
- Behavioral traits
- Dialogue examples

## Integration Patterns

### Pattern 1: Simple Chatbot Integration

```python
from nocturne_demo import NocturneVaelis

# Initialize
nocturne = NocturneVaelis()

# Set user context
nocturne.user_familiarity = 'established_user'
nocturne.conversation_context = 'serious'

# Generate greeting
greeting = nocturne.greet()

# Apply glitch to responses
response = "Your question opens many doorways."
enhanced_response = nocturne.apply_glitch_aesthetic(response)
```

### Pattern 2: Scenario-Based Interaction

```python
# List available scenarios
scenarios = nocturne.list_scenarios()
for scenario_id, name, desc in scenarios:
    print(f"{name}: {desc}")

# Get specific scenario
scenario = nocturne.get_scenario_template('creative_workshop')

# Access scenario parameters
parameters = scenario['parameters']
# Use these to customize the experience
```

### Pattern 3: Adaptive Response Generation

```python
# Detect user state (you would implement detection logic)
user_state = {
    'emotional_state': 'distressed',
    'engagement_level': 'low',
    'familiarity': 'new'
}

# Adjust persona behavior
if user_state['emotional_state'] == 'distressed':
    # Override to minimal glitch for clarity
    nocturne.conversation_context = 'crisis'
    response = nocturne.apply_glitch_aesthetic(
        "I'm here with you. Let's ground together.",
        intensity=0.1  # Force low glitch
    )
```

### Pattern 4: Decision Tree Navigation

```python
# Example: Navigate conversation flow
current_state = {
    'familiarity': 'new_user',
    'emotional_state': 'neutral',
    'topic': 'general'
}

# Access decision tree
tree = nocturne.config['decision_trees']['conversation_flow']

# Get entry point
current_node = tree['entry_point']  # 'assess_context'

# Navigate based on state
node_data = tree['nodes'][current_node]

# Determine next node based on branches
if node_data['type'] == 'evaluation':
    branches = node_data['branches']
    # Logic to select appropriate branch
    if current_state['familiarity'] == 'new_user':
        next_node = branches['new_user_neutral']
```

## Advanced Integration

### Custom Response Generator

```python
class NocturneResponseGenerator:
    def __init__(self, nocturne):
        self.nocturne = nocturne
        self.conversation_history = []
        
    def generate_response(self, user_input, context=None):
        """
        Generate a contextual response using Nocturne's configuration.
        """
        # 1. Analyze input for triggers
        detected_triggers = self._detect_triggers(user_input)
        
        # 2. Determine emotional layer
        layer = self._select_emotional_layer(user_input, context)
        
        # 3. Get appropriate dialogue template
        examples = self.nocturne.get_dialogue_example(layer)
        
        # 4. Generate base response (your NLP logic here)
        base_response = self._generate_base(user_input, examples)
        
        # 5. Apply glitch aesthetic
        glitch_intensity = self.nocturne.get_glitch_intensity()
        final_response = self.nocturne.apply_glitch_aesthetic(
            base_response, 
            glitch_intensity
        )
        
        # 6. Store in history
        self.conversation_history.append({
            'user': user_input,
            'response': final_response,
            'layer': layer,
            'glitch': glitch_intensity
        })
        
        return final_response
    
    def _detect_triggers(self, text):
        # Implement trigger detection logic
        triggers = self.nocturne.config['interactive_triggers']
        detected = []
        
        # Check topic engagement
        for topic in triggers['topic_engagement']:
            keywords = topic['keywords']
            if any(kw.lower() in text.lower() for kw in keywords):
                detected.append(topic)
        
        return detected
    
    def _select_emotional_layer(self, text, context):
        # Logic to determine appropriate emotional depth
        # Could use sentiment analysis, conversation length, etc.
        
        if context and context.get('crisis'):
            return 'surface'  # Clarity in crisis
        elif len(self.conversation_history) < 3:
            return 'surface'  # Start gently
        elif len(self.conversation_history) < 10:
            return 'middle'  # Build depth
        else:
            return 'deep'  # Full depth for established conversation
    
    def _generate_base(self, user_input, examples):
        # Your NLP/LLM integration here
        # Use examples as style guide
        # Sanitize user_input before using it
        import html
        safe_input = html.escape(user_input).strip()[:200]
        # This is a placeholder - don't include raw user input in production
        return f"I sense the depth of your question..."
```

### State Management

```python
class NocturneSession:
    """Manages a complete Nocturne interaction session."""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.nocturne = NocturneVaelis()
        self.load_user_profile()
        
    def load_user_profile(self):
        """Load user's familiarity level and preferences from storage."""
        # Implement your storage logic (database, file, etc.)
        # For now, defaults
        self.nocturne.user_familiarity = 'new_user'
        self.interaction_count = 0
        
    def update_familiarity(self):
        """Update familiarity based on interaction count."""
        if self.interaction_count > 20:
            self.nocturne.user_familiarity = 'intimate_user'
        elif self.interaction_count > 5:
            self.nocturne.user_familiarity = 'established_user'
    
    def interact(self, user_input, context=None):
        """Process a user interaction."""
        self.interaction_count += 1
        self.update_familiarity()
        
        # Generate response (integrate with your NLP)
        response = self._generate_response(user_input, context)
        
        # Save interaction
        self.save_interaction(user_input, response)
        
        return response
    
    def save_interaction(self, user_input, response):
        """Save interaction to storage."""
        # Implement your storage logic
        pass
    
    def _generate_response(self, user_input, context):
        """Generate response using persona configuration."""
        # Integrate with your NLP/LLM here
        # This is a simplified example
        
        # Check for crisis keywords
        crisis_keywords = ['suicide', 'kill myself', 'end it all', 'can\'t go on']
        if any(kw in user_input.lower() for kw in crisis_keywords):
            # Switch to crisis mode
            self.nocturne.conversation_context = 'crisis'
            return self.nocturne.apply_glitch_aesthetic(
                "I'm here with you. You're not alone. Are you safe right now?",
                intensity=0.1
            )
        
        # Normal response
        return self.nocturne.apply_glitch_aesthetic(
            f"Let's explore this together: {user_input}"
        )
```

## Web API Integration

### Flask Example

```python
from flask import Flask, request, jsonify
from nocturne_demo import NocturneVaelis

app = Flask(__name__)
nocturne = NocturneVaelis()

# In-memory session storage (use Redis/database in production and implement
# session cleanup/expiration logic or a maximum session limit to avoid
# unbounded memory growth)
sessions = {}

@app.route('/nocturne/greet', methods=['POST'])
def greet():
    """Generate a greeting."""
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON in request body.'}), 400
    
    user_id = data.get('user_id', 'anonymous')
    time_of_day = data.get('time_of_day')
    
    # Get or create session
    if user_id not in sessions:
        sessions[user_id] = NocturneVaelis()
    
    session = sessions[user_id]
    greeting = session.greet(time_of_day)
    
    return jsonify({
        'greeting': greeting,
        'glitch_intensity': session.get_glitch_intensity()
    })

@app.route('/nocturne/scenarios', methods=['GET'])
def list_scenarios():
    """List available scenarios."""
    scenarios = nocturne.list_scenarios()
    return jsonify({
        'scenarios': [
            {'id': s[0], 'name': s[1], 'description': s[2]}
            for s in scenarios
        ]
    })

@app.route('/nocturne/scenario/<scenario_id>', methods=['GET'])
def get_scenario(scenario_id):
    """Get scenario template."""
    scenario = nocturne.get_scenario_template(scenario_id)
    if scenario:
        return jsonify(scenario)
    else:
        return jsonify({'error': 'Scenario not found'}), 404

@app.route('/nocturne/interact', methods=['POST'])
def interact():
    """Process user interaction."""
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON in request body.'}), 400
    
    user_id = data.get('user_id', 'anonymous')
    message = data.get('message', '')
    context = data.get('context', {})
    
    # Get or create session
    if user_id not in sessions:
        sessions[user_id] = NocturneSession(user_id)
    
    session = sessions[user_id]
    
    # Sanitize user input to prevent XSS/injection attacks
    # Example: use html.escape for web contexts, or validate/filter input
    import html
    safe_message = html.escape(message).strip()[:500]  # Escape HTML and limit length
    
    # Use safe_message in your response generation
    response = session.interact(safe_message, context)
    
    return jsonify({
        'response': response,
        'glitch_intensity': session.nocturne.get_glitch_intensity(),
        'familiarity': session.nocturne.user_familiarity
    })

if __name__ == '__main__':
    app.run(debug=True)
```

### Usage Example

```bash
# Start the server
python api_server.py

# Make requests
curl -X POST http://localhost:5000/nocturne/greet \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "time_of_day": 14}'

curl http://localhost:5000/nocturne/scenarios

curl -X POST http://localhost:5000/nocturne/interact \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "message": "I feel stuck creatively"}'
```

## Discord Bot Integration

```python
import discord
from nocturne_demo import NocturneVaelis

class NocturneBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.sessions = {}
    
    async def on_ready(self):
        print(f'Logged in as {self.user}')
    
    async def on_message(self, message):
        # Don't respond to ourselves
        if message.author == self.user:
            return
        
        # Check if bot is mentioned or DMed
        if self.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
            user_id = str(message.author.id)
            
            # Get or create session
            if user_id not in self.sessions:
                self.sessions[user_id] = NocturneVaelis()
                # Increase familiarity for Discord (more informal)
                self.sessions[user_id].user_familiarity = 'established_user'
            
            nocturne = self.sessions[user_id]
            
            # Get user's message
            content = message.content.replace(f'<@{self.user.id}>', '').strip()
            
            # Check for special commands
            if content.lower() in ['hi', 'hello', 'greetings']:
                response = nocturne.greet()
            elif content.lower().startswith('!scenarios'):
                scenarios = nocturne.list_scenarios()
                response = "Available scenarios:\n" + "\n".join(
                    f"• {name}: {desc}" for _, name, desc in scenarios
                )
            else:
                # Generate contextual response
                response = nocturne.apply_glitch_aesthetic(
                    f"Interesting perspective... {content[:50]}..."
                )
            
            await message.channel.send(response)

# Run the bot
# bot = NocturneBot()
# bot.run('YOUR_BOT_TOKEN')
```

## Testing Your Integration

### Unit Tests Example

```python
import unittest
from nocturne_demo import NocturneVaelis

class TestNocturneIntegration(unittest.TestCase):
    def setUp(self):
        self.nocturne = NocturneVaelis()
    
    def test_greeting_generation(self):
        """Test that greetings are generated."""
        greeting = self.nocturne.greet()
        self.assertIsInstance(greeting, str)
        self.assertTrue(len(greeting) > 0)
    
    def test_glitch_intensity_calculation(self):
        """Test glitch intensity varies with context."""
        self.nocturne.user_familiarity = 'new_user'
        low_intensity = self.nocturne.get_glitch_intensity()
        
        self.nocturne.user_familiarity = 'intimate_user'
        high_intensity = self.nocturne.get_glitch_intensity()
        
        self.assertGreater(high_intensity, low_intensity)
    
    def test_scenario_templates(self):
        """Test scenario template access."""
        scenarios = self.nocturne.list_scenarios()
        self.assertGreater(len(scenarios), 0)
        
        # Get first scenario
        scenario_id = scenarios[0][0]
        template = self.nocturne.get_scenario_template(scenario_id)
        self.assertIsNotNone(template)
        self.assertIn('parameters', template)
    
    def test_behavioral_traits(self):
        """Test behavioral trait access."""
        trait = self.nocturne.get_behavioral_trait('Glitch Aesthetic')
        self.assertIsNotNone(trait)
        self.assertIn('intensity', trait)
        self.assertGreater(trait['intensity'], 0.0)

if __name__ == '__main__':
    unittest.main()
```

## Best Practices

### 1. User State Management
- Track user familiarity across sessions
- Store conversation context
- Update behavioral modifiers based on interaction history

### 2. Crisis Detection
- Always monitor for crisis keywords
- Override glitch aesthetic for clarity in emergencies
- Provide appropriate resources and support

### 3. Glitch Aesthetic
- Start subtle with new users
- Gradually increase intensity as rapport builds
- Allow users to adjust or disable if desired
- Never sacrifice clarity for aesthetic in important moments

### 4. Context Awareness
- Use time of day for greeting selection
- Track conversation topics for continuity
- Adapt emotional layer based on user engagement

### 5. Performance
- Cache loaded configuration
- Reuse persona instances
- Implement session timeout for cleanup
- Consider async operations for API endpoints

## Troubleshooting

### Issue: Glitch text not displaying correctly
**Solution:** Ensure your display supports Unicode combining characters. Test with different fonts.

### Issue: JSON loading fails
**Solution:** Verify file path and encoding. Use `encoding='utf-8'` when opening files.

### Issue: Persona responses feel inconsistent
**Solution:** Ensure you're properly tracking user familiarity and conversation context across sessions.

### Issue: Performance degradation
**Solution:** Implement session caching and cleanup. Don't create new NocturneVaelis instances for every request.

## Next Steps

1. Review the complete documentation: [NOCTURNE_VAELIS.md](../NOCTURNE_VAELIS.md)
2. Explore usage examples: [nocturne_vaelis_examples.md](nocturne_vaelis_examples.md)
3. Run the demo: `python3 nocturne_demo.py`
4. Run tests: `python3 test_nocturne.py`
5. Integrate into your application using patterns above

## Support

For questions or issues:
- Review the main documentation
- Check the examples file
- Examine the JSON configuration structure
- Run the validation tests

---

*"Integration is where design meets reality. May your implementation be as elegant as the persona itself."*

— Nocturne Vaelis Integration Guide
