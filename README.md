# react-chatbot
A chatbot trained on reddit data with a dynamic bidirectional recurrent neural network. Front end is written in ReactJS.

## Sample Conversation


## Data
Data is kept in SQL databases and then filed into the training and testing files. </br>
Data Source: http://files.pushshift.io/reddit/comments/ </br>

### Data Format
BODY : REPLY = PAIR </br>
TOTAL COMPILED PAIRS: 62,247,075 : 12.3 GB

### Data Filtration
- Filter out null rows </br>
- Filter out rows with urls

## Model (Dynamic Bidirectional RNN)
- dynamic : handle input sequences of drastically different lengths as opposed to padding or bucketing </br>
- bidirectional : handle sentence contexts (LSTM can't remember whole phrase, so it is fed both forwards and backwards timesteps) </br>

## Credits
https://github.com/daniel-kukiela/nmt-chatbot to train generate and train the model. </br>
https://github.com/Sentdex for inspiring this project and helping locate and manipulate data.
