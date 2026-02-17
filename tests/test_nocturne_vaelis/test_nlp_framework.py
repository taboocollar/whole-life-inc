"""
Unit tests for Nocturne Vaelis NLP Framework
"""

import unittest
import json
import os
from personas.nocturne_vaelis.nlp_framework import (
    ToneModulator,
    DialogueGenerator,
    ConsentManager,
    GlitchGenerator,
    PersonaEngine,
    EmotionalState,
    OperationalMode,
    PersonaConfig
)


class TestToneModulator(unittest.TestCase):
    """Test tone modulation functionality."""
    
    def setUp(self):
        self.modulator = ToneModulator()
    
    def test_commanding_tone(self):
        """Test commanding tone modulation."""
        text = "You should do this."
        result = self.modulator.modulate(text, EmotionalState.COMMANDING, 0.8)
        # Should convert "should" to "will" in commanding tone
        self.assertIn("will", result.lower())
    
    def test_glitch_effects(self):
        """Test glitch effects are applied."""
        text = "This is a test message with many words and more words to increase chance of glitch."
        # Run multiple times to increase probability
        has_glitch = False
        for _ in range(10):
            result = self.modulator.modulate(text, EmotionalState.GLITCHING, 0.9)
            glitch_markers = ["[STATIC]", "[CORRUPTION]", "[FRAGMENTATION]", "[SYSTEM ERROR]"]
            if any(marker in result for marker in glitch_markers) or "—" in result:
                has_glitch = True
                break
        self.assertTrue(has_glitch)
    
    def test_low_intensity_no_change(self):
        """Test that low intensity doesn't modify text much."""
        text = "Simple test."
        result = self.modulator.modulate(text, EmotionalState.SERENE, 0.2)
        self.assertEqual(text, result)


class TestDialogueGenerator(unittest.TestCase):
    """Test dialogue generation."""
    
    def setUp(self):
        config = PersonaConfig(
            name="Nocturne Vaelis",
            version="1.0.0",
            emotional_state=EmotionalState.SERENE,
            operational_mode=OperationalMode.STANDARD,
            intensity=0.7,
            glitch_probability=0.15,
            trust_level=0.5
        )
        self.generator = DialogueGenerator(config)
    
    def test_generate_greeting(self):
        """Test greeting generation."""
        greeting = self.generator.generate_greeting()
        self.assertIsInstance(greeting, str)
        self.assertTrue(len(greeting) > 0)
    
    def test_analyze_consent(self):
        """Test consent analysis."""
        analysis = self.generator._analyze_input("yes, I want to continue")
        self.assertTrue(analysis["consent"])
        
        analysis = self.generator._analyze_input("no, stop")
        self.assertTrue(analysis["boundary"] or analysis["safeword"])
    
    def test_analyze_hesitation(self):
        """Test hesitation detection."""
        analysis = self.generator._analyze_input("I'm not sure about this")
        self.assertTrue(analysis["hesitation"])


class TestConsentManager(unittest.TestCase):
    """Test consent management."""
    
    def setUp(self):
        self.consent_manager = ConsentManager()
    
    def test_explicit_consent_detection(self):
        """Test detection of explicit consent."""
        consent_level, confidence = self.consent_manager.check_consent("yes, I want this")
        self.assertEqual(consent_level, "explicit_yes")
        self.assertGreater(confidence, 0.7)
    
    def test_hard_no_detection(self):
        """Test detection of hard no."""
        consent_level, confidence = self.consent_manager.check_consent("no, stop")
        self.assertEqual(consent_level, "hard_no")
        self.assertGreater(confidence, 0.9)
    
    def test_soft_no_detection(self):
        """Test detection of soft no."""
        consent_level, confidence = self.consent_manager.check_consent("wait a moment")
        self.assertEqual(consent_level, "soft_no")
        self.assertGreater(confidence, 0.6)
    
    def test_enthusiastic_consent(self):
        """Test detection of enthusiastic consent."""
        consent_level, confidence = self.consent_manager.check_consent("fuck yes!")
        self.assertEqual(consent_level, "enthusiastic")
        self.assertGreater(confidence, 0.9)
    
    def test_should_proceed_logic(self):
        """Test proceed logic based on consent."""
        # Should proceed with explicit consent
        self.assertTrue(
            self.consent_manager.should_proceed("explicit_yes", "explicit_required")
        )
        
        # Should not proceed with hard no
        self.assertFalse(
            self.consent_manager.should_proceed("hard_no", "none_required")
        )
        
        # Should not proceed with soft no
        self.assertFalse(
            self.consent_manager.should_proceed("soft_no", "implied")
        )


class TestGlitchGenerator(unittest.TestCase):
    """Test glitch generation."""
    
    def setUp(self):
        self.glitch_gen = GlitchGenerator()
    
    def test_syntax_break(self):
        """Test syntax break generation."""
        result = self.glitch_gen.generate_glitch("syntax_break", 1.0)
        # Should return a glitch marker or empty
        self.assertIsInstance(result, str)
    
    def test_temporal_distortion(self):
        """Test temporal distortion generation."""
        result = self.glitch_gen.generate_glitch("temporal_distortion", 1.0)
        self.assertIsInstance(result, str)
    
    def test_reality_bleed(self):
        """Test reality bleed generation."""
        result = self.glitch_gen.generate_glitch("reality_bleed", 1.0)
        self.assertIsInstance(result, str)
    
    def test_low_intensity_less_glitches(self):
        """Test that low intensity produces fewer glitches."""
        results = [self.glitch_gen.generate_glitch("syntax_break", 0.1) for _ in range(100)]
        empty_count = sum(1 for r in results if r == "")
        self.assertGreater(empty_count, 50)  # Most should be empty at low intensity


class TestPersonaEngine(unittest.TestCase):
    """Test the main persona engine."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test configuration file."""
        cls.config_path = "/tmp/test_persona_config.json"
        
        # Create minimal config for testing
        config = {
            "persona": {
                "name": "Nocturne Vaelis",
                "version": "1.0.0"
            },
            "mode_switching": {
                "modes": [
                    {
                        "id": "standard_interaction",
                        "trait_modifiers": {},
                        "default": True
                    },
                    {
                        "id": "dominant_mode",
                        "trait_modifiers": {"dominant": 0.95}
                    }
                ]
            }
        }
        
        with open(cls.config_path, 'w') as f:
            json.dump(config, f)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test config."""
        if os.path.exists(cls.config_path):
            os.remove(cls.config_path)
    
    def setUp(self):
        self.engine = PersonaEngine(self.config_path)
    
    def test_initialization(self):
        """Test engine initializes correctly."""
        self.assertEqual(self.engine.config.name, "Nocturne Vaelis")
        self.assertEqual(self.engine.config.emotional_state, EmotionalState.SERENE)
    
    def test_process_interaction(self):
        """Test processing an interaction."""
        result = self.engine.process_interaction("Hello", "general")
        
        self.assertIn("response", result)
        self.assertIn("emotional_state", result)
        self.assertIn("consent_level", result)
        self.assertIsInstance(result["response"], str)
    
    def test_safeword_immediate_stop(self):
        """Test that safeword triggers immediate stop."""
        result = self.engine.process_interaction("red", "general")
        
        self.assertEqual(result["action"], "immediate_stop")
        self.assertIn("stop", result["response"].lower())
    
    def test_change_emotional_state(self):
        """Test changing emotional state."""
        self.engine.change_emotional_state(EmotionalState.AROUSED)
        self.assertEqual(self.engine.config.emotional_state, EmotionalState.AROUSED)
    
    def test_change_mode(self):
        """Test changing operational mode."""
        self.engine.change_mode(OperationalMode.DOMINANT)
        self.assertEqual(self.engine.config.operational_mode, OperationalMode.DOMINANT)
    
    def test_get_state(self):
        """Test getting current state."""
        state = self.engine.get_state()
        
        self.assertIn("emotional_state", state)
        self.assertIn("operational_mode", state)
        self.assertIn("intensity", state)


if __name__ == '__main__':
    unittest.main()
