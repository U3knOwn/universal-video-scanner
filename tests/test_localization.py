#!/usr/bin/env python3
"""
Simple test script to verify localization functionality
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.i18n import translate, load_translations


def test_translations():
    """Test that all API message keys are properly translated"""
    print("Testing localization system...")
    
    # Test keys to check
    test_keys = [
        'api_file_scanned_successfully',
        'api_file_not_profile_or_scanned',
        'api_assets_updated_successfully',
        'api_no_file_path_provided',
        'api_file_not_found',
        'api_failed_to_update_assets',
        'unknown'
    ]
    
    # Test English
    print("\n=== Testing English (en) ===")
    en_translations = load_translations('en')
    for key in test_keys:
        en_text = translate(key, 'en')
        status = "✓" if en_text != key else "✗"
        print(f"{status} {key}: {en_text}")
    
    # Test German
    print("\n=== Testing German (de) ===")
    de_translations = load_translations('de')
    for key in test_keys:
        de_text = translate(key, 'de')
        status = "✓" if de_text != key else "✗"
        print(f"{status} {key}: {de_text}")
    
    # Verify all keys exist
    print("\n=== Verification ===")
    all_passed = True
    for key in test_keys:
        en_exists = key in en_translations
        de_exists = key in de_translations
        if not en_exists or not de_exists:
            all_passed = False
            print(f"✗ Missing key '{key}' in: ", end="")
            if not en_exists:
                print("EN ", end="")
            if not de_exists:
                print("DE", end="")
            print()
    
    if all_passed:
        print("✓ All localization keys are properly defined")
        return True
    else:
        print("✗ Some localization keys are missing")
        return False


if __name__ == '__main__':
    success = test_translations()
    sys.exit(0 if success else 1)
