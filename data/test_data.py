import sqlite3, json, sys

def audit(body):
    if not body:
        return False
    elif body == '[deleted]' or body == '[removed]':
        return False
    elif len(body.split(' ')) > 50 or len(body) > 1000:
        return False
    else:
        return True

def format_body(body):
    return body.replace('\n', '').replace('\r', '').replace('"', "'")

def create_database(file_name):
    connection = sqlite3.connect('{}.db'.format(file_name))
    c = connection.cursor()
    c.execute(""" CREATE TABLE IF NOT EXISTS data(parent_id TEXT, id TEXT); """)
    sql_insertions = []
    row_count = 0
    # compile and execute SQL statements
    with open("{}".format(file_name), buffering=1000) as file:
        for row in file:
            data = json.loads(row)

            print(data.keys())

            parent_id = data['parent_id'][3:]
            id = data['id']
            body = data['body']
            score = data['score']

            if score >= 2:
                if audit(body):
                    row_count += 1
                    sql_insertions.append("""INSERT INTO data VALUES("{}", "{}")""".format(parent_id, id))

            # execute SQL statements and reset transaction list
            if row_count % 10 == 0:
                c.execute(""" BEGIN TRANSACTION """)
                for insert in sql_insertions:
                    c.execute(insert)
                connection.commit()
                sql_insertions = []

if __name__ == '__main__':
    file = sys.argv[1]
    create_database(file)
