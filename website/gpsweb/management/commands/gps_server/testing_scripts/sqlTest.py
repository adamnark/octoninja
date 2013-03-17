def first():
    import MySQLdb                                    #1
    connection=MySQLdb.connect(host="127.0.0.1", user="amir", passwd="amir", db="test")  #2
    cur=connection.cursor()                           #3
    cur.execute("select * from customer")                  #6
    multiplerow=cur.fetchall()     
    #    print "Displaying All the Rows:  ", multiplerow
    for row in multiplerow:
        print row




# another way to do this, with each row as a dictionary:
def another():
    import MySQLdb
    import MySQLdb.cursors

    conn = MySQLdb.Connect(
        host='127.0.0.1', user='amir',
        passwd='amir', db='test',
        cursorclass=MySQLdb.cursors.DictCursor) # <- important
    cursor = conn.cursor()
    cursor.execute("SELECT name, telephone tel FROM customer")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    for row in rows:
        print 'name:' + row['name'], 'tel:' + row['tel'] # bingo!
        

another()