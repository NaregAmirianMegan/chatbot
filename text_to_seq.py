from keras.preprocessing.text import text_to_word_sequence

def tokenize_text(text):
    return text_to_word_sequence(text, filters='#$&()*+,-/:;<=>@[\]^_`{|}~\n', lower=False, split=' ')

if __name__ == '__main__':
    with open("compiled_data/RC_2018-01.train.text", "r") as f:
        line = f.readline()
        while line:
            print(line)
            print(tokenize_text(line))
            line = f.readline()
