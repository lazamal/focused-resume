from gliner import GLiNER

class Analyze_Gliner:
    def __init__(self):

        self.model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

        self.labels = [
            'tasks'
                    "technical",
                    "responsibility",
               
                ]

    def analyze(self, text):

        entities = self.model.predict_entities(text, self.labels, threshold=0.1, max_len=1024, flat_ner=True,)

        entities_to_return = [{'text': entity['text'], 'label':entity['label']} for entity in entities if len(entity['text'].split())>3]
        return entities_to_return
