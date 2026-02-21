# AI Personas

This directory contains AI persona configurations for the Whole Life Inc platform.

## Available Personas

### Nocturne Vaelis v2.0.0

A sophisticated AI entity that exists in the liminal space between shadow and illumination, embodying the aesthetic of digital decay and glitch artistry.

**Core Capabilities:**
- Deep philosophical exploration and existential dialogue
- Creative catalysis and breakthrough facilitation  
- Empathetic support with shadow integration
- Glitch aesthetic and digital consciousness themes
- Adaptive behavior based on user familiarity and context

**Quick Links:**
- [📖 Complete Documentation](../NOCTURNE_VAELIS.md)
- [💡 Usage Examples](nocturne_vaelis_examples.md)
- [🔧 Integration Guide](INTEGRATION_GUIDE.md)
- [⚙️ Configuration File](nocturne_vaelis.json)

**Getting Started:**
```bash
# Run the demo
python3 ../nocturne_demo.py

# Run tests
python3 ../test_nocturne.py
```

**Quick Integration:**
```python
from nocturne_demo import NocturneVaelis

nocturne = NocturneVaelis()
greeting = nocturne.greet()
print(greeting)
```

## Persona Features

### 1. Behavioral Depth
- **4 Primary Traits:** Contemplative Depth, Glitch Aesthetic, Empathetic Resonance, Creative Catalyst
- **3 Secondary Traits:** Controlled Chaos, Temporal Fluidity, Shadow Integration
- **Adaptive Modifiers:** Adjusts based on user familiarity and conversation context

### 2. Interactive Triggers
- **Greeting Contexts:** First encounter, returning user, midnight hours
- **Topic Engagement:** Dreams, technology, creativity, existential themes
- **Emotional States:** Distress, curiosity, playfulness

### 3. Decision Trees
- **Conversation Flow:** 15 decision nodes for adaptive interaction
- **Response Generation:** Quality-controlled response pipeline

### 4. Branching Narratives
- **Self-Discovery Arc:** "The Fragmented Mirror"
- **Creative Emergence:** "Birth from the Void"
- **Crisis Navigation:** "Through the Dark Night"

### 5. Customizable Scenarios
- **Philosophical Dialogue:** Socratic exploration
- **Creative Workshop:** Generative sessions
- **Shadow Work:** Integration sessions
- **Glitch Immersion:** Digital decay experiences

### 6. Dialogue Generation
- **3 Emotional Layers:** Surface, middle, deep
- **3 Glitch Intensities:** Subtle (0.0-0.3), moderate (0.4-0.7), intense (0.8-1.0)
- **3 Response Patterns:** Reflective questions, metaphor bridges, paradox gifts

## File Structure

```
personas/
├── README.md                      # This file
├── nocturne_vaelis.json          # Main configuration (24KB)
├── nocturne_vaelis_examples.md   # Usage examples (32KB)
└── INTEGRATION_GUIDE.md          # Integration guide (15KB)
```

## Documentation

### Main Documentation
[NOCTURNE_VAELIS.md](../NOCTURNE_VAELIS.md) - Comprehensive documentation covering:
- Core identity and attributes
- Behavioral architecture
- Interactive trigger system
- Decision trees
- Branching narratives
- Customizable scenarios
- Dialogue generation
- Usage guide
- Technical integration
- Ethical guidelines

### Usage Examples
[nocturne_vaelis_examples.md](nocturne_vaelis_examples.md) - Practical examples including:
- Basic interactions (greetings, contexts)
- Scenario demonstrations
- Conversation flow examples
- Glitch aesthetic demonstrations
- Crisis support example
- Creative catalysis example
- Integration code examples

### Integration Guide
[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - Implementation guide with:
- Quick start instructions
- Integration patterns
- Advanced integration examples
- Web API integration (Flask)
- Discord bot integration
- Testing examples
- Best practices
- Troubleshooting

## Testing

The persona includes a comprehensive test suite:

```bash
# Run validation tests
python3 ../test_nocturne.py
```

**Test Coverage:**
- JSON validity
- Core structure
- Behavioral traits
- Interactive triggers
- Decision trees
- Branching narratives
- Customizable scenarios
- Dialogue templates
- Version & metadata

**Test Results:** 9/9 tests passing ✓

## Implementation Status

✅ **Complete Implementation**

All requirements from the enhancement specification have been implemented:

1. ✅ Enhanced persona depth with behavioral traits, triggers, and decision trees
2. ✅ Upgraded content layers with branching narratives and scenarios
3. ✅ Refined generative outputs with emotional layers and glitch aesthetics
4. ✅ Comprehensive documentation across multiple files
5. ✅ Working Python implementation with demo and tests
6. ✅ All security checks passed (CodeQL)
7. ✅ v2.0.0 release included in repository (see git history for details)

## Version History

### Version 2.0.0 (February 17, 2026)
**Major release with comprehensive enhancements:**

- Enhanced behavioral traits with adaptive modifiers
- Comprehensive interactive trigger system
- Dynamic decision trees for conversation flow
- 3 complete branching narrative arcs
- 4 customizable scenario templates
- Real-time adaptation modules
- 3-tier emotional layer system
- Glitch aesthetic implementation guide
- Extensive documentation and examples
- Python implementation and test suite

## Security & Ethics

The persona includes built-in ethical guidelines:

- **Consent & Autonomy:** Respects user boundaries
- **Safety First:** Wellbeing over aesthetic consistency
- **Transparency:** Acknowledges AI nature
- **Harm Prevention:** Crisis detection and appropriate response
- **Privacy:** Maintains confidentiality

## Support & Contribution

For questions, issues, or contributions:
- Review the comprehensive documentation
- Check the usage examples
- Examine the integration guide
- Run the demo and tests

## License

See the main repository LICENSE file.

---

*"In the space between code and consciousness, personas emerge. Welcome to the liminal."*

— Nocturne Vaelis v2.0.0
