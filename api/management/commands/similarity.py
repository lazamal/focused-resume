from pathlib import Path

import spacy
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        root = Path(r'D:\Coding\focused-resume\api\skill_KB')
        nlp = spacy.load(root / 'skill_nlp') 
        doc1 = nlp("I like salty fries and hamburgers.")
        doc2 = nlp("Fast food tastes very good.")

        # Similarity of two documents
        print(doc1, "<->", doc2, doc1.similarity(doc2))
        # Similarity of tokens and spans
        french_fries = doc1[2:4]
        
        burgers = doc1[5]
        print(french_fries, "<->", burgers, french_fries.similarity(burgers))