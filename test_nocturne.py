#!/usr/bin/env python3
"""
Test suite for Nocturne Vaelis persona configuration.

This script validates:
- JSON structure integrity
- Required fields presence
- Data type consistency
- Value ranges
- Cross-reference validity
"""

import json
import sys


def test_json_validity(config_path='personas/nocturne_vaelis.json'):
    """Test 1: Verify JSON file is valid and loadable."""
    print("Test 1: JSON Validity...")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("  ✓ JSON file is valid and loadable")
        return data
    except json.JSONDecodeError as e:
        print(f"  ✗ JSON decode error: {e}")
        return None
    except FileNotFoundError:
        print(f"  ✗ File not found: {config_path}")
        return None


def test_core_structure(data):
    """Test 2: Verify core structure has required top-level keys."""
    print("\nTest 2: Core Structure...")
    required_keys = [
        'id', 'name', 'version', 'description', 'core_attributes',
        'behavioral_traits', 'interactive_triggers', 'decision_trees',
        'branching_narratives', 'customizable_scenarios', 
        'dialogue_templates', 'system_metadata'
    ]
    
    persona = data.get('persona', {})
    missing = [key for key in required_keys if key not in persona]
    
    if not missing:
        print("  ✓ All required top-level keys present")
        return True
    else:
        print(f"  ✗ Missing keys: {', '.join(missing)}")
        return False


def test_behavioral_traits(data):
    """Test 3: Verify behavioral traits structure."""
    print("\nTest 3: Behavioral Traits...")
    traits = data['persona'].get('behavioral_traits', {})
    
    # Check for primary traits
    primary = traits.get('primary', [])
    if len(primary) < 3:
        print(f"  ✗ Expected at least 3 primary traits, found {len(primary)}")
        return False
    
    # Validate trait structure
    for trait in primary:
        required = ['trait', 'description', 'intensity', 'triggers']
        missing = [k for k in required if k not in trait]
        if missing:
            print(f"  ✗ Trait '{trait.get('trait', 'unknown')}' missing: {missing}")
            return False
        
        # Validate intensity range
        intensity = trait.get('intensity')
        if not (0.0 <= intensity <= 1.0):
            print(f"  ✗ Trait '{trait['trait']}' intensity {intensity} out of range [0.0, 1.0]")
            return False
    
    # Check adaptive modifiers
    modifiers = traits.get('adaptive_modifiers', {})
    if 'user_familiarity' not in modifiers or 'conversation_context' not in modifiers:
        print("  ✗ Missing adaptive modifiers")
        return False
    
    print(f"  ✓ Behavioral traits valid ({len(primary)} primary traits)")
    return True


def test_interactive_triggers(data):
    """Test 4: Verify interactive triggers."""
    print("\nTest 4: Interactive Triggers...")
    triggers = data['persona'].get('interactive_triggers', {})
    
    required_sections = ['greeting_contexts', 'topic_engagement', 'emotional_states']
    missing = [s for s in required_sections if s not in triggers]
    
    if missing:
        print(f"  ✗ Missing trigger sections: {', '.join(missing)}")
        return False
    
    # Validate greeting contexts
    greetings = triggers.get('greeting_contexts', [])
    if len(greetings) < 2:
        print(f"  ✗ Expected at least 2 greeting contexts, found {len(greetings)}")
        return False
    
    # Validate topic engagement
    topics = triggers.get('topic_engagement', [])
    if len(topics) < 3:
        print(f"  ✗ Expected at least 3 topic engagement types, found {len(topics)}")
        return False
    
    print(f"  ✓ Interactive triggers valid ({len(greetings)} greetings, {len(topics)} topics)")
    return True


def test_decision_trees(data):
    """Test 5: Verify decision tree structure."""
    print("\nTest 5: Decision Trees...")
    trees = data['persona'].get('decision_trees', {})
    
    required_trees = ['conversation_flow', 'response_generation']
    missing = [t for t in required_trees if t not in trees]
    
    if missing:
        print(f"  ✗ Missing decision trees: {', '.join(missing)}")
        return False
    
    # Validate tree structure
    for tree_name, tree in trees.items():
        if 'entry_point' not in tree or 'nodes' not in tree:
            print(f"  ✗ Tree '{tree_name}' missing entry_point or nodes")
            return False
        
        # Verify entry point exists in nodes
        entry = tree['entry_point']
        if entry not in tree['nodes']:
            print(f"  ✗ Tree '{tree_name}' entry_point '{entry}' not in nodes")
            return False
    
    print(f"  ✓ Decision trees valid ({len(trees)} trees)")
    return True


def test_branching_narratives(data):
    """Test 6: Verify branching narratives."""
    print("\nTest 6: Branching Narratives...")
    narratives = data['persona'].get('branching_narratives', {})
    
    if len(narratives) < 2:
        print(f"  ✗ Expected at least 2 narrative arcs, found {len(narratives)}")
        return False
    
    # Validate narrative structure
    for name, narrative in narratives.items():
        required = ['title', 'description', 'entry_points', 'stages']
        missing = [k for k in required if k not in narrative]
        if missing:
            print(f"  ✗ Narrative '{name}' missing: {', '.join(missing)}")
            return False
        
        # Validate stages
        stages = narrative.get('stages', [])
        if len(stages) < 2:
            print(f"  ✗ Narrative '{name}' should have at least 2 stages")
            return False
    
    print(f"  ✓ Branching narratives valid ({len(narratives)} arcs)")
    return True


def test_customizable_scenarios(data):
    """Test 7: Verify customizable scenarios."""
    print("\nTest 7: Customizable Scenarios...")
    scenarios = data['persona'].get('customizable_scenarios', {})
    
    templates = scenarios.get('templates', [])
    if len(templates) < 3:
        print(f"  ✗ Expected at least 3 scenario templates, found {len(templates)}")
        return False
    
    # Validate template structure
    for template in templates:
        required = ['id', 'name', 'description', 'parameters']
        missing = [k for k in required if k not in template]
        if missing:
            print(f"  ✗ Template '{template.get('id', 'unknown')}' missing: {', '.join(missing)}")
            return False
    
    # Check adaptation modules
    if 'adaptation_modules' not in scenarios:
        print("  ✗ Missing adaptation_modules")
        return False
    
    print(f"  ✓ Customizable scenarios valid ({len(templates)} templates)")
    return True


def test_dialogue_templates(data):
    """Test 8: Verify dialogue templates."""
    print("\nTest 8: Dialogue Templates...")
    templates = data['persona'].get('dialogue_templates', {})
    
    required_sections = ['emotional_layers', 'glitch_aesthetic_templates', 'response_patterns']
    missing = [s for s in required_sections if s not in templates]
    
    if missing:
        print(f"  ✗ Missing template sections: {', '.join(missing)}")
        return False
    
    # Validate emotional layers
    layers = templates.get('emotional_layers', {})
    required_layers = ['surface', 'middle', 'deep']
    missing_layers = [l for l in required_layers if l not in layers]
    
    if missing_layers:
        print(f"  ✗ Missing emotional layers: {', '.join(missing_layers)}")
        return False
    
    # Validate glitch templates
    glitch = templates.get('glitch_aesthetic_templates', {})
    required_glitch = ['subtle', 'moderate', 'intense']
    missing_glitch = [g for g in required_glitch if g not in glitch]
    
    if missing_glitch:
        print(f"  ✗ Missing glitch levels: {', '.join(missing_glitch)}")
        return False
    
    print(f"  ✓ Dialogue templates valid")
    return True


def test_version_info(data):
    """Test 9: Verify version and metadata."""
    print("\nTest 9: Version & Metadata...")
    persona = data.get('persona', {})
    
    # Check version
    version = persona.get('version')
    if not version or not version.startswith('2.'):
        print(f"  ✗ Expected version 2.x.x, found: {version}")
        return False
    
    # Check metadata
    metadata = persona.get('system_metadata', {})
    required = ['capabilities', 'limitations', 'ethical_guidelines']
    missing = [k for k in required if k not in metadata]
    
    if missing:
        print(f"  ✗ Missing metadata sections: {', '.join(missing)}")
        return False
    
    print(f"  ✓ Version {version} and metadata valid")
    return True


def run_all_tests():
    """Run all validation tests."""
    print("=" * 70)
    print("NOCTURNE VAELIS - VALIDATION TEST SUITE")
    print("=" * 70)
    
    # Load the data
    data = test_json_validity()
    if not data:
        print("\n✗ FAILED: Cannot proceed without valid JSON")
        return False
    
    # Run all tests
    tests = [
        test_core_structure,
        test_behavioral_traits,
        test_interactive_triggers,
        test_decision_trees,
        test_branching_narratives,
        test_customizable_scenarios,
        test_dialogue_templates,
        test_version_info
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test(data))
        except Exception as e:
            print(f"  ✗ Test failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 70)
    passed = sum(results)
    total = len(results) + 1  # +1 for JSON validity
    
    print(f"TEST SUMMARY: {passed + 1}/{total} tests passed")
    
    if all(results):
        print("✓ ALL TESTS PASSED - Persona configuration is valid!")
        print("=" * 70)
        return True
    else:
        print("✗ SOME TESTS FAILED - Please review errors above")
        print("=" * 70)
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
