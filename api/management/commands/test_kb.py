import spacy
from spacy.kb import InMemoryLookupKB
from django.core.management.base import BaseCommand
from pathlib import Path
from api.services.analyze_text import Analyze_Text

class Command(BaseCommand):
    help = 'בודק שה-Knowledge Base נטען ועובד'

    def handle(self, *args, **options):
   
            # א. ייבוא הקלאס (בהנחה ששמרת אותו ב-api/services.py)
 

        # ב. יצירת מופע של האנלייזר (זה ייקח כמה שניות כי הוא טוען את ה-NLP וה-KB)
        analyzer = Analyze_Text()

        # ג. טעינת הסקילים מה-DB לתוך ה-Ruler
        # שים לב: בגרסה שלך צריך לקרוא לזה ידנית
        analyzer.add_skills_to_ruler()

        # ד. הרצת הבדיקה על טקסט חופשי
        text = "python, django and machine learning"
        # results = analyzer.analyze_entity_ruler(text)
        # semantic_results = analyzer.analyze_similarity_vs_kb(text)
        chunks = analyzer.extract_noun_chunks(text)

        # ה. הדפסת התוצאות
        # self.stdout.write(self.style.SUCCESS(results))
        self.stdout.write(self.style.SUCCESS(chunks))