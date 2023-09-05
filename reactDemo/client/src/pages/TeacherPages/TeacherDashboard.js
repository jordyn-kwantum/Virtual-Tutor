import React, { useState, useEffect } from 'react'
import httpClient from '../../httpClient'
import "../main.css"
import { FINNISH_MODE } from '../..';


export const TeacherDashboard = () => {

  const [count, setCount] = useState(0)
  const [qaSelectedPairs, setQaLocalSelectedPairs] = useState([])
  const [qaLocalPairs, setQaLocalPairs] = useState([])
  const [qaGlobalPairs, setQaGlobalPairs] = useState([])
  const [gameState, setGameState] = useState([0])

  const tick = () => {
    //let newCount = count < 60 ? count + 1 : 0
    setCount((prevState) => prevState < 20 ? prevState + 1 : 0);
  }

  useEffect(() => {
    const timer = setInterval(() => tick(), 1000);
    return () => clearInterval(timer);
  });



  function updateQuestionRating(i, value) {
    let data = { "id": qaGlobalPairs[i].id, "rating": value }
    console.log(data)
    httpClient.post("/api/updateQuestionRating", {
      "question": data
    }).catch(err => {
      console.log(err)
    })
  }
  function updateLocalQuestionRating(i, value) {
    let data = { "id": qaLocalPairs[i].id, "rating": value }
    console.log(data)
    httpClient.post("/api/updateLocalQuestionRating", {
      "question": data
    }).catch(err => {
      console.log(err)
    })
  }

  function updateSelectedQuestionRating(i, value) {
    let data = { "id": qaSelectedPairs[i].id, "rating": value }
    console.log(data)
    httpClient.post("/api/updateLocalQuestionRating", {
      "question": data
    }).catch(err => {
      console.log(err)
    })
  }


  function getGameState() {
    httpClient.get("/api/GetGameState").then(function (result) {
      let gState = parseInt(result.data["GameState"])
      setGameState(gState)
    }).catch(function (err) {
      console.log(err)
    })
  }

  function getGamestateText() {
    switch (gameState) {
      case 0: return FINNISH_MODE ? "Peliä ei aloitettu" : "Game Not Started";
      case 1: return FINNISH_MODE ? "Joukkueen 1 kierros" :"Team 1 Turn";
      case 2: return FINNISH_MODE ? "Opettajan arviointivuoro" :"Teacher Evaluation Turn";
      case 3: return FINNISH_MODE ? "Ryhmän 1 kysymykset lähetetty takaisin" :"Team 1 Questions Sent Back";
      case 4: return FINNISH_MODE ? "Joukkue 2 Käännös" :"Team 2 Turn";
      case 5: return FINNISH_MODE ? "Pelin loppu" :"Game End";
      default: return FINNISH_MODE ? "Peliä ei aloitettu" :"Game Not Started"
    }
  }


  function getGamestateButton() {
    switch (gameState) {
      case 0: return (<div><button class='button4' onClick={() => startGame()}>{FINNISH_MODE ? "Aloita peli" : "Start Game"}</button></div>);
      case 1: return (<div><button class='button4' onClick={() => endTeam1Turn()}>{FINNISH_MODE ? "Lopeta joukkue 1 kierros" : "End Team 1 Turn"}</button></div>);
      case 2: return (<div><button class='button4' onClick={() => sendBackToTeam1()}>{FINNISH_MODE ? "Lähetä takaisin joukkueelle 1": "Send back to Team 1"}</button><button class='button4' onClick={() => sendToTeam2()}>{FINNISH_MODE? "Lähetä joukkueelle 2":"Send To Team 2"}</button></div>);
      case 3: return (<div><button class='button4' onClick={() => endTeam1Turn()}>{FINNISH_MODE ? "Lopeta joukkue 2 kierros": "End Team 2 Turn"}</button></div>);
      case 4: return (<div><button class='button4' onClick={() => endGame()}>{FINNISH_MODE ? "Loppupeli": "End Game"}</button></div>);
      case 5: return (<div><button class='button4' onClick={() => startGame()}>{FINNISH_MODE ? "Käynnistä peli uudelleen": "Restart Game"}</button></div>);
      default: return (<div><button class='button4' onClick={() => startGame()}>{FINNISH_MODE ? "Aloita peli": "Start Game"}</button></div>);
    }
  }

  function startGame() {
    httpClient.post("/api/startGame", {}).catch(err => {
      console.log(err)
    })

    setGameState(1)
  }

  function sendBackToTeam1() {
    httpClient.post("/api/Team1TurnAgain", {}).catch(err => {
      console.log(err)
    })
    setGameState(3)
  }

  function endTeam1Turn() {
    httpClient.post("/api/Team1TurnEnd", {}).catch(err => {
      console.log(err)
    })
    setGameState(2)
  }

  function sendToTeam2() {
    for (let i = 0; i < qaSelectedPairs.length; i++) {
      if (qaSelectedPairs[i].flag) {
        if (window.confirm(FINNISH_MODE ? "Jäljellä on käsittelemättömiä kysymyksiä.\n\nKaikki kysymykset, joita ei ole lisätty tietokantaan, poistuvat pelin päätyttyä\n\nJatketaanko?" : "There remain questions not handled.\n\nAny questions not added to the DB will be gone after the Game is finished\n\nContinue?")) { break }
        else { return }
      }
    }

    httpClient.post("/api/TeacherTurnEnd", {}).catch(err => {
      console.log(err)
    })
    setGameState(4)
  }

  function endGame() {
    httpClient.post("/api/Team2TurnEnd", {}).catch(err => {
      console.log(err)
    })
    setGameState(5)
  }

  function MergeDB(i) {
    httpClient.post("/api/mergeLocalDBquestionToGlobal", { "id": qaSelectedPairs[i].id }).catch((e) => (console.log(e)));
    getQAPairs()
  }

  function addToDB(i) {
    if (qaSelectedPairs[i].rating === 0) {
      alert("Question Needs a rating")
      return
    }
    httpClient.post("/api/AddLocalQuestionToDB", { "id": qaSelectedPairs[i].id, "newId": qaGlobalPairs[qaGlobalPairs.length - 1]["id"] }).catch((e) => (console.log(e)));
    getQAPairs()
  }

  function AddToCurrent(i) {
    httpClient.post("/api/addGlobalQuestionToCurrent", { "id": qaGlobalPairs[i].id }).catch((e) => (console.log(e)));
    getQAPairs()
  }

  function TakeDBquestion(i) {
    httpClient.post("/api/preferDatabaseFormulation", { "id": qaSelectedPairs[i].id }).catch((e) => (console.log(e)));
    getQAPairs()
  }


  function deleteQuestion(i) {
    httpClient.post("/api/deleteCurrentQuestion", { "id": qaLocalPairs[i].id }).catch((e) => (console.log(e)));
    // getQAPairs()
  }

  function rejectQuestion(i) {
    httpClient.post("/api/rejectCurrentQuestion", { "id": qaSelectedPairs[i].id }).catch((e) => (console.log(e)));
    // getQAPairs()
  }

  async function getQAPairs() {
    try {

      const resp = await httpClient.get("/api/GetQAPairs")
      let selectp = []
      let localp = []
      let globalp = []
      console.log(resp.data)

      for (let i = 0; i < resp.data["pairs"]["local"].length; i++) {
        if (resp.data["pairs"]["local"][i].selected) {
          selectp.push(resp.data["pairs"]["local"][i])
        } else {
          localp.push(resp.data["pairs"]["local"][i])
        }
      }
      setQaLocalSelectedPairs(selectp)
      setQaLocalPairs(localp)

      for (let i = 0; i < resp.data["pairs"]["global"].length; i++) {
        globalp.push(resp.data["pairs"]["global"][i])
      }
      setQaGlobalPairs(globalp)
    }
    catch (err) {
      console.log(err)
    }
  }

  useEffect(() => {
    if (count === 0){
      getQAPairs();
      getGameState();
    }
  }, [count]);




  function GeneratePage() {
    // getGameState()

    let block0 = []
    for (let i = 0; i < qaSelectedPairs.length; i++) {
      let qblock = []
      for (let j = 0; j < qaSelectedPairs[i].questions.length; j++) {
        qblock.push(qaSelectedPairs[i].questions[j] + "\n")
      }

      let additionalAblock
      let AddToDbButton
      if ("A_Answer" in qaSelectedPairs[i] && qaSelectedPairs[i].flag) {
        qblock.push(<br></br>)
        qblock.push(<div className="azureanswer"> {qaSelectedPairs[i]["A_questions"][0]}</div>)
        additionalAblock = <div className="azureanswer">{qaSelectedPairs[i]["A_Answer"]}</div>
        AddToDbButton = <div><button class="button3" id={"a" + i.toString()} onClick={() => MergeDB(i)}>{FINNISH_MODE ? "Lisää alakysymykseksi":"Add as subquestion"}</button><br></br><button class="button3" id={"b" + i.toString()} onClick={() => TakeDBquestion(i)}>{FINNISH_MODE ? "Mieluummin tietokantakysymys":"Prefer Database question"} </button></div>
      } else if (qaSelectedPairs[i].flag) {
        AddToDbButton = <div><button class="button3" onClick={() => addToDB(i)}>{FINNISH_MODE ? "Lisää tietokantaan":"Add to Database"}</button></div>
      }


      block0.push(<div key={"local_pair_" + i.toString()} className="row">
        <div className='col'>
          {qblock}

        </div>
        <div className='col'>
          {qaSelectedPairs[i].answer}<br></br>
          {additionalAblock}
        </div>
        <div className='col'>
          <select name="question" defaultValue={qaSelectedPairs[i].rating} id={"local_question_" + i.toString()} onChange={e => updateSelectedQuestionRating(i, e.target.value)} >
            <option value="3" >{FINNISH_MODE ? "hyvä" : "good"}</option>
            <option value="2" >{FINNISH_MODE ? "okei" : "ok"}</option>
            <option value="1"  >{FINNISH_MODE ? "huono" : "bad"}</option>
            <option hidden value="0" >Unrated</option>
          </select>

        </div>
        <div className='col' id="add-reject">
          <button class='button3' onClick={() => rejectQuestion(i)}>{FINNISH_MODE ? "Hylkää kysymys" : "Reject Question"}</button><br></br>
          {AddToDbButton}
        </div>
      </div>
      )
    }


    let block = []
    for (let i = 0; i < qaLocalPairs.length; i++) {
      let qblock = []
      for (let j = 0; j < qaLocalPairs[i].questions.length; j++) {
        qblock.push(qaLocalPairs[i].questions[j] + "\n")
      }

      let additionalAblock
      let AddToDbButton
      if ("A_Answer" in qaLocalPairs[i] && qaLocalPairs[i].flag) {
        qblock.push(<br></br>)
        qblock.push(<div className="azureanswer"> {qaLocalPairs[i]["A_questions"][0]}</div>)
        additionalAblock = <div className="azureanswer">{qaLocalPairs[i]["A_Answer"]}</div>
        AddToDbButton = <div><button class='button3' id={"a" + i.toString()} onClick={() => MergeDB(i)}>{FINNISH_MODE ? "Lisää alakysymykseksi" : "Add as subquestion"}</button><br></br><button class="button3" id={"b" + i.toString()} onClick={() => TakeDBquestion(i)}>{FINNISH_MODE ? "Mieluummin tietokantakysymys" : "Prefer database question"} </button></div>
      } else if (qaLocalPairs[i].flag) {
        AddToDbButton = <div><button class='button3' onClick={() => addToDB(i)}>{FINNISH_MODE ? "Lisää tietokantaan" : "Add to Database"}</button></div>
      }


      block.push(<div key={"local_pair_" + i.toString()} className="row">
        <div className='col'>
          {qblock}

        </div>
        <div className='col'>
          {qaLocalPairs[i].answer}<br></br>
          {additionalAblock}
        </div>
        <div className='col'>
          <select name="question" defaultValue={qaLocalPairs[i].rating} id={"local_question_" + i.toString()} onChange={e => updateLocalQuestionRating(i, e.target.value)} >
            <option value="3" >{FINNISH_MODE ? "hyvä" : "good"}</option>
            <option value="2" >{FINNISH_MODE ? "okei" : "ok"}Ok</option>
            <option value="1"  >{FINNISH_MODE ? "huono" : "bad"}</option>
            <option hidden value="0" >{FINNISH_MODE ? "luokittelematon" : "unrated"}</option>
          </select>

        </div>
        <div className='col' id='add-delete'>
          <button class='button3' onClick={() => deleteQuestion(i)}>{FINNISH_MODE? "Poista kysymys" : "Delete Question"}</button><br></br>
          {AddToDbButton}
        </div>
      </div>
      )
    }

    let block2 = []
    for (let i = 0; i < qaGlobalPairs.length; i++) {
      let qblock = []
      for (let j = 0; j < qaGlobalPairs[i].questions.length; j++) {
        qblock.push(qaGlobalPairs[i].questions[j] + "\n")
      }
      block2.push(<div key={"global_pair_" + i.toString()} className="row">
        <div className='col'>
          {qblock}
        </div>
        <div className='col'>
          {qaGlobalPairs[i].answer}
        </div>
        <div className='col'>
          <select name="question" defaultValue={qaGlobalPairs[i].rating} id={"global_question_" + i.toString()} onChange={e => updateQuestionRating(i, e.target.value)} >
            <option value="3" >{FINNISH_MODE ? "hyvä" : "good"}</option>
            <option value="2" >{FINNISH_MODE ? "okei" : "ok"}</option>
            <option value="1"  >{FINNISH_MODE ? "huono" : "bad"}</option>
            <option hidden value="0" >{FINNISH_MODE ? "luokittelematon" : "unrated"}</option>
          </select>

        </div>
        <div className='col'>
          <button class='button3' onClick={() => AddToCurrent(i)}>{FINNISH_MODE? "Lisää kysymys" : "Add Question"}</button>
        </div>
      </div>
      )
    }
    return (
      <div>
        <header>
          <div id='nav'>
            <a class='button3' href='/'>{FINNISH_MODE ? "Takaisin" : "Back"}</a>
          </div>
          <h2 id='title'>{FINNISH_MODE ? "Opettajan kojelauta" : "Teacher Dashboard"}</h2>
          <div></div>
        </header>
        <section class='teacher-dash'>
          <div class='card'>
            <a href="TeacherPage/AddQuestion">{FINNISH_MODE ? "Lisää kysymyksiä" : "Add Questions"}</a>
          </div>
          <div class='card' id='game-card'>
            {getGamestateText()}
            {getGamestateButton()}
          </div>
          <div class='card'>
            <a href="TeacherPage/AllocateStudents">{FINNISH_MODE ? "Kohdista opiskelijat tiimeihin" : "Allocate Students to Teams"}</a>
          </div>
          <div class='card'>
            <a href="TeacherPage/MassRegister">{FINNISH_MODE ? "Joukkorekisteriopiskelijat" : "Mass Register Students"}</a>
          </div>
        </section>
        <section class="q-table">
          <h3>{FINNISH_MODE ? "Tällä hetkellä valitut kysymykset" : "Currently Selected Questions"}</h3>
          <div className='row' id='row-head'>
            <div className='col'>
              <h5>{FINNISH_MODE ? "Kysymys" : "Question "}</h5>
            </div>
            <div className='col'>
              <h5>{FINNISH_MODE ? "Vastaus" : "Answer"}</h5>
            </div>
            <div className='col'>
              <h5>{FINNISH_MODE ? "Laatu" : "Quality"}</h5>
            </div>
            <div className='col'>
              <h5> </h5>
            </div>
          </div>
          {block0}
        </section>
        <section class="q-table">
          <h3>{FINNISH_MODE ? "Nykyiset opiskelijoiden luomat kysymykset" : "Current Questions Created By Students"}</h3>
          <div className='row' id='row-head'>
          <div className='col'>
              <h5>{FINNISH_MODE ? "Kysymys" : "Question "}</h5>
            </div>
            <div className='col'>
              <h5>{FINNISH_MODE ? "Vastaus" : "Answer"}</h5>
            </div>
            <div className='col'>
              <h5>{FINNISH_MODE ? "Laatu" : "Quality"}</h5>
            </div>
            <div className='col'>
              <h5> </h5>
            </div>
          </div>
          {block}
        </section>
        <section class="q-table">
          <h3>{FINNISH_MODE ? "Kaikki saatavilla olevat kysymykset" : "All Available Questions"}</h3>
          <div className='row' id='row-head'>
          <div className='col'>
              <h5>{FINNISH_MODE ? "Kysymys" : "Question "}</h5>
            </div>
            <div className='col'>
              <h5>{FINNISH_MODE ? "Vastaus" : "Answer"}</h5>
            </div>
            <div className='col'>
              <h5>{FINNISH_MODE ? "Laatu" : "Quality"}</h5>
            </div>
            <div className='col'>
              <h5> </h5>
            </div>
          </div>
          {block2}
        </section>
      </div>
    )
  }

  return (
    GeneratePage()
  )
}

export default TeacherDashboard