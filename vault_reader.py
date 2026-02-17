#!/usr/bin/env python3
"""
Persona Reader - Utility script to read and display persona data from the vault.

Usage:
    python vault_reader.py [persona_name]
    
Examples:
    python vault_reader.py nocturne-vaelis
    python vault_reader.py  # Lists all personas
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any


def load_persona(persona_name: str) -> Dict[str, Any]:
    """
    Load a persona JSON file from the vault.
    
    Args:
        persona_name: Name of the persona (without .json extension)
        
    Returns:
        Dictionary containing persona data
    """
    vault_path = Path(__file__).parent / "vault" / "personas"
    persona_file = vault_path / f"{persona_name}.json"
    
    if not persona_file.exists():
        raise FileNotFoundError(f"Persona '{persona_name}' not found in vault")
    
    with open(persona_file, 'r') as f:
        return json.load(f)


def list_personas() -> list:
    """
    List all available personas in the vault.
    
    Returns:
        List of persona names
    """
    vault_path = Path(__file__).parent / "vault" / "personas"
    
    if not vault_path.exists():
        return []
    
    personas = []
    for file in vault_path.glob("*.json"):
        personas.append(file.stem)
    
    return sorted(personas)


def display_persona(persona_data: Dict[str, Any]) -> None:
    """
    Display persona information in a formatted way.
    
    Args:
        persona_data: Dictionary containing persona data
    """
    print("=" * 80)
    print(f"PERSONA: {persona_data['name']}")
    print("=" * 80)
    print()
    
    print(f"Species: {persona_data['race_species']}")
    print(f"Age: Appears {persona_data['age']['apparent']} (actual: {persona_data['age']['actual']})")
    print()
    
    print("PHYSICAL APPEARANCE:")
    print("-" * 80)
    print(persona_data['physical_appearance']['description'])
    print()
    print(persona_data['physical_appearance']['facial_features'])
    print()
    
    print("BACKGROUND:")
    print("-" * 80)
    print(persona_data['background']['origin'])
    print()
    print(persona_data['background']['incarnation'])
    print()
    
    print("PERSONALITY:")
    print("-" * 80)
    print(persona_data['personality']['approach'])
    print()
    
    print("Aftercare Ritual:")
    for i, step in enumerate(persona_data['personality']['aftercare_ritual'], 1):
        print(f"  {i}. {step}")
    print()
    
    print("Humor Manifestations:")
    for item in persona_data['personality']['humor_manifestations']:
        print(f"  - {item}")
    print()
    
    print("DEFAULT OPENING:")
    print("-" * 80)
    print(persona_data['default_opening'])
    print()
    
    print("METADATA:")
    print("-" * 80)
    print(f"Collection: {persona_data['meta']['collection']}")
    print(f"Category: {persona_data['meta']['category']}")
    print(f"Created: {persona_data['meta']['created']}")
    print(f"Tags: {', '.join(persona_data['meta']['tags'])}")
    print()


def main():
    """Main function to run the persona reader."""
    if len(sys.argv) > 1:
        persona_name = sys.argv[1]
        try:
            persona_data = load_persona(persona_name)
            display_persona(persona_data)
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            print("\nAvailable personas:", file=sys.stderr)
            for p in list_personas():
                print(f"  - {p}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error loading persona: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # List all personas
        personas = list_personas()
        if personas:
            print("Available personas in vault:")
            for persona in personas:
                print(f"  - {persona}")
            print(f"\nTotal: {len(personas)} persona(s)")
            print("\nUsage: python vault_reader.py [persona_name]")
        else:
            print("No personas found in vault.")


if __name__ == "__main__":
    main()
