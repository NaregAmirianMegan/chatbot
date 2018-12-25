# react-practice
encoder_data = input text to bot.
decoder_data = response.

TOTAL COMPILED PAIRS: 62,247,075 : 12.3 GB


Model:
-dynamic bidirectional recurrent neural network
-dynamic : handle input sequences of drastically different lengths as opposed to padding or bucketing
-bidirectional : handle sentence contexts (LSTM can't remember whole phrase, so it is fed both forwards and backwards)
