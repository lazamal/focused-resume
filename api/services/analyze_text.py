import re
import numpy as np
import spacy
from spacy.kb import InMemoryLookupKB
from pathlib import Path
from api.models import Skill
from huggingface_hub import snapshot_download


class Analyze_Text:
    def __init__(self):
        
        root = Path(r'D:\Coding\focused-resume\api\skill_KB')
        self.nlp = spacy.load(root / 'skill_nlp')
        self.kb = InMemoryLookupKB(vocab=self.nlp.vocab, entity_vector_length=300)
        self.kb.from_disk(root / "skill_kb_file")
        self.ruler = self.nlp.add_pipe('entity_ruler', before="ner", config={"phrase_matcher_attr": "LOWER"})
        self.all_skills = Skill.objects.all()
        self.add_skills_to_ruler()

        self.model_path = snapshot_download("amjad-awad/skill-extractor", repo_type="model")
        self.skill_extractor_model = spacy.load(self.model_path)

        
    def add_skills_to_ruler(self):
        patterns = []
  
        
        for skill in self.all_skills:
            clean_name = re.sub(r'\s*\([^)]*\)', '', skill.name).strip()
            patterns.append({
                "label": "SKILL",
                "pattern": clean_name,
                "id": str(skill.id)
            })
        self.ruler.add_patterns(patterns)

    def analyze_entity_ruler(self,text):
        doc = self.nlp(text)
        results =[]

        for ent in doc.ents:
            if ent.label_ == "SKILL":
                candidates = self.kb.get_alias_candidates(ent.text.lower())
                if candidates:
                    for candidate in candidates:
                        results.append({
                            "text": ent.text,
                            'id': candidate.entity_,
                            "confidence": candidate.prior_prob

                        })
        return results
    
    def analyze_semilariy(self,text1, thershold = 0.8):
        doc1 = self.nlp(text1)
        semantic_results = []
        tokens_to_check = [t for t in doc1 if not t.is_stop and not t.is_punct and t.has_vector]
        if not tokens_to_check:
            return []
        
     
        for token in tokens_to_check:
            for skill in self.all_skills:
        
                skill_doc = self.nlp(skill.name)
                similarity = token.similarity(skill_doc)
                if similarity >= thershold:
                    semantic_results.append({
                        "skill_name": skill.name,
                        "similarity": round(similarity,2),
                        "id": skill.id,
                    })
            return sorted(semantic_results, key=lambda x: x['similarity'], reverse=True)
        
    


    def analyze_similarity_vs_kb(self, text, threshold=0.85):
        doc = self.nlp(text)
        entity_ids = self.kb.get_entity_strings()
        semantic_results = []
        
        tokens_to_check = [t for t in doc if not t.is_stop and not t.is_punct and t.has_vector]

        for token in tokens_to_check:
            for ent_id in entity_ids:
         
                raw_vector = self.kb.get_vector(ent_id)
                skill_vector = np.array(raw_vector)
                
                if np.all(skill_vector == 0):
                    continue

                norm_b = np.linalg.norm(skill_vector)
                if norm_b == 0:
                    continue

                sim = np.dot(token.vector, skill_vector) / (token.vector_norm * norm_b)

                if sim >= threshold:
                    semantic_results.append({
                        "token": token.text,
                        "skill_id": ent_id,
                        "similarity": round(float(sim), 2)
                    })

  
        return sorted(semantic_results, key=lambda x: x['similarity'], reverse=True)
    
    def analyze_2_texts(self, text1, text2):
        
        doc1 = self.nlp(text1)
        doc2 = self.nlp(text2)
        similarity = doc1.similarity(doc2)
        return  similarity
    
    def extract_noun_chunks(self, text):


        doc = self.nlp(text)
        chunks = list(doc.noun_chunks)
        list_to_return = []
        for chunk in chunks:
            chunk_nlp = self.nlp(chunk.text)
            tokens = []
            
            for t in chunk_nlp:
                if (not t.is_stop and     
                    not t.is_punct and 
                    not t.like_num and    
                    not t.like_email and   
                    not t.like_url and 
                    t.pos_ != "SYM" and    
                    len(t.lemma_) > 2):
                        
                        tokens.append(t.text)
            
            cleaned_text = " ".join(tokens).strip()
         
            if len(cleaned_text) >=3:

                list_to_return.append(cleaned_text)
        
        list_to_return = sorted(list(set(list_to_return)))
        return {
            "count": len(list_to_return),
            "items": list_to_return
        }
    def extract_entities(self, text):
        doc = self.nlp(text)
        ents_list = []

        for ent in doc.ents:
            ents_list.append(ent.text)
            
        return ents_list
    
    def extract_skills_new_model(self, text):

        doc = self.skill_extractor_model(text)
        skills = [ent.text for ent in doc.ents if "SKILLS" in ent.label_]
        return skills
    
    def extract_skills_new_model2(self, text):


        doc = self.nlp2(text)

        skills = [ent.text for ent in doc.ents]
        return skills

    
    





