## Technical Documentation for the Flask demo

### What is the Demo
This demo is a proof of concept for the Helsinki project in which we are attempting to produce a chat bot or question and answering system that assists students in their learning in school. Furthermore is should give feedback to the teacher about real time information about how the students are performing an on what aspect they need further assistance.

### What is flask
This demo is built in flask. Flask is a relatively simple python based framework for the building websites. Static HTML pages are used as templates and python code run in the background, where it deals with user requests, populates the web pages with the relevant information, and makes calls to other processes and databases.

Flask is useful because it is fast to set up but it has limitations. It is not possible to work with dynamically updating websites, ie websites where changes are made on the machine of the user instead of on the server. It can also be clunky. It is effective as a prototyping tool or for static websites but should not be used for more complicated systems.


### How does the demo work
How to run the flask server is given in the readme.md. Here we give a technical overview of how this server works.

In the home.py file the majority of the computation occurs. The worksheet/text is generated from the SQUAD dataset and the conversation histories and other history is produced.

The home.py also produces a homepage (index.html) at localhost:5000 in your browser here you have access to two POC views. One for the students and one for the teachers.


#### Student view

For the students this will load localhost:5000/student/id where this id is the id of the student. Each id has its own conversation history with the model that is stored. In this way we can keep track of what individual students are discussion specifically.

On the student page we see the assignment or text that is given to the student. At the bottom of the document there is a textbox for asking questions to the chatbot. As student enters a question and hits enter or submit and the question is sent to the azure environment where the custom QA model is stored.

The querying is completed through a REST API call the code for which may be found in the python folder. This folder holds the scripts that are responsible for communication with the azure environment, such as for summarization, parsing, querying and so forth.

Once the API call returns with a question response the page is reloaded automatically with the answer to the question being given at the bottom of the page. The student is then presented with several options.

1. The student can ask another question. In this case the previous question is given as context for the new question, this tends to increase performance. The code for this may be seen in the Querry.py file
2. The student can confirm or deny that the answer to the question was helpful. if it was helpful, this feedback is sent to the azure environment using the addSuggestion() function in the tagging.py file. This updates the information in the QA database. As the students version of the question may have been slightly different than  the one stored in the database, this new successfully answered question may then be added as a potential alternative in the azure environment.

If the feedback is negative this information will be forwarded to the teacher, that then will be able to act on this information, potentially adding additional questions into the database so that in the future such questions can be answered.

3. If the question had any follow up questions, which may be defined by the teacher in the azure environment or in the demo environment a button is given that allows the student to ask the follow up question.

This is a post request to the same page that updates it with the renderQuestion method.


Regardless of what option is chosen the webpage is refreshed based on the impact of the students actions with new information. The webpages are created by means of templates. The templates may be found in the templates directory where they are stored as html files. When the render_template function is run in home.py with a webpage and several arguments as in render_template("student.html", id=id)
the students.html file is loaded. In all areas of the file {{}} may be used to access the parameters passed into the file. As such {{id}} would print the id passed into the rendering method.

In addition to this {%%} blocks may be used to run loops and conditionals in the html, that are populated at runtime by python. This allows us to pass in lists or dictionaries and access their values one at a time in the html, and give each their own treatment.

#### Teacher view

For the teacher view we aim to give the teachers maximal information of the students activities. In the teacher view we have 4 fields. First is a list of students by id. This allows for a more in depth look at that individual students activity including full conversation histories, and what answers they were unhappy with.

Secondarily there is a button to add an additional question to the azure data base, this provides a number of simple fields for adding in information about the question answer, source document and additional tags.

Thirdly there is a list of failed questions. These are the questions for which the QA system did not have an answer. Here this an easy button provided that allows the teacher to add a new answer to the database based on the failed question.

Finally there is a list of questions that were not answered effectively. Here the teacher has the option to update the question and answer pair in order to improve clarity for the students. All of the updating is done via code in the tagging.py file.
