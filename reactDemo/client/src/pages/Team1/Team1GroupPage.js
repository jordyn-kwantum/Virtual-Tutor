import React, { useState, useEffect } from 'react'
import httpClient from '../../httpClient';
import "../main.css"
import { FINNISH_MODE } from '../..';

const Team1GroupPage = () => {

    const [count, setCount] = useState(0);
    const [questionObject, setQuestionObject] = useState([])
    const [selectedQuestions, setSelectedQuestions] = useState([])
    const [remainingSlots, setRemainingSlots] = useState(5)
    const [gameState, setGameState] = useState(0)


    const tick = () => {
        //let newCount = count < 60 ? count + 1 : 0
        setCount((prevState) => prevState < 20 ? prevState + 1 : 0);
    }

    useEffect(() => {
        const timer = setInterval(() => tick(), 1000);
        return () => clearInterval(timer);
    });

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
            })();

    }, []);


    useEffect(() => {
        if (count === 0) {
            let tempQs = []
            let numLeft = 5
            httpClient.get("/api/GetQAPairsStudent").then(function (result) {
                for (let elem of result.data) {
                    tempQs.push(elem);
                    if (elem["selected"]){
                        numLeft -=1
                    }
                }
                setQuestionObject(tempQs)
                setRemainingSlots(numLeft)
            }).catch((e) => console.log(e));
        }
    }, [count]);


    function addQuestion(id, checked) {
        if (checked) {
            selectedQuestions.push(id)
            setSelectedQuestions(selectedQuestions)
            setRemainingSlots(remainingSlots - 1)
        }
        else {
            const index = selectedQuestions.indexOf(id);
            if (index > -1) { // only splice array when item is found
                selectedQuestions.splice(index, 1); // 2nd parameter means remove one item only
                setRemainingSlots(remainingSlots + 1)
            }
            setSelectedQuestions(selectedQuestions)

        }
        console.log(selectedQuestions)
    }

    function submitPage() {
        if (remainingSlots < 0) {
            let text = FINNISH_MODE ? "Liian monta kysymystä valit" :"Too many questions selected"
            alert(text)
            return
        }
        httpClient.post("/api/StudentSubmitQuestions", { "ids": selectedQuestions }).then(() => {
            window.location.href = "/";
        }).catch(e => {
            console.log(e);
        })
    }

    function GeneratePage() {
        let block = []
        for (let i = 0; i < questionObject.length; i++) {
            if (questionObject[i].selected) {
                block.push(<div key={"pair_" + i.toString()} className="row">
                        <div className='col'>
                            <b>{questionObject[i]["question"]}</b>
                        </div>
                        <div className='col'>
                            <b>{questionObject[i]["answer"]}</b>
                        </div>

                        <div className='col'>
                        </div>
                    
                </div>
                )
            }
            else {
                block.push(<div key={"pair_" + i.toString()} className="row">
                    <div className='col'>
                        {questionObject[i]["question"]}
                    </div>
                    <div className='col'>
                        {questionObject[i]["answer"]}
                    </div>

                    <div className='col'>
                        <input type='checkbox' id={"checkbox_" + i.toString()} onClick={(e) => addQuestion(questionObject[i]["id"], e.target.checked)}></input>
                    </div>
                </div>
                )
            }
        }

        return ((gameState === 1 || gameState === 3) ?
            <div>
                <header><h1 className='header'>{FINNISH_MODE ? "Valitse Kysymykset ryhmänä": "Select Questions as a Group"}</h1></header>
                <br></br>
                <h2>{FINNISH_MODE ? "Luettelo ajankohtaisista kysymyksistä, valitse 5 parasta vastustajasi tyrmäämiseksi":"List of current questions, pick the top 5 to stump your opponents" } </h2>
                <div className='row'>
                    <div className='col'>
                        <h2>{FINNISH_MODE ? "Kysymys" : "Question"}</h2>
                    </div>
                    <div className='col'>
                        <h2>{FINNISH_MODE ? "Vastaus" : "Answer"}</h2>
                    </div>
                    <div className='col'>
                        <h2>{FINNISH_MODE ? "valittu" : "Selected"}</h2>
                    </div>
                </div>
                {block}
                <div>

                    <h3>{FINNISH_MODE ? "Oletko valmis lähtemään?" : "Ready to go?"} <button onClick={() => { submitPage() }}>Submit</button></h3>
                </div>
            </div> :
            <div>{FINNISH_MODE ? "Sivu ei ole käytettävissä tällä hetkellä." :"Page not Available at this time." }</div>
        )

    }

    return (GeneratePage())
}

export default Team1GroupPage