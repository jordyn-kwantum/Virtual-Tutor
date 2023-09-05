import requests
import json
import random
from typing import List, Dict, Tuple
import python.info as i
import pickle


def querry(question, context =None, filters:List[Tuple[str, str]] = None):
    data = {
        "question": question,
        "top": 3,
        "confidenceScoreThreshold": 0.2,
        "includeUnstructuredSources": True
    }

    if context is not None and len(context) > 0:
        data["context"] = {
            "previousUserQuery":context[0],
            "previousQnaId":context[1]
        }

    if filters is not None and len(filters)> 0:
        data["filters"] ={
            "metadataFilter":{
            "logicalOperation":"AND",
            "metadata":[]
            }
        }
        for f in filters:
            md = {
            "key":f[0],
            "value":f[1]
            }
            data["filters"]["metadataFilter"]["metadata"].append(md)

    datajs = json.dumps(data)

    r = requests.post(url = i.QAendpoint, headers = i.headers, data = datajs)
    j = json.loads(r.text)
    return j
