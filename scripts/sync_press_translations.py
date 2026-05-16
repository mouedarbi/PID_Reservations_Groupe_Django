import os
import sys
import django
import requests
import json
import time

# Configuration de l'environnement Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservations.settings')
django.setup()

from catalogue.models.press_article import PressArticle

LIBRETRANSLATE_URL = "http://159.223.211.21:5000/translate"

def translate_text(text, target_lang, source_lang='auto'):
    if not text or not text.strip():
        return text
    
    payload = {
        'q': text,
        'source': source_lang,
        'target': target_lang,
        'format': 'text'
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(LIBRETRANSLATE_URL, data=json.dumps(payload), headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json().get('translatedText', text)
        else:
            print(f"  [Error] LibreTranslate returned status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"  [Error] Translation failed: {e}")
        return None

def sync_press_articles():
    articles = PressArticle.objects.all()
    total = articles.count()
    print(f"Found {total} press articles to check.")
    
    for i, article in enumerate(articles, 1):
        print(f"[{i}/{total}] Checking article: {article.title}")
        
        updated = False
        
        # On assume que la source est le français (langue par défaut du projet)
        # Si title_fr est vide mais title existe, on remplit title_fr
        if not article.title_fr and article.title:
            article.title_fr = article.title
            updated = True
        if not article.summary_fr and article.summary:
            article.summary_fr = article.summary
            updated = True
        if not article.content_fr and article.content:
            article.content_fr = article.content
            updated = True

        # Traduction vers l'anglais (en)
        if not article.title_en:
            print(f"  Translating title to EN...")
            article.title_en = translate_text(article.title_fr, 'en', 'fr')
            updated = article.title_en is not None
        
        if not article.summary_en:
            print(f"  Translating summary to EN...")
            article.summary_en = translate_text(article.summary_fr, 'en', 'fr')
            updated = updated or (article.summary_en is not None)

        if not article.content_en:
            print(f"  Translating content to EN...")
            article.content_en = translate_text(article.content_fr, 'en', 'fr')
            updated = updated or (article.content_en is not None)

        # Traduction vers le néerlandais (nl)
        if not article.title_nl:
            print(f"  Translating title to NL...")
            article.title_nl = translate_text(article.title_fr, 'nl', 'fr')
            updated = updated or (article.title_nl is not None)
        
        if not article.summary_nl:
            print(f"  Translating summary to NL...")
            article.summary_nl = translate_text(article.summary_fr, 'nl', 'fr')
            updated = updated or (article.summary_nl is not None)

        if not article.content_nl:
            print(f"  Translating content to NL...")
            article.content_nl = translate_text(article.content_fr, 'nl', 'fr')
            updated = updated or (article.content_nl is not None)

        if updated:
            article.save()
            print(f"  [Success] Article '{article.title}' updated with translations.")
        else:
            print(f"  [Skip] No missing translations for '{article.title}'.")
        
        # Petit délai pour ne pas surcharger le serveur de traduction
        time.sleep(0.5)

if __name__ == "__main__":
    sync_press_articles()
