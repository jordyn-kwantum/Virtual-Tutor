import React, { useState, useEffect } from 'react'
import httpClient from '../../httpClient';
import '../main.css'
import { FINNISH_MODE } from '../..';


const MakeQuestions = () => {

    const [questionBoxes, setQuestionBoxes] = useState([1, 2, 3]);
    const [questions, setQuestions] = useState(["", "", ""])
    const [answers, setAnswers] = useState(["", "", ""])
    const [title, setTitle] = useState("")
    const [paragraphs, setParapgraphs] = useState([])
    const [gameState, setGameState] = useState(0)

    useEffect(() => {
        (
            async () => {
                httpClient.get("/api/GetGameState").then(function (result) {
                    let gState = parseInt(result.data["GameState"])
                    setGameState(gState)
                    console.log(gState)
                }).catch(function (err) {
                    console.log(err)
                })
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
            if (questions[i]) {
                data.push(
                    {
                        "question": questions[i],
                        "answer": answers[i],
                    }
                )
            }
        }


        httpClient.post("/api/AddQuestions", {
            "QApairs": data
        }).then(() => {
            window.location.href = "/Team1Page/Group";
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
        console.log(answers)

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


    function QuestionBoxesBlock() {
        if (gameState === 1) {
            return (<div>
                        <form id="AddingQuestionsForm" onSubmit={(e) => {
                        e.preventDefault();}}>
                            <div class='ask-table'>
                                <h3>{FINNISH_MODE ? "Esitä joitakin kysymyksiä!" : "Ask Some Questions!"}</h3>
                                <table>
                                    <thead>
                                        <tr>
                                            <th>{FINNISH_MODE ? "Kysymys" : "Question"}</th>
                                            <th>{FINNISH_MODE ? "Vastaus" : "Answer"}</th>
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
                                            </tr>
                                        )}
                                    </tbody>
                                </table>
                                <div>
                                <button class='button3' type="button" onClick={() => {
                                    addAnotherQuestion();
                                }}>{FINNISH_MODE? "Lisää toinen kysymys" : "Add Another Question"}</button>
                                <button class='button3' type="button" onClick={() => {
                                    removeAQuestion();
                                }}>{FINNISH_MODE? "Poista kysymys" : "Remove question"}</button>
                                </div>
                                <button class='button4' type="button" onClick={() => {
                                sendQuestions();
                                }}>{FINNISH_MODE ? "Lähetä" :"Submit"}</button>
                            </div>
                        </form>
                    </div>
            )
        } else if (gameState === 3){
            window.location.href = "/Team1Page/Group";
        }
        else {
            return (<div></div>)
        }
    }


    function GeneratePage() {
        let block = []
        if (gameState === 1 || gameState === 4) {
            if (title === "") {
                return (
                    <div key="loading">
                        <h4>Loading...</h4>
                    </div>
                )
            }
            else {
                for (var i = 0; i < paragraphs.length; i++) {
                    block.push(<p key={"para_" + i.toString()}> {paragraphs[i]} </p>)
                }
                return (
                    <div>
                        <header>
                            <div id='nav'>
                                <a class='button3' href='/'>Back</a>
                            </div>
                            <h2 id='title'>{FINNISH_MODE ? "Joukkueen 1 sivu" : "Team 1 Page"}</h2>
                        </header>
                        <section class='read-ask-grid'>
                            <div class='instructions'>
                                <h4>{FINNISH_MODE ? "Ohjeet:" : "Instructions:"}</h4>
                                <p>{FINNISH_MODE ? "Tee tästä tekstistä kysymyksiä luokkatovereillesi. Jos pystyt tyrmäämään ne, voitat pisteitä!":"Make some questions about this text for your fellow class mates. If you can manage to stump them, you win points!"}</p>
                            </div>
                            <div class='reading-ask'>
                                {block}
                            </div>
                            <div class='question-block'>
                                {QuestionBoxesBlock()}
                            </div>
                        </section>                           
                    </div>
                )
            }
        }
        else {
            return (<div>
                    <h4>{FINNISH_MODE? "Peli ei ole vielä alkanut. Päivitä tämä sivu myöhemmin." : "The game has not yet started. Please refresh this page later."}</h4>
                </div>)
        }
    }


    return (
        GeneratePage()
    )
}

export default MakeQuestions