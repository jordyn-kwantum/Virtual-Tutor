import React, { useState, useEffect } from 'react'
import httpClient from '../../httpClient';
import { FINNISH_MODE } from '../..';

const TeacherAddQuestions = () => {
  const [questionBoxes, setQuestionBoxes] = useState([1]);
  const [questions, setQuestions] = useState([])
  const [answers, setAnswers] = useState([])
  const [rating, setRating] = useState(["good"])
  const [title, setTitle] = useState("")
  const [paragraphs, setParapgraphs] = useState([])

  useEffect(() => {
      (async () => {
          try {
              const resp = await httpClient.get("/api/GetAssignment");
              console.log(resp.data)
              setTitle(resp.data["title"]);
              setParapgraphs(resp.data["text"])
          }
          catch (err) {
              console.log(err)
          }

      })();

  }, []);


  const sendQuestions = async () => {
    console.log(questions)
    console.log(answers)


    let data = []
    for (let i = 0; i < questions.length; i++) {
      data.push(
        {
          "question": questions[i],
          "answer": answers[i],
          "rating":rating[i],
        }
      )
    }


    httpClient.post("/api/AddQuestionsTeacher", {
      "QApairs": data
    }).then(() => {
      window.location.href = "/TeacherDashboard";
    }).catch(err => {
      console.log(err);
    })

  }
  function addAnotherQuestion(e) {
    if (questionBoxes.length >= 10) { return }
    setQuestionBoxes([...questionBoxes, questionBoxes[questionBoxes.length - 1] + 1])
    if (questions.length === 1) {
      setQuestions([questions[0], ""])
    } else {
      setQuestions([...questions, ""])
    }
    if (answers.length === 1) {
      setAnswers([answers[0], ""])
    } else {
      setAnswers([...answers, ""])
    }
    if (rating.length === 1) {
      setRating([rating[0], "good"])
    } else {
      setRating([...rating, "good"])
    }
  }

  function removeAQuestion(e) {
    if (questionBoxes.length === 1) { return }
    questionBoxes.pop()
    questions.pop()
    answers.pop()
    setQuestionBoxes([...questionBoxes])
    setQuestions([...questions])
    setAnswers([...answers])
  }

  function GeneratePage() {
    let block = []
    if (title === "") {
      return (
        <div key="loading">
          <p>Loading...</p>
        </div>
      )
    }
    else {
      for (var i = 0; i < paragraphs.length; i++) {
        block.push(<p key={"para_" + i.toString()}> {paragraphs[i]} </p>)
      }
      return (
        <div>
          <header></header>
          <section class='read-ask-grid'>
            <div className='reading-ask'>
              {block}
            </div>

            <div id='instructions'>
              <h4>&ldquo;{title}&rdquo;</h4>
              <p>{FINNISH_MODE ? "Lue artikkeli ja luo kysymyksiä käytettäväksi tulevissa peleissä." : "Read the article and define questions to be used in future games."}</p>
            </div>

            <div class='question-block'>
              <form id="AddingQuestionsForm" onSubmit={(e) => {
                e.preventDefault();
              }
              }>
                  <div class='ask-table'>
                    <h3>{FINNISH_MODE ? "Lisää kysymyksiä" : "Add Questions"}</h3>
                    <table>
                      <thead>
                        <tr>
                          <th>{FINNISH_MODE ? "Kysymys" : "Question"}</th>
                          <th>{FINNISH_MODE ? "Vastaus" : "Answer"}</th>
                          {/* <th>Rating</th> */}
                        </tr>
                      </thead>
                      <tbody>
                        {questionBoxes.map((i) =>
                          <tr key={i}>
                            {/* <label>Question</label> */}
                            <td>
                              <textarea form="AddingQuestionsForm" defaultValue="" rows="2" columns="50" onChange={(e) => {
                                if (questions.length === 0 || questions.length === 1) {
                                  setQuestions([e.target.value])
                                }
                                else {
                                  let items = [...questions];
                                  items[i - 1] = e.target.value
                                  setQuestions(items)
                                }
                              }} />
                            </td>
                            <td>
                              <textarea form="AddingQuestionsForm" defaultValue="" rows="2" columns="20" onChange={(e) => {
                                if (answers.length === 0 || answers.length === 1) {
                                  setAnswers([e.target.value])
                                }
                                else {
                                  let items = [...answers];
                                  items[i - 1] = e.target.value
                                  setAnswers(items)
                                }
                              }} />
                            </td>
                            {/* <td>
                            <select name="question" id={"question_" +i.toString()} onChange = {e => {
                              
                              if (rating.length === 0 || rating.length === 1) {
                                setRating([e.target.value])
                              }
                              else {
                                let items = [...rating];
                                items[i - 1] = e.target.value
                                setRating(items)
                              }
                            }} >
                              <option value="3">Good</option>
                              <option value="2">Ok</option>
                              <option value="1">Bad</option>
                            </select>
                            </td> */}
                          </tr>
                        )}
                      </tbody>
                    </table>
                  <div>
                  <button class='button3' type="button" onClick={() => {
                    addAnotherQuestion();
                  }}>{FINNISH_MODE ? "Lisää kysymys" : "Add question"}</button>
                  <button class='button3' type="button" onClick={() => {
                    removeAQuestion();
                  }}>{FINNISH_MODE ? "Poista kysymys" : "Remove question"}</button>
                  </div>
                  <button class='button4' type="button" onClick={() => {
                    sendQuestions()
                  }}>{FINNISH_MODE ? "Lähetä" : "Submit"}</button>
                </div>
              </form>

            </div>
          </section>
        </div>
      )
    }
  }

  return (
    GeneratePage()
  )
}



export default TeacherAddQuestions