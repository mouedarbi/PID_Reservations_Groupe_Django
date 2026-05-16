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
    review_obj.review_fr = translate_text(original_text, 'fr')
    review_obj.review_en = translate_text(original_text, 'en')
    review_obj.review_nl = translate_text(original_text, 'nl')
    
    review_obj.save()

def translate_type(type_obj):
    """
    Traduit un objet Type dans les 3 langues (FR, EN, NL) via LibreTranslate.
    Gère les conflits d'unicité si la traduction existe déjà.
    """
    from django.db import IntegrityError
    original_text = type_obj.type
    if not original_text:
        return

    # Traduire vers les langues cibles
    translated_fr = translate_text(original_text, 'fr')
    translated_en = translate_text(original_text, 'en')
    translated_nl = translate_text(original_text, 'nl')
    
    try:
        type_obj.type_fr = translated_fr
        type_obj.type_en = translated_en
        type_obj.type_nl = translated_nl
        type_obj.save()
    except IntegrityError:
        # Si la traduction FR (qui est souvent le champ 'type' principal) existe déjà
        # On ne peut pas mettre à jour cet objet car il créerait un doublon.
        print(f"Conflit de traduction pour '{original_text}' -> '{translated_fr}' existe déjà.")
        return False
    return True

def translate_genre(genre_obj):
    """
    Traduit un objet Genre dans les 3 langues (FR, EN, NL) via LibreTranslate.
    """
    from django.db import IntegrityError
    original_text = genre_obj.name
    if not original_text:
        return

    # Traduire vers les langues cibles
    translated_fr = translate_text(original_text, 'fr')
    translated_en = translate_text(original_text, 'en')
    translated_nl = translate_text(original_text, 'nl')
    
    try:
        genre_obj.name_fr = translated_fr
        genre_obj.name_en = translated_en
        genre_obj.name_nl = translated_nl
        genre_obj.save()
    except IntegrityError:
        print(f"Conflit de traduction pour le genre '{original_text}' -> '{translated_fr}' existe déjà.")
        return False
    return True

def translate_press_article(article_obj):
    """
    Traduit un objet PressArticle dans les 3 langues (FR, EN, NL) via LibreTranslate.
    """
    fields_to_translate = ['title', 'summary', 'content']
    langs = ['fr', 'en', 'nl']
    
    for field in fields_to_translate:
        original_text = getattr(article_obj, field)
        if original_text:
            for lang in langs:
                translated_field = f"{field}_{lang}"
                setattr(article_obj, translated_field, translate_text(original_text, lang))
    
    article_obj.save()
