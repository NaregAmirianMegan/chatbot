import sqlite3, json, sys, datetime

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
    return body.replace('\n', '').replace('\r', '').replace('"', "'").strip()

def create_database(file_name):
    def get_parent_comment_id_and_reply_score(pid):
        c.execute("""SELECT id, reply_score FROM data WHERE id = "{}";""".format(pid))
        result = c.fetchone()
        if result:
            return result[0], result[1]
        return False, False

    connection = sqlite3.connect('{}.db'.format(file_name))
    c = connection.cursor()
    c.execute(""" CREATE TABLE IF NOT EXISTS data(id TEXT PRIMARY KEY, reply_id TEXT, body TEXT, reply TEXT, reply_score INT); """)
    sql_insertions = []

    # compile and execute SQL statements
    with open("{}".format(file_name), buffering=1000) as file:
        row_count = 0
        pairs = 0
        for row in file:
            row_count += 1

            data = json.loads(row)
            parent_id = data['parent_id'].split('_')[1]
            id = data['id']
            body = data['body']
            score = data['score']

            if score >= 2:
                if audit(body):
                    row_count += 1
                    body = format_body(body)
                    parent_comment_id, parent_reply_score = get_parent_comment_id_and_reply_score(parent_id)
                    if parent_comment_id:
                        if parent_reply_score:
                            if score > parent_reply_score:
                                #PERFORM UPDATE
                                sql_insertions.append("""UPDATE data SET reply_id = "{}", reply = "{}", reply_score = "{}" WHERE id = "{}";""".format(id, body, score, parent_comment_id))
                        else:
                            #PERFORM UPDATE
                            sql_insertions.append("""UPDATE data SET reply_id = "{}", reply = "{}", reply_score = "{}" WHERE id = "{}";""".format(id, body, score, parent_comment_id))
                            pairs += 1
                    #PERFORM INSERT
                    sql_insertions.append("""INSERT INTO data(id, body) VALUES("{}", "{}") """.format(id, body))


            # execute SQL statements and reset transaction list
            if row_count % 1000 == 0:
                c.execute(""" BEGIN TRANSACTION """)
                for insert in sql_insertions:
                    try:
                        c.execute(insert)
                    except Exception as e:
                        pass
                connection.commit()
                sql_insertions = []
            if row_count % 100000 == 0:
                print(str(datetime.datetime.now()), "row_count: ", row_count, "Pairs: ", pairs)

if __name__ == '__main__':
    file = sys.argv[1]
    create_database('data/'+file)
