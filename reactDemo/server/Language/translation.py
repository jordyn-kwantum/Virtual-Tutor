from typing import List
from config import translationUrl, translationKey, translationLocation, languageAnalysisUrl, headers
from enum import Enum
import uuid
import requests
import json

"""
This file is responsible for the translation
"""


class Language(Enum):
    ENGLISH: str = 'en'
    FINNISH: str = 'fi'
    DUTCH: str = 'nl'


class LanguageException(Exception):
    "The language provided for the translator is not off the correct form"
    pass


class Translator():

    def __init__(self, startLanguage: Language, endLanguage: Language) -> None:

        if not isinstance(startLanguage, Language) or not isinstance(endLanguage, Language):
            raise LanguageException(
                "The language provided for the translator is not off the correct form")

        self.startlanguage = startLanguage
        self.endlanguage = endLanguage

        path = "/translate"
        self.constructed_url = translationUrl + path

        self.create_headers()
        self.createParameters()

    def create_headers(self) -> None:
        self.headers = {
            'Ocp-Apim-Subscription-Key': translationKey,
            # location required if you're using a multi-service or regional (not global) resource.
            'Ocp-Apim-Subscription-Region': translationLocation,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

    def createParameters(self) -> None:
        self.params = {
            'api-version': '3.0',
            'from': self.startlanguage.value,
            'to': [self.endlanguage.value]
        }

    @staticmethod
    def detectLanguage(inputText:List[str])-> List[str]:
        body = {
            "kind":"LanguageDetection",
            "parameters" : {
                "modelVersion": "latest"
            },
            "analysisInput":{
                "documents":[]
            }
        }
        for i, text in enumerate(inputText):
            body["analysisInput"]["documents"].append({  # type:ignore
                "id":str(i+1),
                "text":text
            })
        
        request = requests.post(languageAnalysisUrl, headers=headers, json=body)
        response = request.json()
        detectedLanguages = []

        for resp in response["results"]["documents"]:
            detectedLanguages.append(resp["detectedLanguage"]["iso6391Name"])

        return detectedLanguages


    def translate(self, inputText: List[str]) -> List[str]:
        body = []
        for text in inputText:
            body.append({
                "Text": text
            })
            
        request = requests.post(
            self.constructed_url, params=self.params, headers=self.headers, json=body)
        response = request.json()

        translation = []
        for object in response:
            translation.append(object["translations"][0]["text"])

        return translation


# if __name__ == "__main__":
#     # Translator.detectLanguage(["welke taal is dit?", "and what language is this"])
#     tran = Translator(Language.ENGLISH, Language.FINNISH)
#     backTranslator = Translator(Language.FINNISH, Language.ENGLISH)

#     output = tran.translate(["This is a test of deliberate missspelling of word"])
#     print(output)
#     output = backTranslator.translate(["Tämä on sanan tahallisen kirjoitusvirheen testi"])
#     print(output)