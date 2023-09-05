import React, { useState } from 'react'
import httpClient from '../../httpClient';
import "../main.css";
import { FINNISH_MODE } from '../..';

const RegisterPage = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [is_teacher, setIs_teacher] = useState(false);

    const registerUser = async () => {    
        try{
            await httpClient.post("/api/register", {
                email,
                password,
                is_teacher
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
            <h2>{FINNISH_MODE ? "Luo tili" : "Create Account"}</h2>
            <div>
                <form>
                    <div class='field'>
                        <label>Email</label>
                        <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
                    </div>
                    <div class='field'>
                        <label>Password</label>
                        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                    </div>
                    <label>{FINNISH_MODE ? "Opettaja?": "Make Teacher?"}</label>
                    <div>
                        <input type="checkbox" value={is_teacher} onChange={(e) => setIs_teacher(e.target.checked)}></input>
                    </div>
                    <button type="button" class='button2' onClick={() => registerUser() }>Register</button>
                </form>
            </div>
            <footer></footer>
        </div>
    )
}

export default RegisterPage