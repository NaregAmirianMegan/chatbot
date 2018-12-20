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
    def get_competing_reply_score(pid):
        # get score for where parent_id = pid otherwise return false
        c.execute("""SELECT score FROM data WHERE parent_id = "{0}";""".format(pid))
        result = c.fetchone()
        if result:
            return result[0]
        return False

    def get_child_id(id):
        # get id for where pid == id
        sql = """SELECT id FROM data WHERE parent_id = "{0}";""".format(id)
        print(sql)
        c.execute(sql)
        result = c.fetchone()
        if result:
            return result[0]
        return False

    connection = sqlite3.connect('{}.db'.format(file_name))
    c = connection.cursor()
    c.execute(""" CREATE TABLE IF NOT EXISTS data(parent_id TEXT, id TEXT, parent_body TEXT, body TEXT, score INT); """)
    sql_insertions = []

    # compile and execute SQL statements
    with open("{}".format(file_name), buffering=1000) as file:
        row_count = 0
        code_pairs = 0
        for row in file:
            data = json.loads(row)

            parent_id = data['parent_id'][3:]
            id = data['id']
            body = data['body']
            score = data['score']

            is_child = False
            is_parent = False

            if score >= 2:
                if audit(body):
                    row_count += 1
                    body = format_body(body)
                    competing_reply_score = get_competing_reply_score(parent_id)
                    if competing_reply_score:
                        is_child = True
                        # replacing existing child
                        if score > competing_reply_score:
                            # replace id body and score
                            sql = """UPDATE data SET id = "{0}", body = "{1}", score = {2} WHERE parent_id = "{3}";""".format(id, body, score, parent_id)
                            #print(sql)
                            sql_insertions.append(sql)
                    # inserting parent of child
                    child_id = get_child_id(id)
                    if child_id:
                        is_parent = True
                        code_pairs += 1
                        # insert body in parent body
                        sql = """UPDATE data SET parent_body = "{0}" WHERE id = "{1}";""".format(body, child_id)
                        #print(sql)
                        sql_insertions.append(sql)
                    # inserting new row because it's a new thread
                    if not (is_child and is_parent):
                        # insert new row pid, id, body, score
                        sql = """INSERT INTO data(parent_id, id, body, score) VALUES("{0}", "{1}", "{2}", {3});""".format(parent_id, id, body, score)
                        sql_insertions.append(sql)

            # execute SQL statements and reset transaction list
            if row_count % 10 == 0:
                c.execute(""" BEGIN TRANSACTION """)
                for insert in sql_insertions:
                    c.execute(insert)
                connection.commit()
                sql_insertions = []

if __name__ == '__main__':
    file = sys.argv[1]
    create_database('data/'+file)
