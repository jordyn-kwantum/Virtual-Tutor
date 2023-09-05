import React, { useState, useEffect } from 'react'
import httpClient from '../../httpClient';
import '../main.css';
import { FINNISH_MODE } from '../..';

const TeacherAllocateStudents = () => {

    const [students, setStudents] = useState([])

    const updateStudentTeam = (i, value) =>{
        let data = {"student_id":students[i]["id"], "team":value}
        console.log(data)
        httpClient.post("/api/updateStudentTeam", {
            "student":data
        }).catch(err => {
            console.log(err)
        })
    }

    const updateIsTeacher = (i, value) => {
        let data = {"student_id":students[i]["id"], "teacher":value}
        console.log(data)
        httpClient.post("/api/updateIsTeacher", {
            "student":data
        }).catch(err => {
            console.log(err)
        })
    }

    useEffect(() => {
        (async () => {
            try {
                const resp = await httpClient.get("/api/GetStudents")
                setStudents(resp.data["data"])
            }
            catch (err) {
                console.log(err)
            }

        })();

    }, []);


    async function deleteStudent(email){
        let text = FINNISH_MODE ? "Oletko varma?" : "Are you sure?"
        let bool = window.confirm(text)
        if (bool){
            await httpClient.post("/api/deleteAccount", {
                "student_email":email
            }).catch(err => {
                console.log(err)
            })
            window.location.reload();
        }
        else {return}
    }

    function makeTable() {
        let block = []
        console.log(students)
        for (let i = 0; i < students.length; i++) {
            block.push(<div key={"student_" + i.toString()} className="row">
                <div className='col'>
                    {students[i]["id"]}
                </div>
                <div className='col'>
                    {students[i]["email"]}
                </div>
                <div className='col'> 
                    <select name="team" defaultValue={students[i]["team"]} id={"team_" + i.toString()} onChange = {e => updateStudentTeam(i, e.target.value)}>
                        <option value="1" >{FINNISH_MODE ? "Joukkue 1": "Team 1"}</option>
                        <option value="2" >{FINNISH_MODE ? "Joukkue 2": "Team 2"}</option>
                    </select>
                </div>
                <div className='col'> 
                    <select name="teacher" defaultValue={students[i]["teacher"]} id={"teacher_" + i.toString()} onChange = {e => updateIsTeacher(i, e.target.value)}>
                        <option value="1">{FINNISH_MODE ? "Opettaja": "Teacher"}</option>
                        <option value="2">{FINNISH_MODE ? "Opiskelija": "Student"}</option>
                    </select>
                </div>
                <div className='col'> 
                    <button name="deletebutton" class="button3" onClick={() => deleteStudent(students[i]["email"])}>Delete</button>
                </div>

            </div>
            )
        }

        return (block)
    }

    return (
        <div>
            <header>
                <div id='nav'>
                </div>
                <h2 id='title'>{FINNISH_MODE ? "": "Student Roster"}</h2>
            </header>
            <section class='q-table'>
            <div className='row' id='row-head'>
                <div className='col'>
                    <h5>{FINNISH_MODE ? "Opiskelijaluettelo": "Student ID"}</h5>
                </div>
                <div className='col'>
                    <h5>{FINNISH_MODE ? "Email": "Email"}</h5>
                </div>
                <div className='col'>
                    <h5>{FINNISH_MODE ? "Tiimi": "Team"}</h5>
                </div>
                <div className='col'>
                    <h5> </h5>
                </div>
                <div className='col'>
                    <h5>{FINNISH_MODE ? "Poista tili": "Delete account"}</h5>
                </div>
            </div>
            {makeTable()}
            </section>
        </div>
    )
}

export default TeacherAllocateStudents