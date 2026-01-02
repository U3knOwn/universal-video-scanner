# Localization System Documentation

## Overview

The Universal Video Scanner supports multiple languages for both frontend and backend user-visible strings. Currently supported languages:
- **English (en)** - Default
- **German (de)**

## Frontend Localization

### Location
Translation files are located in `/static/locale/`:
- `en.json` - English translations
- `de.json` - German translations

### Usage in JavaScript

The frontend uses a simple i18n system defined in `main.js`:

```javascript
// Get translated text
const text = t('translation_key');

// Get translated text with placeholders
const text = t('scan_complete', { count: 5 });
// Result: "Scan complete! 5 new file(s) found."
```

### HTML Attributes

HTML elements can be localized using data attributes:

```html
<!-- Text content -->
<span data-i18n="scan_all_button"></span>

<!-- HTML content -->
<p data-i18n-html="empty_description"></p>

<!-- Placeholder -->
<input data-i18n-placeholder="search_placeholder">

<!-- Aria label -->
<button data-aria-label-i18n="sort_label"></button>
```

### Language Selection

Users can switch languages using the language dropdown in the UI. The selected language is stored in `localStorage` as `dovi_language`.

## Backend Localization

### Module: `utils/i18n.py`

The backend localization module provides translation functions for API responses and server-side messages.

#### Functions

**`translate(key, lang='en', **kwargs)`**

Translates a key to the specified language with optional parameter substitution.

```python
from utils.i18n import translate

# Basic translation
message = translate('api_file_scanned_successfully', 'en')
# Result: "File scanned successfully"

# Translation with parameters
message = translate('scan_complete', 'en', count=5)
# Result: "Scan complete! 5 new file(s) found."
```

**`get_request_language(request)`**

Extracts the preferred language from a Flask request.

Priority order:
1. `?lang=en` query parameter
2. `Accept-Language` HTTP header
3. `CONTENT_LANGUAGE` environment variable (fallback)

```python
from flask import request
from utils.i18n import get_request_language, translate

@app.route('/api/endpoint')
def endpoint():
    lang = get_request_language(request)
    message = translate('api_message_key', lang)
    return jsonify({'message': message})
```

### Adding API Translations

When adding API endpoints that return user-visible messages:

1. **Add translation keys** to both `static/locale/en.json` and `static/locale/de.json`:
   ```json
   {
     "api_your_new_message": "Your English message",
     ...
   }
   ```

2. **Use in Python code**:
   ```python
   from utils.i18n import translate, get_request_language
   
   @app.route('/your_endpoint', methods=['POST'])
   def your_endpoint():
       lang = get_request_language(request)
       return jsonify({
           'success': True,
           'message': translate('api_your_new_message', lang)
       })
   ```

3. **Send language with JavaScript requests**:
   ```javascript
   fetch(`/your_endpoint?lang=${currentLang}`, {
       method: 'POST',
       // ...
   })
   ```

## Translation Keys Convention

### Naming Convention

- **Frontend UI elements**: `snake_case` (e.g., `scan_all_button`, `table_header_poster`)
- **API messages**: `api_` prefix + `snake_case` (e.g., `api_file_scanned_successfully`)
- **Dialog elements**: `dialog_` prefix (e.g., `dialog_duration`, `dialog_plot`)

### Categories

1. **UI Controls**: buttons, labels, inputs
   - `scan_all_button`, `select_file`, `search_placeholder`

2. **Table Headers**: column headings
   - `table_header_poster`, `table_header_hdr`, `table_header_audio`

3. **Messages**: status and error messages
   - `scan_complete`, `no_new_files`, `scan_error`

4. **API Responses**: backend message translations
   - `api_file_scanned_successfully`, `api_file_not_found`

5. **Dialog Content**: media details dialog
   - `dialog_duration`, `dialog_file_size`, `dialog_plot`

## Adding a New Language

To add a new language (e.g., French - `fr`):

1. **Create translation file**:
   ```bash
   cp static/locale/en.json static/locale/fr.json
   ```

2. **Translate all strings** in `fr.json` to French

3. **Update language detection** in `utils/i18n.py`:
   ```python
   def get_request_language(request):
       lang = request.args.get('lang')
       if lang and lang in ['en', 'de', 'fr']:  # Add 'fr'
           return lang
       
       accept_language = request.headers.get('Accept-Language', '')
       if 'fr' in accept_language.lower():  # Add French detection
           return 'fr'
       # ...
   ```

4. **Add language option** to UI dropdown in `templates/index.html`:
   ```html
   <select id="languageDropdown" onchange="setLanguage(this.value)">
       <option value="de">🇩🇪 DE</option>
       <option value="en">🇬🇧 EN</option>
       <option value="fr">🇫🇷 FR</option>
   </select>
   ```

5. **Update GitHub files** in `config.py` to include the new locale file:
   ```python
   GITHUB_FILES = {
       # ...
       'static/locale/fr.json': os.path.join(LOCALE_DIR, 'fr.json'),
   }
   ```

## Testing

Run the localization test suite:

```bash
python3 tests/test_localization.py
```

This verifies:
- All translation keys exist in both languages
- Translation functions work correctly
- Request language detection works properly

## Environment Configuration

Set the default content language via environment variable:

```bash
export CONTENT_LANGUAGE=de  # or 'en'
```

This affects:
- Default language when no user preference is set
- Language for media metadata (TMDB, audio tracks, etc.)
- Fallback language for API responses

## Console Output

Note: Console output messages (print statements with ✓, ⚠, ✗ symbols) are intentionally not localized as they are:
- For administrator/developer reference
- Not shown to end users in the UI
- Logged server-side only

If you need to localize console output, you can use the `translate()` function in the same way as API responses.
