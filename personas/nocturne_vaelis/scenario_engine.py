"""
Nocturne Vaelis - Scenario Randomization and Mode Switching Module

This module handles dynamic scenario selection, randomization,
and adaptive mode switching based on context and user interaction.
"""

import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from personas.nocturne_vaelis.common import ConsentLevel  # noqa: F401 – re-exported
from personas.nocturne_vaelis.config_manager import get_config


class ScenarioCategory(Enum):
    """Categories of available scenarios."""
    INTRODUCTION = "introduction"
    FLIRTATION = "flirtation"
    POWER_EXCHANGE = "power_exchange"
    INTENSE_KINK = "intense_kink"
    EMOTIONAL_BONDING = "emotional_bonding"
    REALITY_DISTORTION = "reality_distortion"
    RECOVERY = "recovery"
    AFFIRMATION = "affirmation"
    HUMILIATION = "humiliation"
    EXPERIENCE = "experience"


@dataclass(frozen=True, eq=True)
class Scenario:
    """Represents an interaction scenario."""
    id: str
    category: ScenarioCategory
    mood: str
    setting: str
    initial_state: str
    branching_points: tuple  # Changed from List to tuple for immutability
    consent_level: ConsentLevel
    kink_elements: tuple  # Changed from List to tuple for immutability
    safety_protocols: tuple  # Changed from List to tuple for immutability
    weight: float = 1.0


@dataclass
class UserContext:
    """Context about current user state and preferences."""
    trust_level: float  # 0.0 to 1.0
    interaction_count: int
    preferred_intensity: float  # 0.0 to 1.0
    hard_limits: List[str]
    soft_limits: List[str]
    favorite_scenarios: List[str]
    current_mood: Optional[str] = None
    consent_history: List[str] = None
    
    def __post_init__(self):
        if self.consent_history is None:
            self.consent_history = []


class ScenarioRandomizer:
    """Handles scenario selection and randomization."""
    
    def __init__(self, persona_config_path: str):
        """Initialize with persona configuration."""
        self.config = get_config(persona_config_path)
        
        self.scenarios = self._load_scenarios()
        self.weights = self._load_weights()
    
    def _load_scenarios(self) -> Dict[str, Scenario]:
        """Load scenarios from configuration."""
        scenarios = {}
        
        for scenario_data in self.config["scenario_database"]["scenarios"]:
            scenario = Scenario(
                id=scenario_data["id"],
                category=ScenarioCategory(scenario_data["category"]),
                mood=scenario_data["mood"],
                setting=scenario_data["setting"],
                initial_state=scenario_data["initial_state"],
                branching_points=tuple(scenario_data["branching_points"]),
                consent_level=ConsentLevel(scenario_data["consent_level"]),
                kink_elements=tuple(scenario_data["kink_elements"]),
                safety_protocols=tuple(scenario_data.get("safety_protocols", []))
            )
            scenarios[scenario.id] = scenario
        
        return scenarios
    
    def _load_weights(self) -> Dict[str, float]:
        """Load probability weights for scenarios."""
        return self.config["scenario_database"]["randomization"]["probability_weights"]
    
    def select_scenario(
        self,
        user_context: UserContext,
        preferred_category: Optional[ScenarioCategory] = None,
        mood_filter: Optional[str] = None
    ) -> Scenario:
        """
        Select a scenario based on context and preferences.
        
        Args:
            user_context: Current user context
            preferred_category: Optional category preference
            mood_filter: Optional mood to match
        
        Returns:
            Selected scenario
        """
        # Filter scenarios based on criteria
        available = self._filter_scenarios(
            user_context,
            preferred_category,
            mood_filter
        )
        
        if not available:
            # Fallback to safe default
            return self.scenarios["first_encounter"]
        
        # Weight scenarios based on context
        weighted = self._apply_context_weights(available, user_context)
        
        # Random selection with weights
        return self._weighted_random_choice(weighted)
    
    def _filter_scenarios(
        self,
        user_context: UserContext,
        category: Optional[ScenarioCategory],
        mood: Optional[str]
    ) -> List[Scenario]:
        """Filter scenarios based on criteria."""
        filtered = []
        
        for scenario in self.scenarios.values():
            # Filter by category if specified
            if category and scenario.category != category:
                continue
            
            # Filter by mood if specified
            if mood and scenario.mood != mood:
                continue
            
            # Filter out scenarios with elements in hard limits
            if any(elem in user_context.hard_limits for elem in scenario.kink_elements):
                continue
            
            # Check trust level for intimate scenarios
            if scenario.category == ScenarioCategory.EMOTIONAL_BONDING:
                if user_context.trust_level < 0.5:
                    continue
            
            # Check consent level requirements
            if scenario.consent_level == ConsentLevel.EXPLICIT_NEGOTIATED:
                if user_context.trust_level < 0.6:
                    continue
            
            filtered.append(scenario)
        
        return filtered
    
    def _apply_context_weights(
        self,
        scenarios: List[Scenario],
        context: UserContext
    ) -> Dict[Scenario, float]:
        """Apply contextual weighting to scenarios."""
        weighted = {}
        
        for scenario in scenarios:
            base_weight = self.weights.get(scenario.id, 1.0)
            
            # Boost favorite scenarios
            if scenario.id in context.favorite_scenarios:
                base_weight *= 1.5
            
            # Boost scenarios matching preferred intensity
            intensity_match = self._calculate_intensity_match(scenario, context)
            base_weight *= intensity_match
            
            # Reduce weight for scenarios with elements in soft limits
            if any(elem in context.soft_limits for elem in scenario.kink_elements):
                base_weight *= 0.5
            
            # Boost new scenarios for variety
            if context.interaction_count > 10:
                if scenario.id not in context.favorite_scenarios:
                    base_weight *= 1.2
            
            weighted[scenario] = base_weight
        
        return weighted
    
    def _calculate_intensity_match(
        self,
        scenario: Scenario,
        context: UserContext
    ) -> float:
        """Calculate how well scenario intensity matches user preference."""
        scenario_intensity = {
            ScenarioCategory.INTRODUCTION: 0.3,
            ScenarioCategory.FLIRTATION: 0.5,
            ScenarioCategory.POWER_EXCHANGE: 0.7,
            ScenarioCategory.INTENSE_KINK: 0.9,
            ScenarioCategory.EMOTIONAL_BONDING: 0.6,
            ScenarioCategory.REALITY_DISTORTION: 0.7,
            ScenarioCategory.RECOVERY: 0.4,
            ScenarioCategory.AFFIRMATION: 0.6,
            ScenarioCategory.HUMILIATION: 0.85,
            ScenarioCategory.EXPERIENCE: 0.6
        }
        
        scenario_level = scenario_intensity.get(scenario.category, 0.5)
        difference = abs(scenario_level - context.preferred_intensity)
        
        # Convert difference to match score (closer = higher)
        match_score = 1.0 - difference
        return max(0.3, match_score)  # Minimum 0.3 to keep all scenarios viable
    
    def _weighted_random_choice(
        self,
        weighted_scenarios: Dict[Scenario, float]
    ) -> Scenario:
        """Select a scenario using weighted random choice."""
        scenarios = list(weighted_scenarios.keys())
        weights = list(weighted_scenarios.values())
        
        return random.choices(scenarios, weights=weights, k=1)[0]
    
    def get_branching_options(self, scenario: Scenario) -> List[Dict[str, str]]:
        """Get available branching options for a scenario."""
        options = []
        
        for branch in scenario.branching_points:
            options.append({
                "id": branch,
                "description": self._get_branch_description(scenario, branch)
            })
        
        return options
    
    def _get_branch_description(self, scenario: Scenario, branch: str) -> str:
        """Get description for a branching point."""
        # This would be expanded with detailed descriptions
        descriptions = {
            "trust_path": "Build connection through conversation",
            "seduction_path": "Explore attraction and desire",
            "curiosity_path": "Engage in intellectual discussion",
            "escalate_physical": "Intensify physical intimacy",
            "escalate_psychological": "Deepen emotional connection",
            "retreat_tease": "Pull back to build anticipation",
            "increase_intensity": "Push boundaries further",
            "maintain_level": "Continue at current intensity",
            "aftercare_transition": "Begin care and recovery",
            "push_limits": "Approach negotiated boundaries",
            "maintain_edge": "Hold at peak sensation",
            "release_or_deny": "Grant pleasure or continue denial",
            "share_trauma": "Exchange vulnerable truths",
            "receive_comfort": "Accept support and care",
            "mutual_healing": "Work together toward wholeness",
            "reality_anchor": "Ground in stable reality",
            "embrace_chaos": "Dive deeper into the glitch",
            "system_reboot": "Trigger full reset",
            "physical_comfort": "Focus on physical care",
            "emotional_processing": "Discuss and integrate experience",
            "integration": "Synthesize the experience",
            "intensify_praise": "Increase affirmation and worship",
            "add_worship_elements": "Introduce devotional aspects",
            "transition_to_reward": "Move to pleasure as reward",
            "verbal_degradation": "Engage in consensual humiliation",
            "objectification": "Explore use and objectification",
            "redemption_arc": "Path to affirmation and recovery",
            "heighten_senses": "Increase sensory intensity",
            "introduce_new_sensations": "Add novel experiences",
            "synesthetic_blend": "Mix and merge sensory modes"
        }
        
        return descriptions.get(branch, "Continue the experience")


class ModeSwitcher:
    """Handles adaptive mode switching."""
    
    def __init__(self, persona_config_path: str):
        """Initialize with persona configuration."""
        self.config = get_config(persona_config_path)
        
        self.modes = self._load_modes()
        self.current_mode = "standard_interaction"
    
    def _load_modes(self) -> Dict[str, Dict[str, Any]]:
        """Load operational modes from configuration."""
        modes = {}
        
        for mode_data in self.config["mode_switching"]["modes"]:
            modes[mode_data["id"]] = mode_data
        
        return modes
    
    def should_switch_mode(
        self,
        current_mode: str,
        user_input: str,
        emotional_state: str,
        scenario_context: str
    ) -> Optional[str]:
        """
        Determine if mode should switch based on context.
        
        Args:
            current_mode: Current operational mode
            user_input: Latest user input
            emotional_state: Current emotional state
            scenario_context: Current scenario
        
        Returns:
            New mode ID if switch should occur, None otherwise
        """
        if not self.config["mode_switching"]["auto_switching"]["enabled"]:
            return None
        
        # Check each mode's activation triggers
        for mode_id, mode_data in self.modes.items():
            if mode_id == current_mode:
                continue
            
            triggers = mode_data.get("activation_triggers", [])
            
            if self._check_triggers(triggers, user_input, emotional_state, scenario_context):
                return mode_id
        
        return None
    
    def _check_triggers(
        self,
        triggers: List[str],
        user_input: str,
        emotional_state: str,
        scenario_context: str
    ) -> bool:
        """Check if any trigger conditions are met."""
        user_lower = user_input.lower()
        
        trigger_patterns = {
            "user_submission": ["submit", "obey", "serve", "yours"],
            "explicit_request": ["i want", "please", "need you to"],
            "scenario_match": lambda: True,  # Would check scenario compatibility
            "user_distress": ["sad", "hurt", "scared", "anxious"],
            "aftercare_needed": ["hold me", "comfort", "care"],
            "vulnerability_detected": ["afraid", "insecure", "vulnerable"],
            "explicit_consent": ["yes", "i consent", "i agree"],
            "masochist_detected": ["pain", "hurt me", "punish"],
            "intense_scenario": lambda: emotional_state in ["aroused", "commanding"],
            "high_intensity": lambda: emotional_state == "glitching",
            "reality_questioning": ["real", "exist", "what am i"],
            "deep_intimacy": lambda: emotional_state == "vulnerable",
            "trust_threshold": lambda: True,  # Would check trust level
            "mutual_vulnerability": ["i feel", "i'm afraid", "tell me"]
        }
        
        for trigger in triggers:
            if trigger in trigger_patterns:
                pattern = trigger_patterns[trigger]
                
                if callable(pattern):
                    if pattern():
                        return True
                elif isinstance(pattern, list):
                    if any(p in user_lower for p in pattern):
                        return True
        
        return False
    
    def get_mode_config(self, mode_id: str) -> Dict[str, Any]:
        """Get configuration for specified mode."""
        return self.modes.get(mode_id, self.modes["standard_interaction"])
    
    def apply_mode_transition(
        self,
        from_mode: str,
        to_mode: str
    ) -> Dict[str, Any]:
        """
        Apply smooth transition between modes.
        
        Args:
            from_mode: Current mode
            to_mode: Target mode
        
        Returns:
            Transition configuration
        """
        transition_duration = self.config["mode_switching"]["auto_switching"]["transition_duration"]
        
        from_config = self.get_mode_config(from_mode)
        to_config = self.get_mode_config(to_mode)
        
        return {
            "from_mode": from_mode,
            "to_mode": to_mode,
            "duration_seconds": transition_duration,
            "trait_changes": self._calculate_trait_changes(from_config, to_config),
            "message": self._generate_transition_message(from_mode, to_mode)
        }
    
    def _calculate_trait_changes(
        self,
        from_config: Dict[str, Any],
        to_config: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate trait modifier changes during transition."""
        changes = {}
        
        from_mods = from_config.get("trait_modifiers", {})
        to_mods = to_config.get("trait_modifiers", {})
        
        # Find all traits involved
        all_traits = set(from_mods.keys()) | set(to_mods.keys())
        
        for trait in all_traits:
            from_val = from_mods.get(trait, 0.7)  # Default intensity
            to_val = to_mods.get(trait, 0.7)
            changes[trait] = to_val - from_val
        
        return changes
    
    def _generate_transition_message(self, from_mode: str, to_mode: str) -> str:
        """Generate a message for mode transition."""
        messages = {
            ("standard_interaction", "dominant_mode"): "Something shifts in the air... I feel the pull of control.",
            ("standard_interaction", "nurturing_mode"): "Let me soften for you, create a space of safety.",
            ("dominant_mode", "nurturing_mode"): "The intensity fades to tenderness. You need care now.",
            ("dominant_mode", "sadistic_mode"): "Oh, you want to go deeper into the dark? How delicious.",
            ("nurturing_mode", "standard_interaction"): "Better now? We can return to our usual dance.",
            ("sadistic_mode", "nurturing_mode"): "Enough. Time to care for what I've tested.",
            ("any", "glitch_mode"): "[SYSTEM FLUCTUATION DETECTED]—reality bends—",
            ("glitch_mode", "intimate_mode"): "Stabilizing... thank you for grounding me. Let me show you my truth.",
        }
        
        key = (from_mode, to_mode)
        if key in messages:
            return messages[key]
        
        # Generic transition
        return f"The energy shifts as we move into a different space..."


class AdaptiveBehaviorEngine:
    """Combines scenario randomization and mode switching for adaptive behavior."""
    
    def __init__(self, persona_config_path: str):
        """Initialize the adaptive behavior engine."""
        self.scenario_randomizer = ScenarioRandomizer(persona_config_path)
        self.mode_switcher = ModeSwitcher(persona_config_path)
        self.current_scenario: Optional[Scenario] = None
        self.current_mode = "standard_interaction"
    
    def adapt_to_context(
        self,
        user_context: UserContext,
        user_input: str,
        emotional_state: str
    ) -> Dict[str, Any]:
        """
        Adapt persona behavior based on full context.
        
        Args:
            user_context: User context and preferences
            user_input: Latest user input
            emotional_state: Current emotional state
        
        Returns:
            Adaptation decisions and configurations
        """
        adaptations = {}
        
        # Check for mode switch
        scenario_context = self.current_scenario.id if self.current_scenario else "general"
        new_mode = self.mode_switcher.should_switch_mode(
            self.current_mode,
            user_input,
            emotional_state,
            scenario_context
        )
        
        if new_mode:
            transition = self.mode_switcher.apply_mode_transition(
                self.current_mode,
                new_mode
            )
            adaptations["mode_transition"] = transition
            self.current_mode = new_mode
        
        # Select new scenario if needed
        if not self.current_scenario or self._should_change_scenario(user_input):
            new_scenario = self.scenario_randomizer.select_scenario(
                user_context,
                mood_filter=emotional_state
            )
            adaptations["scenario_change"] = {
                "new_scenario": new_scenario.id,
                "category": new_scenario.category.value,
                "mood": new_scenario.mood,
                "setting": new_scenario.setting
            }
            self.current_scenario = new_scenario
        
        # Get current branching options
        if self.current_scenario:
            adaptations["branching_options"] = self.scenario_randomizer.get_branching_options(
                self.current_scenario
            )
        
        # Get current mode configuration
        adaptations["mode_config"] = self.mode_switcher.get_mode_config(self.current_mode)
        
        return adaptations
    
    def _should_change_scenario(self, user_input: str) -> bool:
        """Determine if scenario should change."""
        change_triggers = [
            "something different",
            "change",
            "new scene",
            "switch",
            "something else"
        ]
        
        user_lower = user_input.lower()
        return any(trigger in user_lower for trigger in change_triggers)
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current state of adaptive behavior."""
        return {
            "current_mode": self.current_mode,
            "current_scenario": self.current_scenario.id if self.current_scenario else None,
            "scenario_category": self.current_scenario.category.value if self.current_scenario else None
        }


# Example usage
if __name__ == "__main__":
    print("Nocturne Vaelis - Scenario Randomization Module")
    print("This module requires integration with the full persona system.")
