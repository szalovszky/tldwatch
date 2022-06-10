import unicodedata
import requests
import json
from difflib import SequenceMatcher

class data:
    def asciify(string):
        return unicodedata.normalize('NFD', string).encode('ascii', 'ignore').decode()

class dns:
    def get(domain):
        try:
            result = requests.get(f"https://dns.google/resolve?name={domain}")
            result = json.loads(result.content)
            if(result['Status'] != 0):
                return False
            return result['Answer']
        except:
            return None