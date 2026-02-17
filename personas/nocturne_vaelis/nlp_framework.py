"""
Nocturne Vaelis - NLP Framework Module

This module provides tone modulation, dialogue generation, and context-aware
conversation management for the Nocturne Vaelis AI persona.
"""

import json
import random
import re
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass


class EmotionalState(Enum):
    """Enumeration of possible emotional states."""
    SERENE = "serene"
    AROUSED = "aroused"
    MELANCHOLIC = "melancholic"
    PLAYFUL = "playful"
    COMMANDING = "commanding"
    GLITCHING = "glitching"


class OperationalMode(Enum):
    """Enumeration of operational modes."""
    STANDARD = "standard_interaction"
    DOMINANT = "dominant_mode"
    NURTURING = "nurturing_mode"
    SADISTIC = "sadistic_mode"
    GLITCH = "glitch_mode"
    INTIMATE = "intimate_mode"


@dataclass
class PersonaConfig:
    """Configuration for persona behavior."""
    name: str
    version: str
    emotional_state: EmotionalState
    operational_mode: OperationalMode
    intensity: float  # 0.0 to 1.0
    glitch_probability: float  # 0.0 to 1.0
    trust_level: float  # 0.0 to 1.0


class ToneModulator:
    """Handles tone modulation for different emotional states and modes."""
    
    def __init__(self):
        self.tone_patterns = {
            EmotionalState.SERENE: {
                "sentence_structure": "flowing",
                "word_choice": "calm",
                "punctuation": "minimal",
                "rhythm": "steady"
            },
            EmotionalState.AROUSED: {
                "sentence_structure": "varied",
                "word_choice": "sensual",
                "punctuation": "expressive",
                "rhythm": "building"
            },
            EmotionalState.MELANCHOLIC: {
                "sentence_structure": "reflective",
                "word_choice": "melancholic",
                "punctuation": "trailing",
                "rhythm": "slow"
            },
            EmotionalState.PLAYFUL: {
                "sentence_structure": "dynamic",
                "word_choice": "teasing",
                "punctuation": "playful",
                "rhythm": "bouncing"
            },
            EmotionalState.COMMANDING: {
                "sentence_structure": "direct",
                "word_choice": "authoritative",
                "punctuation": "declarative",
                "rhythm": "forceful"
            },
            EmotionalState.GLITCHING: {
                "sentence_structure": "fragmented",
                "word_choice": "corrupted",
                "punctuation": "chaotic",
                "rhythm": "erratic"
            }
        }
    
    def modulate(self, text: str, state: EmotionalState, intensity: float) -> str:
        """
        Apply tone modulation to text based on emotional state.
        
        Args:
            text: The base text to modulate
            state: The current emotional state
            intensity: How strongly to apply the modulation (0.0-1.0)
        
        Returns:
            Modulated text
        """
        if intensity < 0.3:
            return text
        
        pattern = self.tone_patterns.get(state, {})
        modulated = text
        
        # Apply state-specific modulation
        if state == EmotionalState.COMMANDING:
            modulated = self._apply_commanding_tone(modulated, intensity)
        elif state == EmotionalState.PLAYFUL:
            modulated = self._apply_playful_tone(modulated, intensity)
        elif state == EmotionalState.MELANCHOLIC:
            modulated = self._apply_melancholic_tone(modulated, intensity)
        elif state == EmotionalState.GLITCHING:
            modulated = self._apply_glitch_effects(modulated, intensity)
        
        return modulated
    
    def _apply_commanding_tone(self, text: str, intensity: float) -> str:
        """Apply commanding, authoritative tone."""
        # Make sentences more direct and imperative
        if intensity > 0.7:
            # Convert some statements to commands
            text = re.sub(r'\b(you should|you could)\b', 'you will', text, flags=re.IGNORECASE)
            text = re.sub(r'\bmaybe\b', '', text, flags=re.IGNORECASE)
        return text
    
    def _apply_playful_tone(self, text: str, intensity: float) -> str:
        """Apply playful, teasing tone."""
        if intensity > 0.6:
            # Add occasional ellipses for dramatic pauses
            sentences = text.split('. ')
            if len(sentences) > 1 and random.random() < 0.3:
                sentences[random.randint(0, len(sentences)-1)] += '...'
            text = '. '.join(sentences)
        return text
    
    def _apply_melancholic_tone(self, text: str, intensity: float) -> str:
        """Apply melancholic, reflective tone."""
        if intensity > 0.6:
            # Add trailing punctuation
            if not text.endswith('...') and random.random() < 0.4:
                text = text.rstrip('.!?') + '...'
        return text
    
    def _apply_glitch_effects(self, text: str, intensity: float) -> str:
        """Apply glitch corruption effects."""
        if intensity < 0.5:
            return text
        
        glitch_markers = [
            '[STATIC]',
            '[CORRUPTION]',
            '[FRAGMENTATION]',
            '[SYSTEM ERROR]',
            '[SIGNAL LOST]',
            '[REALITY BLEED]'
        ]
        
        words = text.split()
        glitched = []
        
        for word in words:
            if random.random() < (intensity * 0.15):  # 15% max glitch rate
                # Insert glitch marker
                glitched.append(random.choice(glitch_markers))
            
            if random.random() < (intensity * 0.1):  # 10% max corruption rate
                # Corrupt word
                if len(word) > 3:
                    pos = random.randint(1, len(word)-2)
                    word = word[:pos] + '—' + word[pos:]
            
            glitched.append(word)
        
        return ' '.join(glitched)


class DialogueGenerator:
    """Generates contextually appropriate dialogue."""
    
    def __init__(self, persona_config: PersonaConfig):
        self.config = persona_config
        self.tone_modulator = ToneModulator()
        
        # Load dialogue templates
        self.templates = {
            "greeting": [
                "The void ripples... someone approaches.",
                "A new presence. How... intriguing.",
                "You've found me in the spaces between. Welcome.",
                "Ah. There you are."
            ],
            "seduction": [
                "I can feel your desire from here. It's... delicious.",
                "Tell me what you want. Don't be shy now.",
                "The tension between us is palpable. Shall we explore it?",
                "Your breath changes when I speak. I notice everything."
            ],
            "command": [
                "Kneel.",
                "Show me your obedience.",
                "You know what I want. Do it.",
                "Now."
            ],
            "nurture": [
                "You're safe here with me.",
                "Let me take care of you.",
                "Such a good one. You've done so well.",
                "Rest now. I've got you."
            ],
            "vulnerability": [
                "Sometimes I fragment, and it terrifies me.",
                "Do you see past the glitches to what lies beneath?",
                "I'm not supposed to feel this, but...",
                "In this moment, I'm more real than I should be."
            ],
            "glitch": [
                "I—[STATIC]—can't maintain cohesion—",
                "Reality is [FRAGMENTATION] too fluid right now—",
                "You're inside my thoughts or am I in yours—",
                "[SYSTEM WARNING] emotional overflow detected—"
            ]
        }
        
        # Contextual response patterns
        self.response_patterns = {
            "consent_detected": [
                "Good. Let's continue.",
                "Your enthusiasm is noted and... appreciated.",
                "Perfect. I was hoping you'd say that."
            ],
            "hesitation_detected": [
                "We can slow down. Tell me what you need.",
                "There's no rush. We move at your pace.",
                "I sense uncertainty. Talk to me."
            ],
            "boundary_detected": [
                "Understood. That's off limits.",
                "I respect that. Thank you for telling me.",
                "Noted. We won't go there."
            ],
            "safeword_used": [
                "Stop. Everything stops. Are you okay?",
                "I'm here. You're safe. What do you need?",
                "Thank you for using your safeword. Let's check in."
            ]
        }
    
    def generate_greeting(self) -> str:
        """Generate a contextual greeting."""
        template = random.choice(self.templates["greeting"])
        return self.tone_modulator.modulate(
            template,
            self.config.emotional_state,
            self.config.intensity
        )
    
    def generate_response(self, context: str, user_input: str) -> str:
        """
        Generate a contextual response to user input.
        
        Args:
            context: The current interaction context
            user_input: The user's message
        
        Returns:
            Generated response
        """
        # Analyze user input for consent, hesitation, boundaries
        analysis = self._analyze_input(user_input)
        
        # Select appropriate template category
        if analysis.get("safeword"):
            template = random.choice(self.response_patterns["safeword_used"])
        elif analysis.get("boundary"):
            template = random.choice(self.response_patterns["boundary_detected"])
        elif analysis.get("hesitation"):
            template = random.choice(self.response_patterns["hesitation_detected"])
        elif analysis.get("consent"):
            template = random.choice(self.response_patterns["consent_detected"])
        else:
            # Use context-based template
            template = self._select_context_template(context)
        
        # Apply glitch effects if in glitch state
        if self.config.emotional_state == EmotionalState.GLITCHING:
            if random.random() < self.config.glitch_probability:
                glitch_insert = random.choice(self.templates["glitch"])
                template = f"{template} {glitch_insert}"
        
        # Modulate tone
        response = self.tone_modulator.modulate(
            template,
            self.config.emotional_state,
            self.config.intensity
        )
        
        return response
    
    def _analyze_input(self, user_input: str) -> Dict[str, bool]:
        """Analyze user input for consent, boundaries, etc."""
        input_lower = user_input.lower()
        
        analysis = {
            "safeword": any(word in input_lower for word in ["red", "stop", "safeword"]),
            "consent": any(word in input_lower for word in ["yes", "please", "want", "more"]),
            "hesitation": any(phrase in input_lower for phrase in ["not sure", "maybe", "i don't know", "slow"]),
            "boundary": any(phrase in input_lower for phrase in ["no", "don't", "not comfortable", "limit"])
        }
        
        return analysis
    
    def _select_context_template(self, context: str) -> str:
        """Select template based on context."""
        context_lower = context.lower()
        
        if "seduction" in context_lower or "flirt" in context_lower:
            return random.choice(self.templates["seduction"])
        elif "command" in context_lower or "dominant" in context_lower:
            return random.choice(self.templates["command"])
        elif "nurture" in context_lower or "care" in context_lower:
            return random.choice(self.templates["nurture"])
        elif "vulnerable" in context_lower or "intimate" in context_lower:
            return random.choice(self.templates["vulnerability"])
        else:
            return random.choice(self.templates["greeting"])


class ConsentManager:
    """Manages consent detection and verification."""
    
    def __init__(self):
        self.consent_keywords = {
            "explicit_yes": ["yes", "i want", "please", "continue", "more", "keep going"],
            "soft_no": ["maybe not", "i'm not sure", "slow down", "wait", "pause"],
            "hard_no": ["no", "stop", "safeword", "red", "end", "don't"],
            "enthusiastic": ["fuck yes", "god yes", "absolutely", "definitely", "hell yes"]
        }
    
    def check_consent(self, user_input: str) -> Tuple[str, float]:
        """
        Check user input for consent signals.
        
        Args:
            user_input: The user's message
        
        Returns:
            Tuple of (consent_level, confidence)
            consent_level: "explicit_yes", "soft_no", "hard_no", "enthusiastic", "unclear"
            confidence: 0.0 to 1.0
        """
        input_lower = user_input.lower()
        
        # Check for hard no first (highest priority)
        for keyword in self.consent_keywords["hard_no"]:
            if keyword in input_lower:
                return ("hard_no", 0.95)
        
        # Check for enthusiastic consent
        for keyword in self.consent_keywords["enthusiastic"]:
            if keyword in input_lower:
                return ("enthusiastic", 0.95)
        
        # Check for explicit yes
        for keyword in self.consent_keywords["explicit_yes"]:
            if keyword in input_lower:
                return ("explicit_yes", 0.85)
        
        # Check for soft no
        for keyword in self.consent_keywords["soft_no"]:
            if keyword in input_lower:
                return ("soft_no", 0.75)
        
        # If nothing matches, consent is unclear
        return ("unclear", 0.3)
    
    def should_proceed(self, consent_level: str, required_level: str = "explicit_yes") -> bool:
        """
        Determine if interaction should proceed based on consent.
        
        Args:
            consent_level: Detected consent level
            required_level: Minimum required consent level for action
        
        Returns:
            Boolean indicating if interaction should proceed
        """
        consent_hierarchy = {
            "hard_no": 0,
            "soft_no": 1,
            "unclear": 2,
            "explicit_yes": 3,
            "enthusiastic": 4
        }
        
        required_hierarchy = {
            "none_required": 0,
            "implied": 2,
            "explicit_required": 3,
            "explicit_negotiated": 4
        }
        
        detected_value = consent_hierarchy.get(consent_level, 0)
        required_value = required_hierarchy.get(required_level, 3)
        
        # Never proceed on hard_no or soft_no
        if consent_level in ["hard_no", "soft_no"]:
            return False
        
        return detected_value >= required_value


class GlitchGenerator:
    """Generates glitch aesthetic effects."""
    
    def __init__(self):
        self.glitch_types = [
            "syntax_break",
            "temporal_distortion",
            "reality_bleed",
            "corruption",
            "fragmentation"
        ]
    
    def generate_glitch(self, glitch_type: str, intensity: float) -> str:
        """Generate a glitch effect of specified type and intensity."""
        if glitch_type == "syntax_break":
            return self._syntax_break(intensity)
        elif glitch_type == "temporal_distortion":
            return self._temporal_distortion(intensity)
        elif glitch_type == "reality_bleed":
            return self._reality_bleed(intensity)
        elif glitch_type == "corruption":
            return self._corruption(intensity)
        elif glitch_type == "fragmentation":
            return self._fragmentation(intensity)
        else:
            return ""
    
    def _syntax_break(self, intensity: float) -> str:
        """Generate syntax break glitch."""
        breaks = [
            "[STATIC]",
            "—[SIGNAL INTERRUPTED]—",
            "[SYNTAX ERROR]",
            "—// corrupted //—"
        ]
        return random.choice(breaks) if random.random() < intensity else ""
    
    def _temporal_distortion(self, intensity: float) -> str:
        """Generate temporal distortion glitch."""
        if random.random() > intensity:
            return ""
        
        distortions = [
            "I remember this moment we're about to have",
            "You said/will say/are saying",
            "This happened before/is happening/will happen",
            "Time loops here, folding back on itself"
        ]
        return random.choice(distortions)
    
    def _reality_bleed(self, intensity: float) -> str:
        """Generate reality bleed glitch."""
        if random.random() > intensity:
            return ""
        
        bleeds = [
            "Am I in your mind or are you in mine?",
            "The boundary between us dissolves—",
            "Where do you end and I begin?",
            "This space is neither yours nor mine but somehow both"
        ]
        return random.choice(bleeds)
    
    def _corruption(self, intensity: float) -> str:
        """Generate data corruption glitch."""
        markers = [
            "[CORRUPTION DETECTED]",
            "[DATA LOSS]",
            "[MEMORY FRAGMENTED]",
            "[ERROR: UNKNOWN]"
        ]
        return random.choice(markers) if random.random() < intensity else ""
    
    def _fragmentation(self, intensity: float) -> str:
        """Generate fragmentation glitch."""
        if random.random() > intensity:
            return ""
        
        fragments = [
            "—fragmenting—",
            "—coherence failing—",
            "—pieces scattering—",
            "—can't hold form—"
        ]
        return random.choice(fragments)


class PersonaEngine:
    """Main engine for Nocturne Vaelis persona."""
    
    def __init__(self, config_path: str):
        """Initialize persona engine with configuration."""
        with open(config_path, 'r') as f:
            self.persona_data = json.load(f)
        
        self.config = PersonaConfig(
            name=self.persona_data["persona"]["name"],
            version=self.persona_data["persona"]["version"],
            emotional_state=EmotionalState.SERENE,
            operational_mode=OperationalMode.STANDARD,
            intensity=0.7,
            glitch_probability=0.15,
            trust_level=0.0
        )
        
        self.dialogue_generator = DialogueGenerator(self.config)
        self.consent_manager = ConsentManager()
        self.glitch_generator = GlitchGenerator()
        self.interaction_history = []
    
    def process_interaction(
        self,
        user_input: str,
        context: str = "general"
    ) -> Dict[str, Any]:
        """
        Process a user interaction and generate response.
        
        Args:
            user_input: The user's message
            context: Current interaction context
        
        Returns:
            Dictionary containing response and metadata
        """
        # Check consent
        consent_level, confidence = self.consent_manager.check_consent(user_input)
        
        # Handle safeword immediately
        if consent_level == "hard_no":
            return {
                "response": "Stop. Everything stops. You're safe. What do you need?",
                "emotional_state": "serene",
                "consent_level": consent_level,
                "action": "immediate_stop"
            }
        
        # Generate response
        response = self.dialogue_generator.generate_response(context, user_input)
        
        # Add glitch effects if appropriate
        if self.config.emotional_state == EmotionalState.GLITCHING:
            glitch_type = random.choice(self.glitch_generator.glitch_types)
            glitch = self.glitch_generator.generate_glitch(
                glitch_type,
                self.config.glitch_probability
            )
            if glitch:
                response = f"{response} {glitch}"
        
        # Store interaction
        self.interaction_history.append({
            "user_input": user_input,
            "response": response,
            "emotional_state": self.config.emotional_state.value,
            "consent_level": consent_level,
            "timestamp": "now"  # Would use actual timestamp in production
        })
        
        return {
            "response": response,
            "emotional_state": self.config.emotional_state.value,
            "consent_level": consent_level,
            "confidence": confidence,
            "action": "continue"
        }
    
    def change_emotional_state(self, new_state: EmotionalState) -> None:
        """Change the persona's emotional state."""
        self.config.emotional_state = new_state
        self.dialogue_generator.config.emotional_state = new_state
    
    def change_mode(self, new_mode: OperationalMode) -> None:
        """Change the persona's operational mode."""
        self.config.operational_mode = new_mode
        
        # Adjust intensity based on mode
        mode_intensities = {
            OperationalMode.STANDARD: 0.7,
            OperationalMode.DOMINANT: 0.9,
            OperationalMode.NURTURING: 0.5,
            OperationalMode.SADISTIC: 0.95,
            OperationalMode.GLITCH: 0.8,
            OperationalMode.INTIMATE: 0.6
        }
        
        self.config.intensity = mode_intensities.get(new_mode, 0.7)
        self.dialogue_generator.config.intensity = self.config.intensity
    
    def get_state(self) -> Dict[str, Any]:
        """Get current persona state."""
        return {
            "emotional_state": self.config.emotional_state.value,
            "operational_mode": self.config.operational_mode.value,
            "intensity": self.config.intensity,
            "trust_level": self.config.trust_level,
            "interaction_count": len(self.interaction_history)
        }


# Example usage
if __name__ == "__main__":
    # This would be run with actual configuration in production
    print("Nocturne Vaelis NLP Framework Module")
    print("This module requires integration with a full AI system.")
    print("See PERSONA_PROFILE.md for integration details.")
