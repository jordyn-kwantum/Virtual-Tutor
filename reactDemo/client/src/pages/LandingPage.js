import React, { useState, useEffect } from 'react'
import { Link } from "react-router-dom"
import httpClient from '../httpClient';
import "./main.css";
import { FINNISH_MODE } from '..';

const LandingPage = () => {

  const [count, setCount] = useState(null);
  const [user, setUser] = useState(null);
  const [gamestate, setGameState] = useState(0)

  const tick = () => {
    setCount((prevState) => prevState < 20 ? prevState + 1 : 0);
  }

  useEffect(() => {
    const timer = setInterval(() => tick(), 1000);
    return () => clearInterval(timer);
  });

  useEffect(() => {
    if (count === 0) {
      (
        async () => {
          httpClient.get("/api/GetGameState").then(function (result) {
            let gState = parseInt(result.data["GameState"])
            setGameState(gState)
            // console.log(gState)
          }).catch(function (err) {
            console.log(err)
          })
        })();
    }
  }, [count]);

  useEffect(() => {
    (async () => {
      try {
        const resp = await httpClient.get("/api/@me");
        setUser(resp.data)
      } catch (e) {
        // console.log("Not authenticated")
      }
    })();
  }, [])

  const logoutUser = async () => {
    await httpClient.post("/api/logout")
    window.location.href = "/"
  }

  function loginSectionHTML() {
    if (user == null) return (<div id='nav'>
      <Link to="/Login" className='button3'>
        Login
      </Link>
      <Link to="/Register" className='button3'>
        Register
      </Link>
    </div>);
    // console.log(user)
    return (<div id='nav'>
      <button class='button3' onClick={logoutUser}>Logout</button>
      {FINNISH_MODE ? "Tervetuloa" : "Welcome"}, {user.email}!
    </div>);
  }

  function Team1SectionHTML() {
    if (user != null && (user.teacher || (user.team === 1 && (gamestate === 1 || gamestate === 3)))) return (
      <div>
        <Link to="/Team1Page" className='card'>
          {FINNISH_MODE ? "Joukkueen 1 sivu" : "Team 1 Page"}
          </Link>
      </div>)
  }


  function Team2SectionHTML() {
    if (user != null && (user.teacher || ((user.team === 2) && (gamestate >= 1 && gamestate <= 4)))) return (
      <div>
        <Link to="/Team2Page" className='card'>
        {FINNISH_MODE ? "Joukkueen 2 sivu" : "Team 2 Page"}
          </Link>
      </div>)
  }


  function TeacherSectionHTML() {
    // console.log(user)
    if (user != null && user.teacher) {
      return (
        <div>
          <Link to="/TeacherPage" className='card'>
          {FINNISH_MODE ? "Opettajan kojelauta" : "Teacher Dashboard"}
            </Link>
        </div>)
    }
  }

  function ScoresHTML() {
    if (user != null && (user.teacher || gamestate === 5)) {
      return (
        <div>
          <Link to="/Scores" className='card'>
          {FINNISH_MODE ? "Tulokset" : "Scores"}
            </Link>
        </div>
      )
    }
  }

  function FinalHTML() {
    return (
      <div>
        <header>
          {loginSectionHTML()}
        </header>
        <section>
          <h1>{FINNISH_MODE ? "Opitaan":"Let's Learn!"}</h1>
          <div class='landing'>
            {Team1SectionHTML()}
            {Team2SectionHTML()}
            {ScoresHTML()}
            {TeacherSectionHTML()}
          </div>
        </section>
      </div>);

  }

  return FinalHTML()

};

export default LandingPage 