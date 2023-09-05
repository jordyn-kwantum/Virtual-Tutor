import json
import io
import codecs
import csv
import pickle
import random
def get_random_text():
    with open('SquadDataset/dev-v2.0.json') as f:
        content = f.read()

    js = json.loads(content)
    data = js["data"]

    number_of_para = len(data)
    choice = random.randint(0, number_of_para-1)
    data = data[choice]
    title = data["title"]
    paragraphs = []
    for para in data["paragraphs"]:
        paragraphs.append(para["context"])
    return title, paragraphs

def htmlwriter(number:int):
    with open('../dev-v2.0.json') as f:
        content = f.read()

    total = 0
    js = json.loads(content)
    data = js["data"]

    taggingDict = {}
    for elem in data:

        with codecs.open(f"pdfs/{elem['title']}.html", "w", "utf-8") as f:
            f.writelines("<HTML> <HEAD> </HEAD><BODY>")
            count = 0
            total +=1
            f.writelines("<h1> " + elem["title"].replace("_", " ")+"</h1>\n")
            print(elem["title"])
            count = 0
            for para in elem["paragraphs"]:
                f.writelines("<px>")
                f.writelines(para["context"] + "\n</p>")
            for para in elem["paragraphs"]:
                for ques in para["qas"]:
                    question = ques["question"].replace("?", "")
                    if ques["is_impossible"]:
                        continue
                    else:
                        answer = ques["answers"][0]["text"]
                        if count % 2 == 0:
                            f.writelines("<h1>" + question + "</h1>\n")
                        else:
                            f.writelines("<h2>" + question + "</h2>\n")
                        f.writelines("<p>" + answer + "</p>\n")
                        taggingDict[question.rstrip().encode('ascii', 'ignore')] = {
                        "answer": answer,
                        "tags":{
                        "title":elem["title"]
                        }
                        }
                        count +=1
            f.writelines("</BODY></HTML>")
        with open(f"pdfs/tags{elem['title']}.pickle", 'wb') as f2:
            pickle.dump(taggingDict, f2)


def tsvwriter():

    with open('dev-v2.0.json') as f:
        content = f.read()


    js = json.loads(content)
    data = js["data"]

    count = 10
    with codecs.open("normansqna.tsv", "w", "utf-8") as f:
        tsv_writer = csv.writer(f, delimiter='\t', quotechar=' ',escapechar = "\\")
        tsv_writer.writerow(["Question", "Answer", "Source", "Metadata", "SuggestedQuestions", "IsContextOnly", "Prompts", "QnaId", "SourceDisplayName"])

        for elem in data:
            title = elem["title"]
            paragraphs = elem["paragraphs"]
            for para in paragraphs:
                contex = para["context"]
                qas = para["qas"]

                qas = list(filter(lambda x: not x["is_impossible"], qas))

                numberofQuestions = len(qas)

                for i, quest in enumerate(qas):
                    question = quest["question"]

                    prompt = ""

                    if i % 2 == 0 and i+1<numberofQuestions-1:
                        n = i+1
                        while qas[n]["is_impossible"] and n<numberofQuestions-1: n+=1
                        prompt = "[{\"DisplayOrder\":0, \"QnaId\":"+ str(count+1) +", \"DisplayText\":\""+qas[n]["question"].replace("\"", "\'")+"\"}]"

                    if quest["is_impossible"]:
                        answer = ""
                    else:
                        answer = quest["answers"][0]["text"]
                        tsv_writer.writerow([question, answer, "Normans.pdf", "title:" + title, "[]", "False", prompt, count, "Normans"])
                        count += 1
