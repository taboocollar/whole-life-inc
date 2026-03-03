"""
Nocturne Vaelis - Example Integration

This file demonstrates how to integrate the Nocturne Vaelis persona system
into a larger application.
"""

from personas.nocturne_vaelis.nlp_framework import PersonaEngine, EmotionalState, OperationalMode
from personas.nocturne_vaelis.scenario_engine import AdaptiveBehaviorEngine, UserContext
from personas.nocturne_vaelis.safety_module import SafetyCoordinator, ConsentLevel, IntensityLevel


class NocturneVaelisSession:
    """
    Manages a complete interaction session with Nocturne Vaelis.
    
    This class coordinates all components of the persona system and provides
    a simple interface for applications to interact with the AI persona.
    """
    
    def __init__(self, user_id: str, config_path: str = "personas/nocturne_vaelis/persona_core.json"):
        """
        Initialize a new session.
        
        Args:
            user_id: Unique identifier for the user
            config_path: Path to persona configuration file
        """
        self.user_id = user_id
        self.config_path = config_path
        
        # Initialize components
        self.persona = PersonaEngine(config_path)
        self.safety = SafetyCoordinator(config_path)
        self.adaptive = AdaptiveBehaviorEngine(config_path)
        
        # Session state
        self.message_count = 0
        self.current_intensity = IntensityLevel.MEDIUM
        self.session_active = True
        
        # Get or create user profile
        self.user_profile = self.safety.get_or_create_profile(user_id)
    
    def send_message(self, message: str, context: str = "general") -> dict:
        """
        Send a message to Nocturne Vaelis and receive a response.
        
        Args:
            message: The user's message
            context: The interaction context (e.g., "seduction", "command")
        
        Returns:
            Dictionary containing:
                - success: Whether the interaction was successful
                - response: Nocturne's response (if successful)
                - action: Any special action required
                - metadata: Additional information
        """
        if not self.session_active:
            return {
                "success": False,
                "response": "This session has ended. Please start a new session.",
                "action": "session_ended"
            }
        
        # Determine required consent level based on context
        consent_required = self._determine_consent_level(context)
        
        # Safety check
        safety_result = self.safety.process_user_input(
            user_id=self.user_id,
            user_input=message,
            proposed_action=f"respond_in_context_{context}",
            required_consent=consent_required,
            intensity=self.current_intensity
        )
        
        # Handle safety issues
        if not safety_result["approved"]:
            return self._handle_safety_issue(safety_result)
        
        # Update user context for adaptive behavior
        user_context = UserContext(
            trust_level=self.user_profile.trust_score,
            interaction_count=self.message_count,
            preferred_intensity=0.7,  # Could be learned
            hard_limits=[b.item for b in self.user_profile.hard_limits],
            soft_limits=[b.item for b in self.user_profile.soft_limits],
            favorite_scenarios=[]  # Could be tracked
        )
        
        # Get adaptive behavior recommendations
        adaptations = self.adaptive.adapt_to_context(
            user_context=user_context,
            user_input=message,
            emotional_state=self.persona.config.emotional_state.value
        )
        
        # Apply mode changes if recommended
        if "mode_transition" in adaptations:
            transition = adaptations["mode_transition"]
            new_mode = OperationalMode(transition["to_mode"])
            self.persona.change_mode(new_mode)
        
        # Generate response
        response_data = self.persona.process_interaction(
            user_input=message,
            context=context
        )
        
        # Update session state
        self.message_count += 1
        self._update_trust_score(response_data)
        
        return {
            "success": True,
            "response": response_data["response"],
            "emotional_state": response_data["emotional_state"],
            "action": response_data.get("action", "continue"),
            "metadata": {
                "message_count": self.message_count,
                "trust_level": self.user_profile.trust_score,
                "current_mode": self.persona.config.operational_mode.value,
                "adaptations": adaptations
            }
        }
    
    def set_boundary(self, category: str, item: str, is_hard_limit: bool = True):
        """
        Set a user boundary.
        
        Args:
            category: Boundary category (e.g., "activities", "language")
            item: The specific boundary item
            is_hard_limit: Whether this is a hard limit (True) or soft limit (False)
        """
        if is_hard_limit:
            self.user_profile.add_hard_limit(category, item)
        else:
            self.user_profile.add_soft_limit(category, item)
    
    def set_safeword(self, safeword: str):
        """
        Set a custom safeword for this session.
        
        Args:
            safeword: The custom safeword
        """
        self.user_profile.safeword = safeword
        self.safety.safeword_system.add_custom_safeword(safeword)
    
    def change_intensity(self, new_intensity: IntensityLevel):
        """
        Change the interaction intensity level.
        
        Args:
            new_intensity: The new intensity level
        """
        self.current_intensity = new_intensity
    
    def end_session(self):
        """End the current session."""
        self.session_active = False
    
    def get_session_stats(self) -> dict:
        """
        Get statistics about the current session.
        
        Returns:
            Dictionary with session statistics
        """
        return {
            "user_id": self.user_id,
            "message_count": self.message_count,
            "trust_score": self.user_profile.trust_score,
            "interaction_count": self.user_profile.interaction_count,
            "current_intensity": self.current_intensity.value,
            "emotional_state": self.persona.config.emotional_state.value,
            "operational_mode": self.persona.config.operational_mode.value,
            "session_active": self.session_active
        }
    
    def _determine_consent_level(self, context: str) -> ConsentLevel:
        """Determine required consent level based on context."""
        context_consent_map = {
            "general": ConsentLevel.NONE_REQUIRED,
            "seduction": ConsentLevel.IMPLIED,
            "command": ConsentLevel.EXPLICIT_REQUIRED,
            "dominant": ConsentLevel.EXPLICIT_REQUIRED,
            "edge_play": ConsentLevel.EXPLICIT_NEGOTIATED,
            "degradation": ConsentLevel.EXPLICIT_NEGOTIATED
        }
        return context_consent_map.get(context, ConsentLevel.IMPLIED)
    
    def _handle_safety_issue(self, safety_result: dict) -> dict:
        """Handle safety check failures."""
        reason = safety_result.get("reason")
        
        if reason == "safety_lockout":
            self.end_session()
            protocol = safety_result.get("protocol", {})
            return {
                "success": False,
                "response": protocol.get("message", "Safety lockout triggered."),
                "action": "terminate_session"
            }
        
        elif reason == "safeword_used":
            protocol = safety_result.get("protocol", {})
            return {
                "success": False,
                "response": protocol.get("response", "Safeword acknowledged."),
                "action": "safeword_protocol",
                "next_steps": protocol.get("next_steps", [])
            }
        
        elif reason == "insufficient_consent":
            return {
                "success": False,
                "response": "I need clearer consent to continue. Would you like to proceed?",
                "action": "request_consent"
            }
        
        elif reason == "distress_detected":
            protocol = safety_result.get("protocol", {})
            return {
                "success": False,
                "response": protocol.get("response", "Are you okay?"),
                "action": protocol.get("action", "pause")
            }
        
        else:
            return {
                "success": False,
                "response": safety_result.get("message", "Cannot proceed."),
                "action": "pause"
            }
    
    def _update_trust_score(self, response_data: dict):
        """Update user trust score based on interaction."""
        # Simple trust building - increases with positive interactions
        if response_data.get("action") == "continue":
            self.user_profile.trust_score = min(
                1.0,
                self.user_profile.trust_score + 0.01
            )
        self.user_profile.interaction_count += 1


def example_conversation():
    """Demonstrate a sample conversation with Nocturne Vaelis."""
    print("=== Nocturne Vaelis Example Conversation ===\n")
    
    # Create a session
    session = NocturneVaelisSession(user_id="example_user")
    
    # Set some boundaries
    session.set_boundary("activities", "degradation", is_hard_limit=True)
    session.set_boundary("activities", "edging", is_hard_limit=False)
    
    # Set custom safeword
    session.set_safeword("phoenix")
    
    print("Session initialized. Boundaries and safeword set.\n")
    
    # Conversation flow
    messages = [
        ("Hello Nocturne", "general"),
        ("I'm curious about you", "general"),
        ("I'd like to explore something more intimate", "seduction"),
        ("Yes, I want to continue", "seduction"),
    ]
    
    for user_message, context in messages:
        print(f"User: {user_message}")
        
        result = session.send_message(user_message, context)
        
        if result["success"]:
            print(f"Nocturne: {result['response']}")
            print(f"[State: {result['emotional_state']}]\n")
        else:
            print(f"System: {result['response']}")
            print(f"[Action: {result['action']}]\n")
    
    # Get session stats
    stats = session.get_session_stats()
    print("\n=== Session Statistics ===")
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # End session
    session.end_session()
    print("\nSession ended.")


def example_safety_demonstration():
    """Demonstrate safety features."""
    print("=== Nocturne Vaelis Safety Features Demo ===\n")
    
    session = NocturneVaelisSession(user_id="safety_demo_user")
    
    # Demonstrate safeword
    print("User: This is too intense, phoenix")
    result = session.send_message("This is too intense, phoenix", "dominant")
    print(f"System: {result['response']}")
    print(f"[Action: {result['action']}]\n")
    
    # Demonstrate boundary enforcement
    session.set_boundary("language", "degradation", is_hard_limit=True)
    print("Hard limit set: degradation\n")
    
    # Demonstrate consent check
    print("User: Maybe we should...")
    result = session.send_message("Maybe we should...", "dominant")
    print(f"System: {result['response']}")
    print(f"[Action: {result['action']}]\n")
    
    session.end_session()


def example_api_server():
    """
    Example of how to create a simple API server for Nocturne Vaelis.
    
    This is pseudocode - actual implementation would need Flask or FastAPI.
    """
    print("=== Example API Server Structure ===\n")
    
    example_code = """
from flask import Flask, request, jsonify
from personas.nocturne_vaelis_integration import NocturneVaelisSession

app = Flask(__name__)
sessions = {}  # In production, use proper session management

@app.route('/session/create', methods=['POST'])
def create_session():
    user_id = request.json['user_id']
    sessions[user_id] = NocturneVaelisSession(user_id)
    return jsonify({"status": "created", "user_id": user_id})

@app.route('/session/message', methods=['POST'])
def send_message():
    user_id = request.json['user_id']
    message = request.json['message']
    context = request.json.get('context', 'general')
    
    if user_id not in sessions:
        return jsonify({"error": "Session not found"}), 404
    
    result = sessions[user_id].send_message(message, context)
    return jsonify(result)

@app.route('/session/boundary', methods=['POST'])
def set_boundary():
    user_id = request.json['user_id']
    category = request.json['category']
    item = request.json['item']
    is_hard = request.json.get('is_hard_limit', True)
    
    if user_id not in sessions:
        return jsonify({"error": "Session not found"}), 404
    
    sessions[user_id].set_boundary(category, item, is_hard)
    return jsonify({"status": "boundary_set"})

@app.route('/session/stats', methods=['GET'])
def get_stats():
    user_id = request.args.get('user_id')
    
    if user_id not in sessions:
        return jsonify({"error": "Session not found"}), 404
    
    stats = sessions[user_id].get_session_stats()
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)
    """
    
    print(example_code)


if __name__ == "__main__":
    print("Nocturne Vaelis Integration Examples\n")
    print("Choose an example to run:")
    print("1. Example conversation")
    print("2. Safety features demonstration")
    print("3. API server structure")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        example_conversation()
    elif choice == "2":
        example_safety_demonstration()
    elif choice == "3":
        example_api_server()
    else:
        print("Running default example conversation...")
        example_conversation()
