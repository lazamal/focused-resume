import json
import base64
from new_backend.views2 import AnalyzeCV  

# Initialize the analyzer outside the handler to keep it warm across requests
analyzer_engine = AnalyzeCV()
def handler(event, context):
    try:
  
        print('initiated analyzer_engine')
        return analyzer_engine.post(event)



    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Internal Server Error: {str(e)}"})
        }