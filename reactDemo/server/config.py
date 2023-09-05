from dotenv import load_dotenv
import os
import redis

load_dotenv()
SOURCE:str = "ChatGPT"
FINNISH_MODE:bool = True

database_file_path = os.path.abspath(os.getcwd())+"/Database/project.db"
class ApplicationConfig():
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHELY_ECHO = True 
    SQLALCHEMY_DATABASE_URI =  'sqlite:///' + database_file_path 
    CORS_HEADERS = "Content-Type"

    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url('redis://redis:6379/1') # production
    # SESSION_REDIS = redis.from_url('redis://localhost:6379') #Dev
    

headers = {
    "projectName":"SquadDemo ",
    "api-version":"2021-10-01",
    "deploymentName":"production",
    "Ocp-Apim-Subscription-Key":"6b4cedc723344e79852b272530bd2bb0",
    "Content-Type":"application/json"
}


knowledgeBaseUrl = f"https://cogservtextanalytics1.cognitiveservices.azure.com/language/query-knowledgebases/projects/SquadDemo/qnas?api-version=2021-10-01"
knowledgeBaseQueryUrl = f"https://cogservtextanalytics1.cognitiveservices.azure.com/language/:query-knowledgebases?projectName=SquadDemo&api-version=2021-10-01&deploymentName=production"

# Translation and Language Detection
translationUrl = "https://api.cognitive.microsofttranslator.com"
translationKey = "bd14e09e01044282beade3605b5659a1"
translationLocation = "northcentralus"
languageAnalysisUrl ="https://cogservtextanalytics1.cognitiveservices.azure.com/language/:analyze-text?api-version=2022-05-01"