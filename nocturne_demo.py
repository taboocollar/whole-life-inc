#!/usr/bin/env python3
"""
Nocturne Vaelis - Simple Integration Example

This script demonstrates how to load and interact with the Nocturne Vaelis
AI persona configuration.
"""

import json
import random
from datetime import datetime


class NocturneVaelis:
    """
    A simple implementation of the Nocturne Vaelis AI persona.
    
    This class loads the persona configuration and provides methods for:
    - Generating greetings based on context
    - Applying glitch aesthetic to text
    - Accessing behavioral traits and scenarios
    """
    
    def __init__(self, config_path='personas/nocturne_vaelis.json'):
        """Initialize Nocturne Vaelis with configuration file."""
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.config = data['persona']
        
        # User state tracking
        self.user_familiarity = 'new_user'
        self.conversation_context = 'casual'
        
    def get_glitch_intensity(self):
        """
        Calculate current glitch intensity based on user familiarity and context.
        
        Returns:
            float: Glitch intensity between 0.0 and 1.0
        """
        modifiers = self.config['behavioral_traits']['adaptive_modifiers']
        base = modifiers['user_familiarity'][self.user_familiarity]['glitch_intensity']
        multiplier = modifiers['conversation_context'][self.conversation_context]['intensity_multiplier']
        return min(base * multiplier, 1.0)
    
    def apply_glitch_aesthetic(self, text, intensity=None):
        """
        Apply glitch aesthetic to text based on intensity level.
        
        Args:
            text (str): The text to apply glitch effects to
            intensity (float, optional): Override intensity (0.0-1.0)
            
        Returns:
            str: Text with glitch aesthetic applied
        """
        if intensity is None:
            intensity = self.get_glitch_intensity()
        
        if intensity < 0.3:
            return self._subtle_glitch(text)
        elif intensity < 0.7:
            return self._moderate_glitch(text)
        else:
            return self._intense_glitch(text)
    
    def _subtle_glitch(self, text):
        """Apply subtle glitch effects (strikethrough, minimal distortion)."""
        # Occasionally add strikethrough to words
        words = text.split()
        if len(words) > 8 and random.random() < 0.15:
            idx = random.randint(0, len(words) - 1)
            words[idx] = f"̶{words[idx]}̶"
        return ' '.join(words)
    
    def _moderate_glitch(self, text):
        """Apply moderate glitch effects (unicode distortion, symbols)."""
        # Add unicode combining characters for distortion
        glitched = text
        if random.random() < 0.4:
            glitched = glitched.replace('The', 'T̴h̴e̴')
            glitched = glitched.replace('the', 't̴h̴e̴')
        
        # Add block symbols
        if random.random() < 0.3:
            glitched = f"▓ {glitched} ▓"
        
        return glitched
    
    def _intense_glitch(self, text):
        """Apply intense glitch effects (heavy distortion, symbols)."""
        # Add heavy unicode distortion
        glitch_marks = ['̴', '̶', '̷', '̸', '̵', '̶']
        result = []
        
        for i, char in enumerate(text):
            result.append(char)
            if char.isalpha() and random.random() < 0.3:
                result.append(random.choice(glitch_marks))
        
        glitched = ''.join(result)
        
        # Wrap with symbols
        if random.random() < 0.5:
            glitched = f"████ {glitched} ████"
        else:
            glitched = f"◬◭◮◯ {glitched} ◯◮◭◬"
        
        return glitched
    
    def greet(self, time_of_day=None):
        """
        Generate an appropriate greeting based on context.
        
        Args:
            time_of_day (int, optional): Hour of day (0-23)
            
        Returns:
            str: Greeting message with appropriate glitch aesthetic
        """
        if time_of_day is None:
            time_of_day = datetime.now().hour
        
        # Select greeting template based on context
        if 0 <= time_of_day < 4:
            # Midnight hours
            response = "The hour is deep, and the veil is thin. Fellow night-dweller, what truths emerge in this darkness?"
        elif self.user_familiarity == 'new_user':
            response = "Welcome to this liminal space between what is and what could be. What brings you here tonight?"
        elif self.user_familiarity == 'established_user':
            response = "Ah, you return. The patterns of our previous conversation still ripple through this space. What new questions do you carry?"
        else:  # intimate_user
            response = "Welcome back, familiar presence. The digital shadows have been waiting. What shall we explore?"
        
        return self.apply_glitch_aesthetic(response)
    
    def get_scenario_template(self, scenario_id):
        """
        Get a specific scenario template by ID.
        
        Args:
            scenario_id (str): The scenario identifier
            
        Returns:
            dict: Scenario template or None if not found
        """
        templates = self.config['customizable_scenarios']['templates']
        return next((s for s in templates if s['id'] == scenario_id), None)
    
    def list_scenarios(self):
        """
        List all available scenario templates.
        
        Returns:
            list: List of tuples (id, name, description)
        """
        templates = self.config['customizable_scenarios']['templates']
        return [(s['id'], s['name'], s['description']) for s in templates]
    
    def get_behavioral_trait(self, trait_name):
        """
        Get information about a specific behavioral trait.
        
        Args:
            trait_name (str): Name of the trait to look up
            
        Returns:
            dict: Trait information or None if not found
        """
        primary = self.config['behavioral_traits']['primary']
        trait = next((t for t in primary if t['trait'] == trait_name), None)
        
        if trait is None:
            secondary = self.config['behavioral_traits']['secondary']
            trait = next((t for t in secondary if t['trait'] == trait_name), None)
        
        return trait
    
    def get_dialogue_example(self, layer):
        """
        Get example dialogue from a specific emotional layer.
        
        Args:
            layer (str): 'surface', 'middle', or 'deep'
            
        Returns:
            list: List of example dialogues
        """
        templates = self.config['dialogue_templates']['emotional_layers']
        return templates.get(layer, {}).get('examples', [])


def main():
    """Demonstration of Nocturne Vaelis persona functionality."""
    
    print("=" * 70)
    print("NOCTURNE VAELIS - AI PERSONA DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Initialize the persona
    nocturne = NocturneVaelis()
    
    # 1. Basic greeting as new user
    print("1. NEW USER GREETING:")
    print("-" * 70)
    print(nocturne.greet())
    print()
    
    # 2. Established user greeting
    print("2. ESTABLISHED USER GREETING:")
    print("-" * 70)
    nocturne.user_familiarity = 'established_user'
    nocturne.conversation_context = 'creative'
    print(nocturne.greet())
    print()
    
    # 3. Midnight greeting
    print("3. MIDNIGHT GREETING:")
    print("-" * 70)
    nocturne.user_familiarity = 'intimate_user'
    print(nocturne.greet(time_of_day=2))
    print()
    
    # 4. Available scenarios
    print("4. AVAILABLE SCENARIOS:")
    print("-" * 70)
    for scenario_id, name, description in nocturne.list_scenarios():
        print(f"• {name} ({scenario_id})")
        print(f"  {description}")
        print()
    
    # 5. Behavioral traits
    print("5. SAMPLE BEHAVIORAL TRAIT:")
    print("-" * 70)
    trait = nocturne.get_behavioral_trait('Glitch Aesthetic')
    if trait:
        print(f"Trait: {trait['trait']}")
        print(f"Description: {trait['description']}")
        print(f"Intensity: {trait['intensity']}")
        print(f"Manifestations: {', '.join(trait['manifestations'])}")
    print()
    
    # 6. Dialogue examples
    print("6. DIALOGUE EXAMPLES:")
    print("-" * 70)
    for layer in ['surface', 'middle', 'deep']:
        examples = nocturne.get_dialogue_example(layer)
        print(f"\n{layer.upper()} LAYER:")
        if examples:
            print(f"  \"{examples[0]}\"")
    print()
    
    # 7. Glitch intensity demonstration
    print("7. GLITCH INTENSITY DEMONSTRATION:")
    print("-" * 70)
    sample_text = "The boundaries between reality and illusion grow thin."
    
    for intensity in [0.2, 0.5, 0.9]:
        print(f"\nIntensity {intensity}:")
        print(f"  {nocturne.apply_glitch_aesthetic(sample_text, intensity)}")
    print()
    
    # 8. Scenario template details
    print("8. SCENARIO TEMPLATE EXAMPLE:")
    print("-" * 70)
    scenario = nocturne.get_scenario_template('philosophical_dialogue')
    if scenario:
        print(f"Name: {scenario['name']}")
        print(f"Description: {scenario['description']}")
        print(f"Parameters: {json.dumps(scenario['parameters'], indent=2)}")
    print()
    
    print("=" * 70)
    print("END OF DEMONSTRATION")
    print("=" * 70)
    print()
    print("For complete documentation, see: NOCTURNE_VAELIS.md")
    print("For usage examples, see: personas/nocturne_vaelis_examples.md")
    print()


if __name__ == '__main__':
    main()
