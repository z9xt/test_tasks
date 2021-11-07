#!/usr/bin/env python3

import cgi
from hashlib import md5
import sqlite3 as sq3


def print_header(title):
    
    #writes title and header of page
    print("""Content-type: text/html

          <html>
          <head>
          <title>%s</title>
          </head>
          <body>""" % title)

def user_exist(cur, user):

    if cur.execute('SELECT * FROM USERS WHERE name = (?)' , (user,) ).fetchall() != [] :
        
        return True
    else:
        return False

conn = sq3.connect('users.db')

with conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS USERS (name TEXT, md5 TEXT);
    """)
cur = conn.cursor()
sql = 'INSERT INTO USERS (name, md5) values(?, ?)'


print_header("New user registration")



print("""<b>Enter ID for registration:</b>
    <p>(If you use ID before you can't use it again)</p>
    <p>(You ID can contains only letters and numbers)</p>
    <form method = "post" method = "index.py">
    <p>
      <input type = "text" name = "id">
      <input type = "submit">
    </p>
    </form>""")

form = cgi.FieldStorage()

if "id" in form:    
    result= str.encode(form["id"].value)
    if result.isalnum():
        if user_exist(cur, result):
            print('<font color="red"><p>Error: ID %s is already registred</p></font>' 
                % result.decode('utf-8'))
        else:
            hsh=md5(result)
            print("<p>ID <em>%s</em> was registred</p>""" % result.decode('utf-8'))
            print("""<p>Please copy and keep this hash for next authorization: <em>%s</em></p>
                """ % hsh.hexdigest())
            print("""<p>Now you can save message to log with you pair ID and hash
                on the second part of server <a href="http://127.0.0.1:8001">here</a></p>""")
            cur.execute(sql, (result, hsh.hexdigest().encode() ))
            conn.commit()

    else:
        print('<font color="red"><p>Error: ID can contain only letters and numbers</p></font>')
    
print("</body></html>\n")
