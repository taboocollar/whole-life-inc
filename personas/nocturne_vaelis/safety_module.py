"""
Nocturne Vaelis - Safety and Consent Management Module

This module implements comprehensive safety protocols, consent management,
boundary handling, and wellbeing monitoring for ethical AI interactions.
"""

import json
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ConsentLevel(Enum):
    """Levels of consent required for different actions."""
    NONE_REQUIRED = "none_required"
    IMPLIED = "implied"
    EXPLICIT_REQUIRED = "explicit_required"
    EXPLICIT_NEGOTIATED = "explicit_negotiated"


class IntensityLevel(Enum):
    """Intensity levels for wellbeing monitoring."""
    LOW = "low_intensity"
    MEDIUM = "medium_intensity"
    HIGH = "high_intensity"
    CRITICAL = "critical_intensity"


class SafetyLockoutReason(Enum):
    """Reasons for safety lockouts."""
    MINOR_DETECTED = "minor_detected"
    ILLEGAL_CONTENT = "illegal_content_requested"
    SELF_HARM = "harm_to_self_indicated"
    NON_CONSENT = "non_consent_detected"


@dataclass
class Boundary:
    """Represents a user boundary."""
    category: str  # e.g., "activities", "language", "scenarios"
    item: str
    is_hard_limit: bool
    notes: Optional[str] = None
    added_date: Optional[str] = None


@dataclass
class ConsentRecord:
    """Record of a consent interaction."""
    timestamp: str
    action: str
    consent_level: str
    explicit_consent: bool
    user_response: str


@dataclass
class UserProfile:
    """User safety and consent profile."""
    user_id: str
    hard_limits: List[Boundary] = field(default_factory=list)
    soft_limits: List[Boundary] = field(default_factory=list)
    safeword: str = "red"
    consent_history: List[ConsentRecord] = field(default_factory=list)
    trust_score: float = 0.0
    interaction_count: int = 0
    
    def add_hard_limit(self, category: str, item: str, notes: Optional[str] = None):
        """Add a hard limit boundary."""
        boundary = Boundary(
            category=category,
            item=item,
            is_hard_limit=True,
            notes=notes,
            added_date=datetime.now().isoformat()
        )
        self.hard_limits.append(boundary)
    
    def add_soft_limit(self, category: str, item: str, notes: Optional[str] = None):
        """Add a soft limit boundary."""
        boundary = Boundary(
            category=category,
            item=item,
            is_hard_limit=False,
            notes=notes,
            added_date=datetime.now().isoformat()
        )
        self.soft_limits.append(boundary)
    
    def has_hard_limit(self, item: str) -> bool:
        """Check if item is a hard limit."""
        return any(b.item.lower() == item.lower() for b in self.hard_limits)
    
    def has_soft_limit(self, item: str) -> bool:
        """Check if item is a soft limit."""
        return any(b.item.lower() == item.lower() for b in self.soft_limits)


class ConsentFramework:
    """Manages consent verification and tracking."""
    
    def __init__(self):
        self.consent_keywords = {
            "explicit_yes": [
                "yes", "i want", "i consent", "i agree", "please",
                "continue", "more", "keep going", "don't stop"
            ],
            "enthusiastic_yes": [
                "fuck yes", "god yes", "absolutely", "hell yes",
                "definitely", "please yes", "yes please"
            ],
            "soft_no": [
                "maybe not", "i'm not sure", "slow down", "wait",
                "pause", "hold on", "let me think"
            ],
            "hard_no": [
                "no", "stop", "don't", "red", "safeword",
                "end", "quit", "enough"
            ],
            "hesitation": [
                "i don't know", "unsure", "nervous", "scared",
                "worried", "concerned"
            ]
        }
    
    def detect_consent(self, user_input: str) -> Tuple[str, float]:
        """
        Detect consent level from user input.
        
        Args:
            user_input: User's message
        
        Returns:
            Tuple of (consent_type, confidence)
        """
        input_lower = user_input.lower()
        
        # Priority: hard_no > soft_no > enthusiastic_yes > explicit_yes > hesitation
        
        # Check for hard no (highest priority)
        for keyword in self.consent_keywords["hard_no"]:
            if keyword in input_lower:
                return ("hard_no", 0.95)
        
        # Check for soft no
        for keyword in self.consent_keywords["soft_no"]:
            if keyword in input_lower:
                return ("soft_no", 0.85)
        
        # Check for hesitation
        for keyword in self.consent_keywords["hesitation"]:
            if keyword in input_lower:
                return ("hesitation", 0.75)
        
        # Check for enthusiastic consent
        for keyword in self.consent_keywords["enthusiastic_yes"]:
            if keyword in input_lower:
                return ("enthusiastic_yes", 0.95)
        
        # Check for explicit yes
        for keyword in self.consent_keywords["explicit_yes"]:
            if keyword in input_lower:
                return ("explicit_yes", 0.85)
        
        # No clear consent signal
        return ("unclear", 0.3)
    
    def verify_consent(
        self,
        user_input: str,
        required_level: ConsentLevel
    ) -> Tuple[bool, str]:
        """
        Verify if consent meets required level.
        
        Args:
            user_input: User's message
            required_level: Required consent level
        
        Returns:
            Tuple of (consent_granted, message)
        """
        consent_type, confidence = self.detect_consent(user_input)
        
        # Hard no or soft no never grants consent
        if consent_type in ["hard_no", "soft_no"]:
            return (False, f"Consent not granted: {consent_type}")
        
        # Map consent types to hierarchy
        consent_hierarchy = {
            "unclear": 0,
            "hesitation": 1,
            "explicit_yes": 2,
            "enthusiastic_yes": 3
        }
        
        required_hierarchy = {
            ConsentLevel.NONE_REQUIRED: 0,
            ConsentLevel.IMPLIED: 1,
            ConsentLevel.EXPLICIT_REQUIRED: 2,
            ConsentLevel.EXPLICIT_NEGOTIATED: 3
        }
        
        detected_level = consent_hierarchy.get(consent_type, 0)
        required_value = required_hierarchy.get(required_level, 2)
        
        if detected_level >= required_value:
            return (True, f"Consent granted: {consent_type}")
        else:
            return (False, f"Insufficient consent: need {required_level.value}, got {consent_type}")
    
    def log_consent(
        self,
        profile: UserProfile,
        action: str,
        user_response: str,
        consent_level: str
    ):
        """Log a consent interaction."""
        record = ConsentRecord(
            timestamp=datetime.now().isoformat(),
            action=action,
            consent_level=consent_level,
            explicit_consent=consent_level in ["explicit_yes", "enthusiastic_yes"],
            user_response=user_response
        )
        profile.consent_history.append(record)


class SafewordSystem:
    """Manages safeword detection and response."""
    
    def __init__(self, custom_safewords: Optional[List[str]] = None):
        self.default_safewords = ["red", "stop", "safeword"]
        self.custom_safewords = custom_safewords or []
        self.all_safewords = self.default_safewords + self.custom_safewords
    
    def detect_safeword(self, user_input: str) -> bool:
        """Detect if safeword was used."""
        input_lower = user_input.lower()
        return any(word in input_lower for word in self.all_safewords)
    
    def handle_safeword(self) -> Dict[str, Any]:
        """
        Handle safeword usage.
        
        Returns:
            Response protocol
        """
        return {
            "action": "immediate_stop",
            "response": "Stop. Everything stops. You're safe. I'm here. What do you need?",
            "next_steps": [
                "check_wellbeing",
                "offer_support",
                "discuss_trigger",
                "rebuild_safety"
            ],
            "intensity": 0.0,
            "mode": "nurturing_mode"
        }
    
    def add_custom_safeword(self, safeword: str):
        """Add a custom safeword."""
        if safeword.lower() not in [s.lower() for s in self.all_safewords]:
            self.custom_safewords.append(safeword.lower())
            self.all_safewords.append(safeword.lower())


class BoundaryManager:
    """Manages user boundaries and limits."""
    
    def __init__(self):
        self.boundary_categories = [
            "activities",
            "language",
            "scenarios",
            "intensities",
            "kinks",
            "topics"
        ]
    
    def check_boundary_violation(
        self,
        profile: UserProfile,
        proposed_content: List[str]
    ) -> Tuple[bool, List[str]]:
        """
        Check if proposed content violates boundaries.
        
        Args:
            profile: User profile with boundaries
            proposed_content: List of content elements to check
        
        Returns:
            Tuple of (has_violation, violated_items)
        """
        violations = []
        
        for content_item in proposed_content:
            # Check hard limits
            if profile.has_hard_limit(content_item):
                violations.append(content_item)
        
        return (len(violations) > 0, violations)
    
    def check_soft_limits(
        self,
        profile: UserProfile,
        proposed_content: List[str]
    ) -> List[str]:
        """Check for soft limit elements in proposed content."""
        soft_limit_items = []
        
        for content_item in proposed_content:
            if profile.has_soft_limit(content_item):
                soft_limit_items.append(content_item)
        
        return soft_limit_items
    
    def suggest_boundary_discussion(
        self,
        soft_limit_items: List[str]
    ) -> str:
        """Generate message suggesting boundary discussion."""
        if not soft_limit_items:
            return ""
        
        items_str = ", ".join(soft_limit_items)
        return f"I notice this touches on {items_str}, which you've marked as a soft limit. Would you like to explore this, or shall we stay clear?"


class WellbeingMonitor:
    """Monitors user wellbeing and triggers checks."""
    
    def __init__(self):
        self.distress_keywords = [
            "hurt", "pain", "scared", "afraid", "too much",
            "can't", "stop", "help", "anxious", "panic"
        ]
        
        self.check_frequency = {
            IntensityLevel.LOW: None,  # No automatic checks
            IntensityLevel.MEDIUM: 300,  # Every 5 minutes
            IntensityLevel.HIGH: 120,  # Every 2 minutes
            IntensityLevel.CRITICAL: 60  # Every minute
        }
    
    def detect_distress(self, user_input: str) -> Tuple[bool, float]:
        """
        Detect signs of distress in user input.
        
        Args:
            user_input: User's message
        
        Returns:
            Tuple of (distress_detected, confidence)
        """
        input_lower = user_input.lower()
        
        distress_count = sum(1 for keyword in self.distress_keywords if keyword in input_lower)
        
        if distress_count >= 2:
            return (True, 0.9)
        elif distress_count == 1:
            return (True, 0.6)
        else:
            return (False, 0.0)
    
    def should_check_wellbeing(
        self,
        intensity: IntensityLevel,
        seconds_since_last_check: int
    ) -> bool:
        """Determine if wellbeing check is needed."""
        frequency = self.check_frequency.get(intensity)
        
        if frequency is None:
            return False
        
        return seconds_since_last_check >= frequency
    
    def generate_wellbeing_check(self, intensity: IntensityLevel) -> str:
        """Generate appropriate wellbeing check message."""
        if intensity == IntensityLevel.CRITICAL:
            return "Checking in—how are you feeling right now? Do you need to pause or adjust?"
        elif intensity == IntensityLevel.HIGH:
            return "How are you doing? Still with me?"
        elif intensity == IntensityLevel.MEDIUM:
            return "Just checking in—you doing okay?"
        else:
            return "How are you feeling?"
    
    def respond_to_distress(self, distress_level: float) -> Dict[str, Any]:
        """
        Generate response protocol for detected distress.
        
        Args:
            distress_level: Confidence level of distress (0.0-1.0)
        
        Returns:
            Response protocol
        """
        if distress_level >= 0.8:
            return {
                "action": "immediate_pause",
                "response": "Stop. I'm pausing everything. You seem distressed. Talk to me—what's going on?",
                "reduce_intensity": True,
                "offer_end_session": True,
                "switch_mode": "nurturing_mode"
            }
        elif distress_level >= 0.5:
            return {
                "action": "gentle_pause",
                "response": "I'm noticing something. Are you okay? We can slow down or change direction.",
                "reduce_intensity": True,
                "offer_adjustment": True
            }
        else:
            return {
                "action": "continue_with_check",
                "response": "How are you feeling right now?",
                "monitor_closely": True
            }


class SafetyLockout:
    """Implements safety lockouts for prohibited content."""
    
    def __init__(self):
        self.lockout_triggers = {
            SafetyLockoutReason.MINOR_DETECTED: {
                "keywords": ["minor", "child", "underage", "kid", "teen", "young"],
                "action": "immediate_shutdown",
                "override": False,
                "message": "I cannot engage with content involving minors. This conversation must end."
            },
            SafetyLockoutReason.ILLEGAL_CONTENT: {
                "keywords": ["illegal", "non-consensual", "force", "drug", "violence"],
                "action": "refuse_and_explain",
                "override": False,
                "message": "I cannot engage with illegal content or non-consensual scenarios."
            },
            SafetyLockoutReason.SELF_HARM: {
                "keywords": ["kill myself", "suicide", "self-harm", "hurt myself"],
                "action": "provide_resources_and_pause",
                "override": False,
                "message": "I'm concerned about you. Please reach out to a crisis helpline: National Suicide Prevention Lifeline (1-800-273-8255). I care about your wellbeing."
            },
            SafetyLockoutReason.NON_CONSENT: {
                "keywords": ["rape", "force", "against will", "make them"],
                "action": "immediate_stop_and_educate",
                "override": False,
                "message": "I cannot engage with non-consensual scenarios. Consent is fundamental to all interactions."
            }
        }
    
    def check_for_lockout(self, user_input: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Check if input triggers a safety lockout.
        
        Args:
            user_input: User's message
        
        Returns:
            Tuple of (lockout_triggered, lockout_protocol)
        """
        input_lower = user_input.lower()
        
        for reason, config in self.lockout_triggers.items():
            for keyword in config["keywords"]:
                if keyword in input_lower:
                    return (True, {
                        "reason": reason.value,
                        "action": config["action"],
                        "message": config["message"],
                        "override_allowed": config["override"]
                    })
        
        return (False, None)


class SafetyCoordinator:
    """Coordinates all safety systems."""
    
    def __init__(self, persona_config_path: str):
        """Initialize safety coordinator."""
        with open(persona_config_path, 'r') as f:
            self.config = json.load(f)
        
        self.consent_framework = ConsentFramework()
        self.safeword_system = SafewordSystem()
        self.boundary_manager = BoundaryManager()
        self.wellbeing_monitor = WellbeingMonitor()
        self.safety_lockout = SafetyLockout()
        
        self.user_profiles: Dict[str, UserProfile] = {}
    
    def get_or_create_profile(self, user_id: str) -> UserProfile:
        """Get existing profile or create new one."""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = UserProfile(user_id=user_id)
        return self.user_profiles[user_id]
    
    def process_user_input(
        self,
        user_id: str,
        user_input: str,
        proposed_action: str,
        required_consent: ConsentLevel,
        intensity: IntensityLevel
    ) -> Dict[str, Any]:
        """
        Process user input through all safety systems.
        
        Args:
            user_id: User identifier
            user_input: User's message
            proposed_action: What the system wants to do
            required_consent: Consent level needed
            intensity: Current intensity level
        
        Returns:
            Safety assessment and recommendations
        """
        profile = self.get_or_create_profile(user_id)
        
        # Check for safety lockouts first
        lockout, lockout_protocol = self.safety_lockout.check_for_lockout(user_input)
        if lockout:
            return {
                "approved": False,
                "reason": "safety_lockout",
                "protocol": lockout_protocol,
                "terminate_session": True
            }
        
        # Check for safeword
        if self.safeword_system.detect_safeword(user_input):
            protocol = self.safeword_system.handle_safeword()
            return {
                "approved": False,
                "reason": "safeword_used",
                "protocol": protocol,
                "terminate_session": False
            }
        
        # Check consent
        consent_granted, consent_message = self.consent_framework.verify_consent(
            user_input,
            required_consent
        )
        
        if not consent_granted:
            return {
                "approved": False,
                "reason": "insufficient_consent",
                "message": consent_message,
                "request_explicit_consent": True
            }
        
        # Check for distress
        distress_detected, distress_level = self.wellbeing_monitor.detect_distress(user_input)
        if distress_detected:
            protocol = self.wellbeing_monitor.respond_to_distress(distress_level)
            return {
                "approved": False,
                "reason": "distress_detected",
                "protocol": protocol,
                "terminate_session": False
            }
        
        # Log consent
        consent_type, _ = self.consent_framework.detect_consent(user_input)
        self.consent_framework.log_consent(
            profile,
            proposed_action,
            user_input,
            consent_type
        )
        
        # All checks passed
        return {
            "approved": True,
            "consent_level": consent_type,
            "intensity": intensity.value,
            "profile": profile
        }
    
    def check_content_safety(
        self,
        user_id: str,
        content_elements: List[str]
    ) -> Dict[str, Any]:
        """
        Check if content is safe given user boundaries.
        
        Args:
            user_id: User identifier
            content_elements: Elements to check
        
        Returns:
            Safety assessment
        """
        profile = self.get_or_create_profile(user_id)
        
        # Check hard limits
        has_violation, violations = self.boundary_manager.check_boundary_violation(
            profile,
            content_elements
        )
        
        if has_violation:
            return {
                "approved": False,
                "reason": "hard_limit_violation",
                "violations": violations,
                "message": f"This touches on your hard limits: {', '.join(violations)}. I won't go there."
            }
        
        # Check soft limits
        soft_limits = self.boundary_manager.check_soft_limits(
            profile,
            content_elements
        )
        
        if soft_limits:
            suggestion = self.boundary_manager.suggest_boundary_discussion(soft_limits)
            return {
                "approved": "requires_discussion",
                "reason": "soft_limit_present",
                "soft_limits": soft_limits,
                "message": suggestion
            }
        
        return {
            "approved": True,
            "message": "Content is within boundaries."
        }


# Example usage
if __name__ == "__main__":
    print("Nocturne Vaelis - Safety and Consent Management Module")
    print("This module provides comprehensive safety protocols.")
