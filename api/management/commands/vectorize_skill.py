from pathlib import Path
import re
from django.core.management.base import BaseCommand, CommandError
from api.models import Skill
import spacy
from spacy.kb import InMemoryLookupKB




class Command(BaseCommand):

    def handle(self, *args, **options):

        nlp = spacy.load('en_core_web_md')
        vocab = nlp.vocab
        kb = InMemoryLookupKB(vocab=vocab, entity_vector_length=300)
        all_skills = Skill.objects.all()

        for skill in all_skills:
            name = skill.name.strip() or ""
            alt_name = skill.alt_name.strip() or ""
            description = skill.description.strip() or ""

   
            combined_text = f"{name} | {alt_name} | {description}"

            combined_text_doc = nlp(combined_text)
            combined_text_vector = combined_text_doc.vector
            kb.add_entity(entity = str(skill.id), entity_vector = combined_text_vector, freq = 342 )
            
            text_to_process = [name,alt_name]

            for text in text_to_process:
                text_clean = re.sub(r'\s*\([^)]*\)', '', text).strip()
                text_doc = nlp(text)
                text_no_punct = re.sub(r'[^\w\s()]', "", text)
                lemmatized_text = " ".join([token.lemma_ for token in text_doc])

                aliases_to_add = { text_no_punct , lemmatized_text, text_clean.lower() }

                for alias in aliases_to_add:
                    if alias and alias.lower() != "nan":
                        kb.add_alias(alias = alias, entities = [str(skill.id)], probabilities = [1.0])
            


        root_path = Path(r"D:\Coding\focused-resume\api\skill_KB")
        nlp_path = root_path / "skill_nlp"
        kb_path = root_path / "skill_kb_file"
        kb.to_disk(kb_path)
        nlp.to_disk(nlp_path)
        self.stdout.write(self.style.SUCCESS('Successfully created KB!'))
        


        
