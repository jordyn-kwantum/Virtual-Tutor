import React, { useEffect, useState } from 'react'
import httpClient from '../../httpClient'
import { FINNISH_MODE } from '../..';


export const Team2Page = () => {

    const [ids, setIds] = useState([])
    const [answers, setAnswers] = useState([])
    const [questions, setQuestions] = useState([])

    const [paragraphs, setParapgraphs] = useState([])
    const [title, setTitle] = useState("")

    const [gameState, setGameState] = useState(0)
    const [toQuestions, setToQuestions] = useState(false)



    const sendQuestions = async () => {
        console.log(questions)
        let data = []
        for (let i = 0; i < questions.length; i++) {
            data.push({
                "id": ids[i],
                "question": questions[i]
            })
        }

        httpClient.post("/api/checkQuestions", {
            "questions": data
        }).then(() => {
            window.location.href = "/"
        }).catch(err => {
            console.log(err)
        })
    }

    useEffect(() => {
        (
            async () => {
                httpClient.get("/api/GetGameState").then(function (result) {
                    let gState = parseInt(result.data["GameState"])
                    setGameState(gState)
                    // console.log(gState)
                }).catch(function (err) {
                    console.log(err)
                })
                try {
                    const resp = await httpClient.get("/api/GetAssignment");
                    // console.log(resp.data)
                    setTitle(resp.data["title"]);
                    setParapgraphs(resp.data["text"])
                }
                catch (err) {
                    console.log(err)
                }
                try {
                    const resp = await httpClient.get("/api/GetAnswers");
                    console.log(resp.data)
                    let c = []
                    let a = []
                    for (let i = 0; i < resp.data["pairs"].length; i++) {
                        c.push(resp.data["pairs"][i]["id"])
                        a.push(resp.data["pairs"][i]["answer"])
                    }
                    
                    setIds(c)
                    setAnswers(a);
                    // console.log(a)
                    let q = []
                    for (let i = 0; i < resp.data.length; i++) {
                        q.push("")
                    }
                    setQuestions(q)
                }
                catch (err) {
                    console.log(err)
                }
            }
        )();
    }, []);


    function GeneratePage() {
        console.log(toQuestions)
        if (!toQuestions && title === "") {
            return (
                <div><p>Loading...</p></div>
            )
        }
        else if (!toQuestions) {
            let block = []
            for (var i = 0; i < paragraphs.length; i++) {
                block.push(<p key={"para_" + i.toString()}> {paragraphs[i]} </p>)
            }
            let but = <div></div>
            if (gameState === 4){
                but = <button class='button4' type="button" onClick={() => { setToQuestions(true); }}>Go</button>
            }
            return (
                <div>
                    <header>
                        <div id='nav'>
                            <a class='button3' href='/'>Back</a>
                        </div>
                        <h2 id='title'>Reading Assignment</h2>
                    </header>
                    <section class='read-ask-grid'>
                    <div class='instructions'>
                        <h4>{FINNISH_MODE? "Ohjeet:": "Instructions:"}</h4>
                        <p>{FINNISH_MODE? "Lue teksti ja yritä muistaa niin paljon kuin mahdollista. Kun olet valmis, paina \"Go\"-painiketta!": "Read the text and try and memorize as much as possible. When you are ready press the \"Go\" button!"}</p>
                        <form>{but}</form>
                    </div>
                    {/* <h1 class='title'>{title}</h1> */}
                    <div class='reading-ask'>
                        <h5>{title}</h5>
                        {block}
                    </div>
                    </section>
                </div>
            )
        }
        else if (toQuestions && questions == null && gameState === 4) {
            return (
                <div><p>Loading...</p></div>
            )
        }
        else if (toQuestions && gameState === 4) return (
            <div>
                <header>
                    <h2 id='title'>Team 2</h2>
                </header>
                <section>
                <section class='text-section'>
                    <h3>{FINNISH_MODE? "Ohjeet:": "Instructions:"}</h3>
                    <p>{FINNISH_MODE? "Tässä on vastauksia joihinkin tekstiä koskeviin kysymyksiin. Voitko esittää kysymyksen, joka vastaa vastausta?": "Here are the answers to the some questions about the text. Can you give the question, that corresponds to the answer?"}</p>
                </section>
                <section class='q-table'>
                <form if="AnsweringQuestionsForm" onSubmit={(e) => {
                    e.preventDefault();
                }}>
                    {answers.map((a, index) =>
                        <div class='game-row' key={index}>
                                <div class='col'>
                                    <h5>{FINNISH_MODE ? "Vastaus" : "Answer"}</h5>
                                    {a}
                                </div>
                                <div class='col'>
                                    <h5>{FINNISH_MODE ? "Anna kysymyksiä": "Give Questions"}</h5>
                                    <textarea class='wide-area' form="AnsweringQuestionsForm defaultValue=" rows="2" columns="50" onChange={(e) => {
                                        let items = [...questions];
                                        items[index] = e.target.value;
                                        setQuestions(items);
                                    }} />
                                </div>
                        </div>
                    )}

                </form>

                <button class='button4' type="button" onClick={() => {
                    sendQuestions()
                }}>
                    {FINNISH_MODE? "Tarkista kysymyksesi!" : "Check your questions!"}
                </button>
                </section>
                </section>
            </div>
        )
    }

    return (GeneratePage()
    )
}

export default Team2Page