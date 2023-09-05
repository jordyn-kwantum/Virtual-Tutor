from turtle import update
from typing import Dict
from flask import Flask, redirect, url_for, request, render_template
import json
import io
import codecs
import python.parsing as parsing
import python.query as querry
import python.tagging as tagging
import python.summarize as summarize
import nltk

nltk.download("stopwords")
nltk.download("punkt")


def get_assignment():
    with open("SquadDataset/PrimeMinisterDraftAssignment.txt", 'r') as fp:
        text = []
        for line in fp.readlines():
            line = str(line)    
            line = line.strip()
            line = line.replace("\r\n", "")
            text.append(line)

    return text 

app = Flask(__name__)

title, paragraphs = "Finish Prime Ministers", get_assignment() #parsing.get_random_text()
tag = [("title",title.lower().replace(" ", "_"))]
convHistoryFull:Dict[str, list]= {}
convHistory:Dict[str, list] = {}

failedQuestions:Dict[str, list] = {}
unsatisfiedAnswers = {}

@app.route('/')
def index():
   return render_template('index.html')


def renderQuestion(id, q, context = ""):
    answer = querry.querry(q, context = context, filters=[("assignment","primeminister")])
    print(answer)
    # time.sleep(1)
    # print(answer["answers"][0]["id"])
    b = True
    followup = []

    print(answer["answers"][0]["answer"])
    if "answers" in answer and  answer["answers"][0]["answer"] == "No answer found":
        strippedAnswer = "Sorry we dont have an answer for that question"
        failedQuestions[id].append([len(failedQuestions[id]), q, tag])
        b=False
    else:
        strippedAnswer = answer["answers"][0]["answer"]
        # strippedAnswer = answer["answers"][0]["answer"].split("**")[2]
        for prompt in answer["answers"][0]["dialog"]["prompts"]:
            followup.append(prompt["displayText"])
        # for i in range(len(answer["answers"][0]["dialog"]["prompts"])):
        #     followup += answer["answers"][0]["dialog"]["prompts"][i]["displayText"]
    # print(followup)

    convHistoryFull[id].append([len(convHistoryFull[id]), q, answer])
    convHistory[id].append([len(convHistory[id]), q, strippedAnswer])
    return render_template(f'StudentView.html', id = id, title = title, paragraphs = paragraphs, convo=convHistory[id], askGood=b, followup = followup)


@app.route('/StudentView/', methods=['GET'])
def student_general():
    return redirect("/StudentView/0", code=302)

@app.route('/StudentView/<int:id>', methods=['GET', 'POST'])
def student_view(id):
    id = str(id)

    if not (id in convHistory):
        convHistory[id] = []
        convHistoryFull[id] = []
        failedQuestions[id] = []
        unsatisfiedAnswers[id] = []

    if request.method == 'POST':

        if request.form.get('follow') != None:
            q = request.form.get('follow')
            if len(convHistoryFull[id]) > 0:
                # print(convHistoryFull[id][-1][1]["answers"][0]["dialog"]["prompts"][0]["displayText"])
                # print(convHistoryFull[id][-1][1]["answers"][0]["dialog"]["prompts"][0]["qnaId"])
                # return
                return renderQuestion(id, q, (convHistoryFull[id][-1][1], convHistoryFull[id][-1][2]["answers"][0]["id"]))
            else:
                return renderQuestion(id, q)


        if request.form.get('yesaction') == 'Yes':
            tagging.addSuggestion([convHistoryFull[id][-1][2]], [convHistoryFull[id][-1][1]])

            return render_template(f'StudentView.html', id = id,title = title, paragraphs = paragraphs, convo=convHistory[id], askGood=False)
        elif request.form.get("noaction") == "No":
            unsatisfiedAnswers[id].append(convHistoryFull[id][-1])
            return render_template(f'StudentView.html',id = id, title = title, paragraphs = paragraphs, convo=convHistory[id], askGood=False)

        if request.form["question"]!="":
            q = request.form["question"]
            language = summarize.getLanguage(q)
            if language["name"] == "english":
                if len(convHistoryFull[id]) > 0:
                    return renderQuestion(id,q, (convHistoryFull[id][-1][1], convHistoryFull[id][-1][2]["answers"][0]["id"]))
                else:
                    return renderQuestion(id, q)
            else:
                print(f"This Language is believed to be {language['name']}")
                if len(convHistoryFull[id]) > 0:
                    return renderQuestion(id,q, (convHistoryFull[id][-1][1], convHistoryFull[id][-1][2]["answers"][0]["id"]))
                else:
                    return renderQuestion(id, q)

        else:
            return render_template(f'StudentView.html',id = id, title = title, paragraphs = paragraphs, convo=convHistory[id], askGood=False, followup = [])
    else:
        return render_template(f'StudentView.html', id = id, title = title, paragraphs = paragraphs, convo=convHistory[id], askGood=False, followup = [])

@app.route('/TeacherOverview', methods=['GET', 'POST'])
def teacher_general():
    print(convHistory.keys())
    return render_template("TeacherOverview.html", students=convHistory.keys(), fails = failedQuestions, unhappy = unsatisfiedAnswers)


@app.route('/TeacherOverview/NewQuestion', methods=['GET', 'POST'])
def newquestion_page():
    if request.method == 'POST':
        # print(request.form)
        newq =request.form.get("newq")
        answer = request.form.get("answer")
        tags = request.form.get("tags")
        tags = tags.split("\n")
        newtag = []
        for t in tags:
            t2 = t.strip().split(":")
            newtag.append((t2[0], t2[1]))
        source = request.form.get("source")
        r = tagging.addQuestion(newq, answer, source, newtag)
        return redirect("/TeacherOverview", code=302)

    else:
        question = request.args.get('question', None)
        return render_template('NewQuestion.html', q = question)

@app.route('/TeacherOverview/UpdateQuestion', methods=["GET", "POST"])
def updatequestion_page():
    if request.method == 'POST':
        updatedq =request.form.get("newq")
        answer = request.form.get("answer")
        qid = request.form.get("qid")
        key = request.form.get("key")

        id = unsatisfiedAnswers[key][qid][2]["answers"][0]["id"]
        source = unsatisfiedAnswers[key][qid][2]["answers"][0]["source"]

        tags = request.form.get("tags")
        tags = tags.split("\n")
        newtag = []
        for t in tags:
            t2 = t.strip().split(":")
            newtag.append((t2[0], t2[1]))

        r =tagging.updateQuestion(id, updatedq, answer, source, newtag)
        return redirect("/TeacherOverview", code=302)

    else:
        key = request.args.get("key", None)
        key = key
        qid = request.args.get("qid", None)
        qid = int(qid)

        print(key, qid)

        qa = ""
        if request.args.get("type", None) == "unhappy":
            qa = convHistoryFull[key][qid]
        if request.args.get("type", None) == "normal":
            qa = convHistoryFull[key][qid]

        return render_template("UpdateQuestion.html",key = key, qa = qa)

@app.route('/TeacherSpecificStudentOverview/<int:id>', methods=['GET', 'POST'])
def teacher_view(id):
    id = str(id)
    print(convHistoryFull[id])


    text = ""
    for elem in convHistoryFull[id]:
        text+= elem[1] + "."
        # text+= elem[2]["answers"][0]["answer"].split("**")[2] + "."
        text+= elem[2]["answers"][0]["answer"]+"."

    summary =summarize.summarize(text)

    history = convHistoryFull[id]
    return render_template('TeacherSpecificStudentOverview.html', id = id, history=convHistoryFull[id], fails = failedQuestions[id], unhappy = unsatisfiedAnswers[id], summary=summary)


if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug = True)
