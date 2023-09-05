## Overview of the python scripts

Info: this file has information that is necessary for making API calls to azure. The key that is used as well endpoints and header information.

parsing: This file reads in the raw data of the squad datset and manipulates the data in a usable form

Query: This file is used for querying the azure QnA system by means of API calls.

Summarize: This file is used to call the API for the azure cognitive system conversation summarization tool
For additional documentation on the summarization tool see:
https://learn.microsoft.com/en-us/azure/cognitive-services/language-service/summarization/overview?tabs=document-summarization

Tagging: This file has multiple functionalities. It has methods for automatically tagging files that are uploaded.  Getting the list of all questions. Updating questions with new fields. Adding new questions to the database. And adding feedback and suggestion to questions. This feedback may be seen in the Azure environment.

For additional documentation on the API for the custom question and answering system of Azure please see:

https://learn.microsoft.com/en-us/azure/cognitive-services/language-service/question-answering/overview
https://learn.microsoft.com/en-us/rest/api/cognitiveservices/questionanswering/question-answering
