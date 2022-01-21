from datetime import datetime
import time
import mysql.connector

daatabase = mysql.connector.connect(
    host = "database",
    user = "user",
    password = "password",
    database = "pnvs_db"
)

#
def fetch_role(user_id):
    daatabase = mysql.connector.connect(
        host = "database",
        user = "user",
        password = "password",
        database = "pnvs_db"
    )
    # dbc is a database cursor
    dbc = daatabase.cursor(buffered=True)
    dbc.execute("""SELECT puborsub FROM roles where user_id = %d"""%(user_id))
    lst=[]
    for i in dbc:
        lst.append(i)
        print(lst)
    dbc.close()

def fetch_topicname(topic_id):
    daatabase = mysql.connector.connect(
        host = "database",
        user = "user",
        password = "password",
        database = "pnvs_db"
    )
    dbc = daatabase.cursor(buffered=True)
    dbc.execute("""SELECT topic_name FROM topic_info where id = %d"""%(topic_id))
    lst=[]
    for i in dbc:
        lst.append([i[0],i[1]])
        print(lst)
    dbc.close()

def fetchAllTopics():
    daatabase = mysql.connector.connect(
        host = "database",
        user = "user",
        password = "password",
        database = "pnvs_db"
    )
    dbc = daatabase.cursor(buffered=True)
    query = """Select id, topic_name from topic_info"""
    dbc.execute(query)
    lst = []
    for x in dbc:
        lst.append(x)
    dbc.close()
    return lst
    
#
def fetch_info(topic_id):
    daatabase = mysql.connector.connect(
        host = "database",
        user = "user",
        password = "password",
        database = "pnvs_db"
    )
    dbc = daatabase.cursor(buffered=True)
    dbc.execute("""SELECT info FROM info where topic_id = %d;"""%(topic_id))
    lst=[]
    for i in dbc:
        lst.append(i[0])
    dbc.close()
    return lst

def publish_info(topic_id,info):
    dbc = daatabase.cursor(buffered=True)
    dbc.execute('''insert into info(topic_id, info) VALUES(%d, "%s")'''%(topic_id, info))
    daatabase.commit()
    dbc.close()

def advertise_info(message):
    daatabase = mysql.connector.connect(
        host = "database",
        user = "user",
        password = "password",
        database = "pnvs_db"
    )
    dbc = daatabase.cursor(buffered=True)
    dbc.execute('''insert into info(topic_id, info) VALUES(0, "%s")'''%(message))
    daatabase.commit()
    dbc.close()

def publisher_topics(user_id):
    daatabase = mysql.connector.connect(
        host = "database",
        user = "user",
        password = "password",
        database = "pnvs_db"
    )
    dbc = daatabase.cursor(buffered=True)
    dbc.execute("""SELECT id FROM pub_topics where id = %d"""%(user_id))
    lst=[]
    for i in dbc:
        lst.append(i)
        print(lst)
    dbc.close()

# To fetch the list of topics that a particular user has subscribed to 
def subscribed_topics(user_id):
    daatabase = mysql.connector.connect(
        host = "database",
        user = "user",
        password = "password",
        database = "pnvs_db"
    )
    dbc = daatabase.cursor(buffered=True)
    dbc.execute("""SELECT topic_id FROM subscriber where user_id = %d and sub_info =1;"""%(user_id))
    lst=[]
    for i in dbc:
        lst.append(i[0])
    dbc.close()
    return lst

def unsubscribe(user_id,topic_id):
    daatabase = mysql.connector.connect(
        host = "database",
        user = "user",
        password = "password",
        database = "pnvs_db"
    )
    dbc = daatabase.cursor(buffered=True)
    dbc.execute("""UPDATE subscriber SET sub_info=0 where user_id = %d and topic_id =%d;"""%(user_id,topic_id))
    daatabase.commit()


def isempty(tableName, colName, value):
    daatabase = mysql.connector.connect(
        host = "database",
        user = "user",
        password = "password",
        database = "pnvs_db"
    )
    dbc = daatabase.cursor(buffered=True)
    query = '''SELECT * FROM %s WHERE %s=%d'''%(tableName, colName, value)
    dbc.execute(query)
    rows = dbc.fetchall()
    if len(rows):
        dbc.close()
        return False
    else:
        dbc.close()
        return True

def isempty_(tableName, colName, colName_, value, value_):
    daatabase = mysql.connector.connect(
        host = "database",
        user = "user",
        password = "password",
        database = "pnvs_db"
    )
    dbc = daatabase.cursor(buffered=True)
    query = '''SELECT * FROM %s WHERE %s=%d && %s=%d'''%(tableName, colName, value, colName_, value_)
    dbc.execute(query)
    rows = dbc.fetchall()
    if len(rows):
        dbc.close()
        return False
    else:
        dbc.close()
        return True

def subscribe(user_id,topic_id):
    daatabase = mysql.connector.connect(
        host = "database",
        user = "user",
        password = "password",
        database = "pnvs_db"
    )
    dbc = daatabase.cursor(buffered=True)

    if isempty_("subscriber", "user_id", "topic_id", user_id, topic_id):
        query = """INSERT into subscriber (user_id,topic_id,sub_info) VALUES(%d,%d,1);"""%(user_id, topic_id)
    else:
        query = """UPDATE subscriber SET sub_info=1 where user_id = %d and topic_id = %d;"""%(user_id, topic_id)
            
    dbc.execute(query)
    daatabase.commit()
    dbc.close()

    if isempty("roles", "userid", user_id):
        daatabase = mysql.connector.connect(
            host = "database",
            user = "user",
            password = "password",
            database = "pnvs_db"
        )
        dbc = daatabase.cursor(buffered=True)
        query = """INSERT into roles VALUES(%d,0)"""%(user_id)
        dbc.execute(query)
        daatabase.commit()
        dbc.close()
