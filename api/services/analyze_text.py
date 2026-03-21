import re
import numpy as np
import spacy
from spacy.kb import InMemoryLookupKB
from pathlib import Path
from api.models import Skill
from huggingface_hub import snapshot_download


class Analyze_Text:
    def __init__(self):
        
        self.all_skills = Skill.objects.all()
      

        self.model_path = snapshot_download("amjad-awad/skill-extractor", repo_type="model")
        self.skill_extractor_model = spacy.load(self.model_path)

        if "entity_ruler" not in self.skill_extractor_model.pipe_names:
            self.ruler = self.skill_extractor_model.add_pipe("entity_ruler", before="ner")
        else:
            self.ruler = self.skill_extractor_model.get_pipe("entity_ruler")

        patterns = [
                {"label": "SKILLS", "pattern": "React.js"},
                {"label": "SKILLS", "pattern": "Node.js"},
                {"label": "SKILLS", "pattern": "CI/CD"},
                {"label": "SKILLS", "pattern": [{"LOWER": "react.js"}]},
    {"label": "SKILLS", "pattern": [{"LOWER": "reactjs"}]},
        ]
        self.ruler.add_patterns(patterns)

        # use this
    def extract_skills_new_model(self, text):

        doc = self.skill_extractor_model(text)

        skills = [ ent.text.lower() for ent in doc.ents if "SKILLS" in ent.label_]


        return list(set(skills))
    


    
    # def extract_noun_chunks(self, text):


    #     doc = self.nlp(text)
    #     chunks = list(doc.noun_chunks)
    #     list_to_return = []
    #     for chunk in chunks:
    #         chunk_nlp = self.nlp(chunk.text)
    #         tokens = []
            
    #         for t in chunk_nlp:
    #             if (not t.is_stop and     
    #                 not t.is_punct and 
    #                 not t.like_num and    
    #                 not t.like_email and   
    #                 not t.like_url and 
    #                 t.pos_ != "SYM" and    
    #                 len(t.lemma_) > 2):
                        
    #                     tokens.append(t.text)
            
    #         cleaned_text = " ".join(tokens).strip()
         
    #         if len(cleaned_text) >=3:

    #             list_to_return.append(cleaned_text)
        
    #     list_to_return = sorted(list(set(list_to_return)))
    #     return {
    #         "count": len(list_to_return),
    #         "items": list_to_return
    #     }

    


    
    





