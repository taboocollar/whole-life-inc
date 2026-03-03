"""
Unit tests for Nocturne Vaelis Scenario Engine
"""

import unittest
import json
import os
from personas.nocturne_vaelis.scenario_engine import (
    ScenarioRandomizer,
    ModeSwitcher,
    AdaptiveBehaviorEngine,
    UserContext,
    ScenarioCategory,
    ConsentLevel
)


class TestScenarioRandomizer(unittest.TestCase):
    """Test scenario randomization."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test configuration."""
        cls.config_path = "/tmp/test_scenario_config.json"
        
        config = {
            "scenario_database": {
                "scenarios": [
                    {
                        "id": "test_scenario_1",
                        "category": "introduction",
                        "mood": "serene",
                        "setting": "test",
                        "initial_state": "serene",
                        "branching_points": ["path1", "path2"],
                        "consent_level": "none_required",
                        "kink_elements": [],
                        "safety_protocols": []
                    },
                    {
                        "id": "test_scenario_2",
                        "category": "power_exchange",
                        "mood": "commanding",
                        "setting": "test",
                        "initial_state": "commanding",
                        "branching_points": ["path1", "path2"],
                        "consent_level": "explicit_required",
                        "kink_elements": ["dominance"],
                        "safety_protocols": ["safeword_active"]
                    }
                ],
                "randomization": {
                    "enabled": True,
                    "probability_weights": {
                        "test_scenario_1": 0.5,
                        "test_scenario_2": 0.5
                    }
                }
            },
            "mode_switching": {
                "modes": []
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
        self.randomizer = ScenarioRandomizer(self.config_path)
    
    def test_load_scenarios(self):
        """Test scenario loading."""
        self.assertEqual(len(self.randomizer.scenarios), 2)
        self.assertIn("test_scenario_1", self.randomizer.scenarios)
    
    def test_select_scenario(self):
        """Test scenario selection."""
        context = UserContext(
            trust_level=0.5,
            interaction_count=5,
            preferred_intensity=0.5,
            hard_limits=[],
            soft_limits=[],
            favorite_scenarios=[]
        )
        
        scenario = self.randomizer.select_scenario(context)
        self.assertIsNotNone(scenario)
        self.assertIn(scenario.id, ["test_scenario_1", "test_scenario_2"])
    
    def test_filter_by_category(self):
        """Test filtering scenarios by category."""
        context = UserContext(
            trust_level=0.5,
            interaction_count=5,
            preferred_intensity=0.5,
            hard_limits=[],
            soft_limits=[],
            favorite_scenarios=[]
        )
        
        scenario = self.randomizer.select_scenario(
            context,
            preferred_category=ScenarioCategory.INTRODUCTION
        )
        self.assertEqual(scenario.category, ScenarioCategory.INTRODUCTION)
    
    def test_filter_by_hard_limits(self):
        """Test filtering out scenarios with hard limit elements."""
        context = UserContext(
            trust_level=0.5,
            interaction_count=5,
            preferred_intensity=0.5,
            hard_limits=["dominance"],
            soft_limits=[],
            favorite_scenarios=[]
        )
        
        scenario = self.randomizer.select_scenario(context)
        # Should not select scenario with dominance
        self.assertNotIn("dominance", scenario.kink_elements)
    
    def test_get_branching_options(self):
        """Test getting branching options."""
        scenario = self.randomizer.scenarios["test_scenario_1"]
        options = self.randomizer.get_branching_options(scenario)
        
        self.assertEqual(len(options), 2)
        self.assertTrue(all("id" in opt and "description" in opt for opt in options))


class TestModeSwitcher(unittest.TestCase):
    """Test mode switching functionality."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test configuration."""
        cls.config_path = "/tmp/test_mode_config.json"
        
        config = {
            "mode_switching": {
                "modes": [
                    {
                        "id": "standard_interaction",
                        "description": "Standard mode",
                        "trait_modifiers": {},
                        "default": True
                    },
                    {
                        "id": "dominant_mode",
                        "description": "Dominant mode",
                        "trait_modifiers": {"dominant": 0.95},
                        "activation_triggers": ["user_submission"]
                    },
                    {
                        "id": "nurturing_mode",
                        "description": "Nurturing mode",
                        "trait_modifiers": {"protective": 0.90},
                        "activation_triggers": ["user_distress"]
                    }
                ],
                "auto_switching": {
                    "enabled": True,
                    "transition_duration": 20
                }
            },
            "scenario_database": {
                "scenarios": []
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
        self.switcher = ModeSwitcher(self.config_path)
    
    def test_load_modes(self):
        """Test mode loading."""
        self.assertEqual(len(self.switcher.modes), 3)
        self.assertIn("standard_interaction", self.switcher.modes)
    
    def test_should_switch_mode(self):
        """Test mode switch detection."""
        # User submission should trigger dominant mode
        new_mode = self.switcher.should_switch_mode(
            current_mode="standard_interaction",
            user_input="I want to submit to you",
            emotional_state="serene",
            scenario_context="general"
        )
        self.assertEqual(new_mode, "dominant_mode")
    
    def test_should_switch_to_nurturing(self):
        """Test switch to nurturing mode on distress."""
        new_mode = self.switcher.should_switch_mode(
            current_mode="dominant_mode",
            user_input="I'm scared and hurt",
            emotional_state="commanding",
            scenario_context="general"
        )
        self.assertEqual(new_mode, "nurturing_mode")
    
    def test_get_mode_config(self):
        """Test getting mode configuration."""
        config = self.switcher.get_mode_config("dominant_mode")
        self.assertEqual(config["id"], "dominant_mode")
        self.assertIn("trait_modifiers", config)
    
    def test_apply_mode_transition(self):
        """Test applying mode transition."""
        transition = self.switcher.apply_mode_transition(
            "standard_interaction",
            "dominant_mode"
        )
        
        self.assertEqual(transition["from_mode"], "standard_interaction")
        self.assertEqual(transition["to_mode"], "dominant_mode")
        self.assertIn("trait_changes", transition)
        self.assertIn("message", transition)


class TestAdaptiveBehaviorEngine(unittest.TestCase):
    """Test adaptive behavior engine."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test configuration."""
        cls.config_path = "/tmp/test_adaptive_config.json"
        
        config = {
            "scenario_database": {
                "scenarios": [
                    {
                        "id": "test_scenario",
                        "category": "introduction",
                        "mood": "serene",
                        "setting": "test",
                        "initial_state": "serene",
                        "branching_points": ["path1"],
                        "consent_level": "none_required",
                        "kink_elements": [],
                        "safety_protocols": []
                    }
                ],
                "randomization": {
                    "enabled": True,
                    "probability_weights": {"test_scenario": 1.0}
                }
            },
            "mode_switching": {
                "modes": [
                    {
                        "id": "standard_interaction",
                        "trait_modifiers": {},
                        "default": True
                    }
                ],
                "auto_switching": {
                    "enabled": True,
                    "transition_duration": 20
                }
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
        self.engine = AdaptiveBehaviorEngine(self.config_path)
    
    def test_initialization(self):
        """Test engine initialization."""
        self.assertIsNotNone(self.engine.scenario_randomizer)
        self.assertIsNotNone(self.engine.mode_switcher)
    
    def test_adapt_to_context(self):
        """Test context adaptation."""
        context = UserContext(
            trust_level=0.5,
            interaction_count=5,
            preferred_intensity=0.5,
            hard_limits=[],
            soft_limits=[],
            favorite_scenarios=[]
        )
        
        adaptations = self.engine.adapt_to_context(
            user_context=context,
            user_input="Hello",
            emotional_state="serene"
        )
        
        self.assertIn("mode_config", adaptations)
        self.assertIn("branching_options", adaptations)
    
    def test_get_current_state(self):
        """Test getting current state."""
        state = self.engine.get_current_state()
        
        self.assertIn("current_mode", state)
        self.assertIn("current_scenario", state)


class TestUserContext(unittest.TestCase):
    """Test user context functionality."""
    
    def test_user_context_creation(self):
        """Test creating user context."""
        context = UserContext(
            trust_level=0.5,
            interaction_count=10,
            preferred_intensity=0.7,
            hard_limits=["item1"],
            soft_limits=["item2"],
            favorite_scenarios=["scenario1"]
        )
        
        self.assertEqual(context.trust_level, 0.5)
        self.assertEqual(context.interaction_count, 10)
        self.assertEqual(len(context.hard_limits), 1)
        self.assertIsInstance(context.consent_history, list)


if __name__ == '__main__':
    unittest.main()
