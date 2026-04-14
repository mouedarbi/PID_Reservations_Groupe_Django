import requests
import json
from catalogue.models.setting import AppSetting

def translate_text(text, target_language):
    """
    Traduit un texte vers une langue cible en utilisant l'API LibreTranslate.
    Utilise l'auto-détection de la langue source.
    """
    api_url = AppSetting.get_value('LIBRETRANSLATE_API_URL', 'https://libretranslate.com')
    api_key = AppSetting.get_value('LIBRETRANSLATE_API_KEY', '')
    
    if not text:
        return text

    # Nettoyage de l'URL si nécessaire
    if api_url.endswith('/'):
        api_url = api_url[:-1]
    
    endpoint = f"{api_url}/translate"
    
    payload = {
        'q': text,
        'source': 'auto',
        'target': target_language,
        'format': 'text'
    }
    
    if api_key:
        payload['api_key'] = api_key

    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(endpoint, data=json.dumps(payload), headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('translatedText', text)
        else:
            print(f"Erreur LibreTranslate API ({response.status_code}): {response.text}")
            return text
    except Exception as e:
        print(f"Erreur lors de la traduction (LibreTranslate) : {e}")
        return text

def translate_review(review_obj):
    """
    Traduit un objet Review dans les 3 langues (FR, EN, NL) via LibreTranslate.
    """
    original_text = review_obj.review
    if not original_text:
        return

    # Traduction vers les 3 langues cibles
    # Note: 'auto' détectera si le texte est déjà dans la langue cible.
    review_obj.review_fr = translate_text(original_text, 'fr')
    review_obj.review_en = translate_text(original_text, 'en')
    review_obj.review_nl = translate_text(original_text, 'nl')
    
    # On sauvegarde sans déclencher à nouveau les signaux si possible
    review_obj.save()
