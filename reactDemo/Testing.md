# Testing the Game Experience

## AI Testing
We make use of two key pieces of Machine Learning for this project. Firstly we use the azure custom question and answering system, which makes use a natural language model. Secondarily, we make use of a natural langauge translation model and language detection model to translate from Finnish to English and Vice Versa.

### Custom Question and Answering Model
Things to Test:
1. If question has multiple subquestions all are returned from querying, which one should be considered.
    - *How to test*: Create questions with multiple subquestions, return these on purpose. See which one is selected by default. Consider changing.
2. Confidence score of the retured answer -> Gives a rough indication of how confident the model is in its prediction. 
    - NNs are usually overconfident in their predictions. Consider a the thresholding factor that maximnizes success.
    - *How to test*: Surver the confidence scores that the model produces for a large amount of questions 
        - Determine threshold from there.
        - Different threshold for different operations?
3. Questions that sound similar but have different answers. These need thorough testing. What can we do to seperate these values well. 
    - also when uploading questions, model checks if this question is already in the DB, if they sound similar but are different needs a method to compare.
    - Needs testing for accuracy.
    - *How to test*: Produce these similar questions and see how the model performs
4. Translation impact on model performance,
    - sentences might have odd or awkward language post translation from finnish.
    - Know that the model is relatively robust to misspellings, word order swaps, and synonyms.
    - *How to test*: Generate large collections of questions in dutch, espescially ones with awkward wording that might be difficult to translate.
5. Possible issues when returning multiple questions that match.
    - ie three questions are found in DB that roughly match new question, with confidence .6, .7, and .5. Which one do we pick? Maximization of confidence score? Present options to teacher.
        - Without information given to teacher might lead to confusion that model is not working
        - Give more information to users to increase model transparancy.
6. DB Growth. Time between adding new questions to deployed DB and everything being updated so that the system works.
    - *How to test*: Generate questions, upload and look at Azure dashboard.

### Language Detection
1. Incorrect Detection of Language
    - Mostly possible when the snippets of the text are too small, or if sentences are near identical in two different languages 
        - Finnish is pretty different than most languages. 
        - ? if detect language in article or respones, set static global variable? Translate from then on?

### Translation
1. Translation Errors 
    - Translation errors could be due to a few different reasons
        - The text was too short and is lacking context
        - The text is too long and is difficult to translate effectively, ie context is lost between senteces because section are translated individually
    - *Potential Solutions*: 
2. Incorrect and awkward translations that do not sound natural
    - *Potential Solution*: Store mutliple copies of the question and answer in different languages and relate between the two of them?
    - Store finnish language questions as sub question as as follow up question, then return these values when asking.

## Technical Testing
We make use of a flask `python` backend server and a `react` front end to create the game application.

### Server
**Testing of the Server Functionality**:
All of the server runs on Cross origin API calls. As such we need to test every one of the functions thoroughly for errors. We need unit testing.
- Use the package `unittest` to generate tests for the individual functions.
- Three types of functions in the code
    1. GET requests that return a jsonified object based on the local state
        - Test by generating a deterministic local state
        - Run the example GET requests using the requests module, or manually using postman.
        - compare output fields on the JSON to determined values
    2. POST requests that alter the internal state of programm.
        - Test by creating example POSTs by means of the requests module
        - Create functions that return the current internal state of the programs
        - compare that the state has changes after the request in the correct manner
    3. POST requests that alter the internal state and return values
        - violate the single responsibility principle
        - refactor into multiple functions that call each other
        - test the individual function seperately. 

### Client
Testing can be done through the interaction with the website directly. Things that should be examined
- How does the website look at different screen resolutions, phone, tablet, laptop, etc.
- How does the website work in different browsers -> IE, Opera, Safari, Chrome, Firefox 
    -> CSS and animations may need to be browser specific.
- Client is only HTTP not HTTPS when running local -> might be an issue.
    - We would need a certificate for this though.
    - possibily generate by heroku/azure at deployment time
    - Test if anything breaks under the encryption of HTTPS
- UI experience and user feedback. 
    - Demonstrate clearly when things are loading, and users need to wait or referesh the page