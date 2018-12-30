import sqlite3

def filter(database):
    connection = sqlite3.connect('{}.db'.format('data/'+database))
    c = connection.cursor()
    c.execute(""" CREATE TABLE pairs AS SELECT body, reply FROM data WHERE reply_score IS NOT NULL; """)
    c.execute(""" DROP TABLE data """)
    c.execute(""" CREATE TABLE data AS SELECT * FROM pairs WHERE body NOT LIKE '%http%' AND reply NOT LIKE '%http%'; """)
    c.execute(""" DROP TABLE pairs; """)
    c.execute(""" VACUUM; """)

if __name__ == '__main__':
    files = ['RC_2015-05', 'RC_2016-01', 'RC_2017-01', 'RC_2017-02', 'RC_2017-12', 'RC_2018-01', 'RC_2018-02']
    for file in files:
        filter(file)
