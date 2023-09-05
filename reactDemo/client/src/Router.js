import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LandingPage from './pages/LandingPage';
import Team1Page from './pages/Team1/Team1Page';
import { NotFound } from './pages/NotFound';
import TeacherDashboard from './pages/TeacherPages/TeacherDashboard';
import TeacherAddQuestions from './pages/TeacherPages/TeacherAddQuestions';
import LoginPage from './pages/UserHandling/LoginPage';
import RegisterPage from './pages/UserHandling/RegisterPage';
import TeacherAllocateStudents from './pages/TeacherPages/TeacherAllocateStudents';
import Team2Page from './pages/Team2/Team2Page';
import ScoresPage from './pages/scores/ScoresPage';
import TeacherMassRegister from './pages/TeacherPages/MassRegister';
import Team1GroupPage from './pages/Team1/Team1GroupPage.js';

const Router = () => {
  return (
    <BrowserRouter uter>
      <Routes>
        <Route exact path="/" element={<LandingPage />} />
        <Route exact path="/Team1Page" element={<Team1Page />} />
        <Route exact path="/Team1Page/Group" element={<Team1GroupPage />} />
        <Route exact path="/login" element={<LoginPage />} />
        <Route exact path="/register" element={<RegisterPage />} />
        <Route exact path="/Team2Page" element={<Team2Page />} />
        <Route exact path="/TeacherPage" element={<TeacherDashboard />} />
        <Route exact path="/TeacherPage/AddQuestion" element={<TeacherAddQuestions />} />
        <Route exact path="/TeacherPage/AllocateStudents" element={<TeacherAllocateStudents />} />
        <Route exact path="/TeacherPage/MassRegister" element={<TeacherMassRegister />} />
        <Route exact path="/Scores" element={<ScoresPage />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter >
  )
}

export default Router