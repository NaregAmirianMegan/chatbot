# output database.test.text, database.test.reply, database.train.text, database.train.reply
import sqlite3

def compile_data(test_size, train_size, database):
    assert train_size > test_size, "train_size must be larger than test_size"

    test_text = open("sample-data/{}.test.text".format(database), "a")
    test_reply = open("sample-data/{}.test.reply".format(database), "a")
    train_text = open("sample-data/{}.train.text".format(database), "a")
    train_reply = open("sample-data/{}.train.reply".format(database), "a")

    connection = sqlite3.connect('{}.db'.format('data/'+database))
    c = connection.cursor()
    c.execute("""SELECT * FROM data LIMIT {};""".format(train_size))
    data = c.fetchall()

    for row in data:
        if test_size:
            test_text.write(row[0]+'\n')
            test_reply.write(row[1]+'\n')
            test_size -= 1
        else:
            train_text.write(row[0]+'\n')
            train_reply.write(row[1]+'\n')

if __name__ == '__main__':
    compile_data(100, 1000, 'RC_2018-01')
