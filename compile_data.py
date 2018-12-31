import sqlite3

def compile_data(test_size, train_size, database):
    assert train_size > test_size, "train_size must be larger than test_size"

    test_text = open("compiled_data_prime/test.text", "a")
    test_reply = open("compiled_data_prime/test.reply", "a")
    train_text = open("compiled_data_prime/train.text", "a")
    train_reply = open("compiled_data_prime/train.reply", "a")

    connection = sqlite3.connect('{}.db'.format('data/'+database))
    c = connection.cursor()
    c.execute("""SELECT * FROM data LIMIT {};""".format(train_size))
    data = c.fetchall()

    for row in data:
        text = row[0]
        reply = row[1]
        if not (text == None or reply == None):
            if test_size:
                test_text.write(text+"\n")
                test_reply.write(reply+"\n")
                test_size -= 1
            else:
                train_text.write(text+"\n")
                train_reply.write(reply+"\n")

def create_compilation(file_list, test_size, train_size):
    div = len(file_list)
    for file in file_list:
        compile_data(int(test_size/div), int(train_size/div), file)

if __name__ == '__main__':
    files = ['RC_2015-05', 'RC_2016-01', 'RC_2017-01', 'RC_2017-02', 'RC_2017-12', 'RC_2018-01', 'RC_2018-02']
    create_compilation(files, 1, 7000000)
