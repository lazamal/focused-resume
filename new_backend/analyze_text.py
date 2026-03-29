import os
import spacy


MODEL_PATH = os.path.join(os.environ.get('LAMBDA_TASK_ROOT'), "models", "skill-extractor")

def load_skill_model():
  
    nlp = spacy.load(MODEL_PATH)

   
    if "entity_ruler" not in nlp.pipe_names:
        ruler = nlp.add_pipe("entity_ruler", before="ner")
        patterns = [
            {"label": "SKILLS", "pattern": "React.js"},
            {"label": "SKILLS", "pattern": "Node.js"},
            {"label": "SKILLS", "pattern": "RAG"},
            {"label": "SKILLS", "pattern": "pyTorch"},
            {"label": "SKILLS", "pattern": "prompt engineering"},
            {"label": "SKILLS", "pattern": "MLflow"},
            {"label": "SKILLS", "pattern": "Airflow"},
            {"label": "SKILLS", "pattern": "DVC"},
            {"label": "SKILLS", "pattern": "Big data platforms"},
            {"label": "SKILLS", "pattern": "containerization"},
            {"label": "SKILLS", "pattern": ""},
            {"label": "SKILLS", "pattern": "CI/CD"},
            {"label": "SKILLS", "pattern": [{"LOWER": "react.js"}]},
            {"label": "SKILLS", "pattern": [{"LOWER": "reactjs"}]},
        ]
        ruler.add_patterns(patterns)
    return nlp


SKILL_MODEL = load_skill_model()

class Analyze_Text:
    def __init__(self):
    
        self.skill_extractor_model = SKILL_MODEL

    def extract_skills_new_model(self, text):
        if not self.skill_extractor_model:
            return []
        doc = self.skill_extractor_model(text)
        skills = [ent.text.lower() for ent in doc.ents if "SKILLS" in ent.label_]
        return list(set(skills))