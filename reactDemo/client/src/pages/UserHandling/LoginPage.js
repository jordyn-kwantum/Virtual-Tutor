import React, { useState } from 'react'
import httpClient from '../../httpClient';
import "../main.css";
import { FINNISH_MODE } from '../..';

const LoginPage = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const logInUser = async () => {
        try{
            await httpClient.post("/api/login", {
                email,
                password
            });
            window.location.href = "/";
        } catch(error){
            if (error.response.status === 401){
                alert("Invalid Credentials")
            }
        }
    }

    return (
        <div>
            <header></header>
            <h2>{FINNISH_MODE? "Tilille kirjautuminen":"Account Login"}</h2>
            <div>
                <form>
                    <div class='field'>
                        <label for="email">Email</label>
                        <input type="text" name="email" value={email} onChange={(e) => setEmail(e.target.value)}/>
                    </div>
                    <div class='field'>
                        <label for="password">Password</label>
                        <input type="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                    </div>
                        <button type="button" class='button2' onClick={() => logInUser()}>Login</button>
                </form>
            </div>
            <footer></footer>
        </div>
    )
}

export default LoginPage