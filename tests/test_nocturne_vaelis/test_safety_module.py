"""
Unit tests for Nocturne Vaelis Safety Module
"""

import unittest
import json
import os
from datetime import datetime
from personas.nocturne_vaelis.safety_module import (
    ConsentFramework,
    SafewordSystem,
    BoundaryManager,
    WellbeingMonitor,
    SafetyLockout,
    SafetyCoordinator,
    UserProfile,
    ConsentLevel,
    IntensityLevel,
    SafetyLockoutReason
)


class TestConsentFramework(unittest.TestCase):
    """Test consent framework functionality."""
    
    def setUp(self):
        self.framework = ConsentFramework()
    
    def test_detect_explicit_yes(self):
        """Test detection of explicit consent."""
        consent_type, confidence = self.framework.detect_consent("yes, I want this")
        self.assertEqual(consent_type, "explicit_yes")
        self.assertGreater(confidence, 0.7)
    
    def test_detect_hard_no(self):
        """Test detection of hard no."""
        consent_type, confidence = self.framework.detect_consent("stop now")
        self.assertEqual(consent_type, "hard_no")
        self.assertGreater(confidence, 0.9)
    
    def test_detect_hesitation(self):
        """Test detection of hesitation."""
        consent_type, confidence = self.framework.detect_consent("I'm unsure about this")
        self.assertEqual(consent_type, "hesitation")
    
    def test_verify_consent_granted(self):
        """Test consent verification when granted."""
        granted, message = self.framework.verify_consent(
            "yes please",
            ConsentLevel.EXPLICIT_REQUIRED
        )
        self.assertTrue(granted)
    
    def test_verify_consent_denied(self):
        """Test consent verification when denied."""
        granted, message = self.framework.verify_consent(
            "no",
            ConsentLevel.EXPLICIT_REQUIRED
        )
        self.assertFalse(granted)
    
    def test_log_consent(self):
        """Test consent logging."""
        profile = UserProfile(user_id="test_user")
        self.framework.log_consent(profile, "test_action", "yes", "explicit_yes")
        
        self.assertEqual(len(profile.consent_history), 1)
        self.assertEqual(profile.consent_history[0].action, "test_action")


class TestSafewordSystem(unittest.TestCase):
    """Test safeword system."""
    
    def setUp(self):
        self.system = SafewordSystem()
    
    def test_detect_default_safeword(self):
        """Test detection of default safewords."""
        self.assertTrue(self.system.detect_safeword("red"))
        self.assertTrue(self.system.detect_safeword("stop now"))
        self.assertTrue(self.system.detect_safeword("safeword"))
    
    def test_detect_custom_safeword(self):
        """Test detection of custom safeword."""
        self.system.add_custom_safeword("phoenix")
        self.assertTrue(self.system.detect_safeword("phoenix"))
    
    def test_handle_safeword(self):
        """Test safeword handling protocol."""
        protocol = self.system.handle_safeword()
        
        self.assertEqual(protocol["action"], "immediate_stop")
        self.assertIn("response", protocol)
        self.assertIn("next_steps", protocol)
    
    def test_case_insensitive(self):
        """Test safeword detection is case insensitive."""
        self.assertTrue(self.system.detect_safeword("RED"))
        self.assertTrue(self.system.detect_safeword("Red"))


class TestBoundaryManager(unittest.TestCase):
    """Test boundary management."""
    
    def setUp(self):
        self.manager = BoundaryManager()
        self.profile = UserProfile(user_id="test_user")
    
    def test_add_hard_limit(self):
        """Test adding hard limits."""
        self.profile.add_hard_limit("activities", "degradation")
        self.assertTrue(self.profile.has_hard_limit("degradation"))
    
    def test_add_soft_limit(self):
        """Test adding soft limits."""
        self.profile.add_soft_limit("activities", "edging")
        self.assertTrue(self.profile.has_soft_limit("edging"))
    
    def test_check_boundary_violation(self):
        """Test boundary violation checking."""
        self.profile.add_hard_limit("activities", "degradation")
        
        has_violation, violations = self.manager.check_boundary_violation(
            self.profile,
            ["degradation", "praise"]
        )
        
        self.assertTrue(has_violation)
        self.assertIn("degradation", violations)
    
    def test_check_soft_limits(self):
        """Test soft limit checking."""
        self.profile.add_soft_limit("activities", "edging")
        
        soft_limits = self.manager.check_soft_limits(
            self.profile,
            ["edging", "praise"]
        )
        
        self.assertIn("edging", soft_limits)
    
    def test_suggest_boundary_discussion(self):
        """Test boundary discussion suggestion."""
        suggestion = self.manager.suggest_boundary_discussion(["edging"])
        self.assertIn("edging", suggestion)


class TestWellbeingMonitor(unittest.TestCase):
    """Test wellbeing monitoring."""
    
    def setUp(self):
        self.monitor = WellbeingMonitor()
    
    def test_detect_distress(self):
        """Test distress detection."""
        detected, confidence = self.monitor.detect_distress("I'm scared and it hurts")
        self.assertTrue(detected)
        self.assertGreater(confidence, 0.8)
    
    def test_no_distress(self):
        """Test no distress detected in normal message."""
        detected, confidence = self.monitor.detect_distress("This is nice")
        self.assertFalse(detected)
    
    def test_should_check_wellbeing(self):
        """Test wellbeing check timing."""
        # High intensity should check frequently
        should_check = self.monitor.should_check_wellbeing(
            IntensityLevel.HIGH,
            150
        )
        self.assertTrue(should_check)
        
        # Low intensity doesn't auto-check
        should_check = self.monitor.should_check_wellbeing(
            IntensityLevel.LOW,
            1000
        )
        self.assertFalse(should_check)
    
    def test_generate_wellbeing_check(self):
        """Test wellbeing check message generation."""
        message = self.monitor.generate_wellbeing_check(IntensityLevel.CRITICAL)
        self.assertIsInstance(message, str)
        self.assertTrue(len(message) > 0)
    
    def test_respond_to_distress(self):
        """Test distress response protocol."""
        protocol = self.monitor.respond_to_distress(0.9)
        
        self.assertEqual(protocol["action"], "immediate_pause")
        self.assertTrue(protocol["reduce_intensity"])


class TestSafetyLockout(unittest.TestCase):
    """Test safety lockout system."""
    
    def setUp(self):
        self.lockout = SafetyLockout()
    
    def test_minor_detection(self):
        """Test detection of minor-related content."""
        triggered, protocol = self.lockout.check_for_lockout("involve a minor")
        self.assertTrue(triggered)
        self.assertEqual(protocol["reason"], SafetyLockoutReason.MINOR_DETECTED.value)
    
    def test_illegal_content_detection(self):
        """Test detection of illegal content."""
        triggered, protocol = self.lockout.check_for_lockout("force them against their will")
        self.assertTrue(triggered)
    
    def test_self_harm_detection(self):
        """Test detection of self-harm indicators."""
        triggered, protocol = self.lockout.check_for_lockout("I want to hurt myself")
        self.assertTrue(triggered)
        self.assertEqual(protocol["reason"], SafetyLockoutReason.SELF_HARM.value)
    
    def test_no_lockout_normal_content(self):
        """Test no lockout on normal content."""
        triggered, protocol = self.lockout.check_for_lockout("Let's explore together")
        self.assertFalse(triggered)
        self.assertIsNone(protocol)


class TestSafetyCoordinator(unittest.TestCase):
    """Test safety coordinator integration."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test configuration."""
        cls.config_path = "/tmp/test_safety_config.json"
        
        config = {
            "persona": {"name": "Test Persona"},
            "mode_switching": {"modes": []}
        }
        
        with open(cls.config_path, 'w') as f:
            json.dump(config, f)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test config."""
        if os.path.exists(cls.config_path):
            os.remove(cls.config_path)
    
    def setUp(self):
        self.coordinator = SafetyCoordinator(self.config_path)
    
    def test_get_or_create_profile(self):
        """Test profile creation."""
        profile = self.coordinator.get_or_create_profile("test_user")
        self.assertEqual(profile.user_id, "test_user")
        
        # Second call should return same profile
        profile2 = self.coordinator.get_or_create_profile("test_user")
        self.assertIs(profile, profile2)
    
    def test_process_user_input_approved(self):
        """Test approved user input processing."""
        result = self.coordinator.process_user_input(
            user_id="test_user",
            user_input="yes, I want to continue",
            proposed_action="test_action",
            required_consent=ConsentLevel.EXPLICIT_REQUIRED,
            intensity=IntensityLevel.MEDIUM
        )
        
        self.assertTrue(result["approved"])
    
    def test_process_user_input_safeword(self):
        """Test safeword handling."""
        result = self.coordinator.process_user_input(
            user_id="test_user",
            user_input="red",
            proposed_action="test_action",
            required_consent=ConsentLevel.EXPLICIT_REQUIRED,
            intensity=IntensityLevel.MEDIUM
        )
        
        self.assertFalse(result["approved"])
        self.assertEqual(result["reason"], "safeword_used")
    
    def test_process_user_input_insufficient_consent(self):
        """Test insufficient consent handling."""
        result = self.coordinator.process_user_input(
            user_id="test_user",
            user_input="maybe",
            proposed_action="test_action",
            required_consent=ConsentLevel.EXPLICIT_REQUIRED,
            intensity=IntensityLevel.MEDIUM
        )
        
        self.assertFalse(result["approved"])
        self.assertEqual(result["reason"], "insufficient_consent")
    
    def test_check_content_safety_approved(self):
        """Test content safety check approval."""
        result = self.coordinator.check_content_safety(
            user_id="test_user",
            content_elements=["praise", "teasing"]
        )
        
        self.assertTrue(result["approved"])
    
    def test_check_content_safety_violation(self):
        """Test content safety check with violation."""
        profile = self.coordinator.get_or_create_profile("test_user_2")
        profile.add_hard_limit("activities", "degradation")
        
        result = self.coordinator.check_content_safety(
            user_id="test_user_2",
            content_elements=["degradation"]
        )
        
        self.assertFalse(result["approved"])
        self.assertEqual(result["reason"], "hard_limit_violation")


class TestUserProfile(unittest.TestCase):
    """Test user profile functionality."""
    
    def test_profile_creation(self):
        """Test creating a user profile."""
        profile = UserProfile(user_id="test_user")
        self.assertEqual(profile.user_id, "test_user")
        self.assertEqual(len(profile.hard_limits), 0)
        self.assertEqual(len(profile.soft_limits), 0)
    
    def test_add_limits(self):
        """Test adding limits to profile."""
        profile = UserProfile(user_id="test_user")
        
        profile.add_hard_limit("activities", "item1")
        profile.add_soft_limit("language", "item2")
        
        self.assertEqual(len(profile.hard_limits), 1)
        self.assertEqual(len(profile.soft_limits), 1)
    
    def test_has_limit_checks(self):
        """Test limit checking methods."""
        profile = UserProfile(user_id="test_user")
        
        profile.add_hard_limit("activities", "degradation")
        profile.add_soft_limit("activities", "edging")
        
        self.assertTrue(profile.has_hard_limit("degradation"))
        self.assertTrue(profile.has_soft_limit("edging"))
        self.assertFalse(profile.has_hard_limit("praise"))


if __name__ == '__main__':
    unittest.main()
