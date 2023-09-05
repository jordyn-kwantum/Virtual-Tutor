import React, { useState} from 'react'
import httpClient from '../../httpClient';
import { FINNISH_MODE } from '../..'

const TeacherMassRegister = () => {
    const [studentString, setStudentString] = useState("")


    function massRegisterStudent(){
        let data = []
        let studentArr = studentString.trim().split("\n")
        for(let i=0; i<studentArr.length; ++i){
            let student = studentArr[i]
            let s = student.split(":")
            data.push({
                "name":s[0],
                "email":s[1],
                "password":s[2]
            })
        }
        console.log(data)

        httpClient.post("/api/massRegister", {
            "Students":data
        }).then(()=> {
            window.location.href = "/TeacherPage";
        }).catch(e => {
            console.log(e);
        })
    }

    function GeneratePage() {
        return <div><h1>{FINNISH_MODE ? "Joukkorekisteriopiskelija tästä": "Mass Register Student Here"}</h1>
            <p><b>{FINNISH_MODE ? "Kirjoita opiskelijat vain muodossa nimi:sähköposti:salasana uusilla riveillä erotettuina" : "Please only enter students in the format name:email:password seperated by new lines"}</b> </p>
            <form><textarea class="wide area" id="emailinput" placeholder='name1:email1:password1' defaultValue="" cols="150" rows="5" onChange={
                (e) => {setStudentString(e.target.value)}
            }/><br></br>
            <button type="button" onClick={() =>
            {massRegisterStudent();}
            }>{FINNISH_MODE ? "Lähetä": "Submit"}</button>
            </form>
            
        </div>
    }

    return (
        GeneratePage()
    )
}



export default TeacherMassRegister