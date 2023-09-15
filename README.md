# Helsinki Virtual Tutor Project 2022

This website is currently hosted at https://virtualtutor.azurewebsites.net/. Navigate here to begin gameplay.

## Project Description

The goal of the game is to engage students in the process of creating and playing a reading-based game. The game is supervised by a teacher, but the main aspects of the game are automated through AI, specifically a Large Language Model in the form of a Question-Answer system. The AI model will answer any question posed during the team 2’s turn of the game, but it can only provide answer’s from a fixed knowledge base (question and answer pairs created by the teacher or team 1).

## Gameplay Instructions

**Teacher:**
1. Navigate to the website and register as a Teacher.
2. Select the Teacher dashboard.
3. Wait for your students' Team Captains to be determined and for them to register.

*Optionally, these accounts can be predetermined and registered. Just have the students chosen sign in to the predetermined accounts and ensure they are on the correct teams.*

4. Navigate to the Allocate Teams space from the Teacher dashboard and ensure the Team Captains match their assigned teams in the application.
5. Head back to the Teacher Dashboard and click Start Game.
6. Instruct Team 1 to begin the reading and determining of question and answer pairs. Once they click Submit, the game can continue.
7. Click End Round 1 in the Teacher Dashboard, then review the questions submitted. You can either send them back to Team 1 for revision, or approve by clicking Send to Team 2.
8. Wait for Team 2 to read the article and guess the questions that belong to each answer sent from Team 1. 
9. After Team 2 has submitted their guesses, click End Game.
10. On the main page, click Score to reveal the final game results. It's encouraged to have a class discussion about the article and the question and answer writing process.

**Team 1:**

1. Assign a Team Captain to sign in to the game.
2. Once the game starts, click the Team 1 button and read the article thoroughly.
3. Decide as a team on 2-3 question and answer pairs and enter them into the prompt.
4. As a team, select your favorite 5 questions from the ones shown. Try to challenge your opposing team, and be sure your questions are correct and fair, or else the Teacher will reject them.
5. Submit your final questions and wait for the Teacher to review the questions and send them on to Team 2.

**Team 2:**

1. Assign a Team Captain to sign in to the game.
2. Once Team 1 has submitted their questions, and they have been reviewed by the Teacher, click the Team 2 button.
3. Read the article provided and discuss within your group. Try to identify key ideas and facts that may be asked about by Team 1.
4. See the answers to the questions written by Team 1. Your goal is to write the correct question for each answer. Discuss as a team, because you can only submit once!
5. Wait to see how you scored.

## Technical Overview

### Flask - Backend

Flask is a Python framework that holds all the logic required to control functionality within the application. This holds the database, the article text files, and all keys needed to connect the application to Azure. In the codebase, all Flask components are held within the “server” folder.

### React - Frontend

React is a JavaScript framework that defines all pages of the web application as well as their respective HTML and CSS elements. This describes the blueprint of the entire application, while functionality is controlled by the Flask backend. The React portion also controls all HTTP calls between the browser and the application. In the codebase, all React components are held within the “client” folder.

### Docker - Container

Docker is used to create an “image” of the application for easy uploading to an app service host. The Docker image is created in a terminal within the codebase and then uploaded to the App Service in Azure.

### Microsoft Azure

**App Service:**

An App Service resource in Azure holds all information required to host the application. Here, we control when the application starts and stops running, and can see statistics like traffic and memory usage.

**Container Registry:**

The Container Registry resource contains the Docker image that holds the web application. This is connected to the App Service resource where it is then hosted on its domain.

**Cognitive Services:**

The Azure AI Cognitive Services resource holds the knowledge base containing all question and answer pairs. This is connected directly to the codebase.

