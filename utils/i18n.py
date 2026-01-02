"""
Internationalization (i18n) utilities for backend messages
"""
import json
import os
import config

# Cache for loaded translations
_translations_cache = {}


def load_translations(lang='en'):
    """Load translations for a specific language"""
    if lang in _translations_cache:
        return _translations_cache[lang]
    
    # Try multiple possible paths for locale files
    possible_paths = [
        os.path.join(config.STATIC_DIR, 'locale', f'{lang}.json'),  # Docker path
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'locale', f'{lang}.json')  # Repository path
    ]
    
    for locale_file in possible_paths:
        try:
            if os.path.exists(locale_file):
                with open(locale_file, 'r', encoding='utf-8') as f:
                    translations = json.load(f)
                    _translations_cache[lang] = translations
                    return translations
        except Exception as e:
            print(f"Error loading translations from {locale_file}: {e}")
            continue
    
    # Fallback to English if language file not found
    if lang != 'en':
        return load_translations('en')
    
    return {}


def translate(key, lang='en', **kwargs):
    """
    Translate a key to the specified language
    
    Args:
        key: Translation key to look up
        lang: Language code (default: 'en')
        **kwargs: Optional parameters for string formatting (e.g., {count})
    
    Returns:
        Translated string with any parameters substituted
    """
    translations = load_translations(lang)
    text = translations.get(key, key)
    
    # Replace placeholders like {count} with provided values
    for placeholder, value in kwargs.items():
        text = text.replace(f'{{{placeholder}}}', str(value))
    
    return text


def get_request_language(request):
    """
    Get the preferred language from a Flask request
    
    Checks for:
    1. 'lang' query parameter
    2. 'Accept-Language' header
    3. Falls back to configured CONTENT_LANGUAGE
    
    Args:
        request: Flask request object
    
    Returns:
        Language code (e.g., 'en', 'de')
    """
    # Check query parameter first
    lang = request.args.get('lang')
    if lang and lang in ['en', 'de']:
        return lang
    
    # Check Accept-Language header
    accept_language = request.headers.get('Accept-Language', '')
    if 'de' in accept_language.lower():
        return 'de'
    elif 'en' in accept_language.lower():
        return 'en'
    
    # Fallback to configured language
    return config.CONTENT_LANGUAGE.lower() if hasattr(config, 'CONTENT_LANGUAGE') else 'en'
