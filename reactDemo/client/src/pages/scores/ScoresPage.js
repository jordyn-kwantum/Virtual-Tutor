import React, { useEffect, useState } from 'react'
import httpClient from '../../httpClient'
import { FINNISH_MODE } from '../..'


const ScoresPage = () => {
    const [gameState, setGameState] = useState(0)
    const [scores, setScores] = useState([])
    const [maxScores, setMaxScores] = useState([])
    const [answers, setAnswers] = useState([])
    const [trueQuestion, setTrueQuestion] = useState([])
    const [givenQuestions, setGivenQuestions] = useState([])

    useEffect(() => {
        (async () => {
            httpClient.get("/api/GetGameState").then(function (result) {
                let gState = parseInt(result.data["GameState"])
                setGameState(gState)
                // console.log(gState)
            }).catch(function (err) {
                console.log(err)
            })
            try {
                const resp = await httpClient.get("/api/getScores")
                console.log(resp.data)
                let s = []
                let sMax = []
                let gq = []
                let tq = []
                let a = []
                for (let i = 0; i < resp.data["scores"].length; i++) {
                    s.push(resp.data["scores"][i]["score"])
                    sMax.push(resp.data["scores"][i]["maxscore"])
                    a.push(resp.data["scores"][i]["Answer"])
                    gq.push(resp.data["scores"][i]["GivenQuestion"])
                    tq.push(resp.data["scores"][i]["TrueQuestion"])
                }
                setScores(s)
                setMaxScores(sMax)
                setTrueQuestion(tq)
                setAnswers(a)
                setGivenQuestions(gq)

            }
            catch (err) {
                console.log(err)
            }
        })();

    }, []);


    function GeneratePage() {
        if (gameState === 5) {
            let block = []
            for (let i = 0; i < scores.length; i++) {
                let team2Score = scores[i]
                let team1Score = maxScores[i] - team2Score
                let correct = (team2Score >= team1Score) ? "cor" : "incor"
                block.push(
                    <div key={"score_" + i.toString()} className={"row " + correct}>
                        <div className='col'>
                            {(team2Score >= team1Score) ?
                                <>Team 2</>
                                :
                                <>Team 1</>
                            }
                        </div>
                        <div className='col'>
                            {answers[i]}
                        </div>
                        <div className='col'>
                            {trueQuestion[i]}
                        </div>
                        <div className='col'>
                            {givenQuestions[i]}
                        </div>
                    </div>
                )
            }
            let winner = GetWinner()
            return (

                <div>
                    {winner}
                    <div className='row'>
                        <div className='col'>
                        {FINNISH_MODE ? "Voittaja":"Winner"}
                        </div>
                        <div className='col'>
                        {FINNISH_MODE ? "Vastaus":"Answer"}
                        </div>
                        <div className='col'>
                        {FINNISH_MODE ? "Tosi Kysymys":"True Question"}
                        </div>
                        <div className='col'>
                            {FINNISH_MODE ? "Team 2 Kysymys Arvaa":"Team 2 Question Guess"}
                        </div>
                    </div>
                    {block}
                </div>

            )
        }
        else {
            return <div>{FINNISH_MODE ? "Peli ei ole vielä päättynyt. Päivitä sivu, kun peli on ohi.":"Game is not yet finished. Please referesh the page when the game is over."}</div>
        }

    }

    function GetWinner() {
        let Team1sum = 0;
        let Team2sum = 0;
        for (let i = 0; i < scores.length; i++) {
            Team2sum += scores[i]
            Team1sum += maxScores[i] - scores[i]
        }
        if (Team2sum === Team1sum) {
            return (<div><h1>{FINNISH_MODE? "Se on solmio" : "It is a Tie"}</h1></div>)
        }
        else if (Team2sum > Team1sum) {
            return (<div><h1>{FINNISH_MODE ? "Joukkue 2 voittaa " + {Team2sum} + "pisteellä" : "Team 2 Wins with "+ {Team2sum} + "points"}</h1></div>)
        } else {
            return (<div><h1>{FINNISH_MODE ? "Joukkue 1 voittaa " + {Team1sum} + "pisteellä" : "Team 1 Wins with "+ {Team1sum} + "points"}</h1></div>)
        }
    }

    return (
        GeneratePage()
    )
}

export default ScoresPage