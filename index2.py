#!/usr/bin/env python3

import cgi
from hashlib import md5
import sqlite3 as sq3
import logging

def print_header(title):
    
    #writes title and header of page
    print("""Content-type: text/html

            <html>
            <head>
            <title>%s</title>
            </head>
            <body>""" % title)

def take_record(cur, user):
    
    record = cur.execute('SELECT * FROM USERS WHERE name = (?)' , (user,) ).fetchall()
    if record != [] :
        return record
    else:
        return False

def main():
    
    #logging setups
    logger = logging.getLogger('task3')
    logger.setLevel('INFO')
    
    task3_format = logging.Formatter(fmt='{asctime}-{levelname}-{message}', 
    style ='{', datefmt='%Y-%m-%d %H:%M:%S')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(task3_format)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler('log_usrs_msgs.txt', mode='a')
    file_handler.setFormatter(task3_format)
    logger.addHandler(file_handler)
    #end of logging setups
    
    conn = sq3.connect('users.db')
    
    with conn:
        conn.execute('CREATE TABLE IF NOT EXISTS USERS (name TEXT, md5 TEXT)')
    cur = conn.cursor()
    
    print_header("Send message to log")
    
    print("""<b>Welcome to the second part of the server :</b>
             <p>Here you can send message to log</p>
             <p>if you have correct pair of ID and hash.</p>
             <p>If you haven\'t, you can take it 
                <a href="http://127.0.0.1:8000">here</a> </p>
             <form method = "post" method = "use_forms.py">
                <p><br>
                Input your ID here:
                <input type = "text" name = "id">
                <br><br>
                Input your hash for checking:
                <input type = "text" name = "hash" size="32">
                <br><br>
                Input your message for logging:<br>
                <textarea
                    type = "text"
                    name = "message"
                    cols="80"
                    rows="25"></textarea>
                <input type = "submit">
                </p>
             </form>""")
    
    form = cgi.FieldStorage(keep_blank_values=True)
    
    raw_iid = form.getvalue("id")
    raw_hhash = form.getvalue("hash")
    message = form.getvalue("message")
    
    if "id" in form and "hash" in form:
        iid = raw_iid.encode()
        hhash = raw_hhash.encode()

        if iid.isalnum() and hhash.isalnum():
            pair=take_record (cur, iid)
    
            if pair:
                #print('<p>{}<p>'.format(pair))
                if pair == [(iid, hhash)]:
                    logger.info('User: "{}" Send message: "{}"'.format(raw_iid, message))
                    print('<p>Message saved to the log: {}</p>'.format(message) )
                else:
                    print('<font color="red"><p>Inputed pair is not relevanted</p></font>')
            else:
                print('<font color="red"><p>user not in database</p></font>')
        else:
            print('<font color="red"><p><b>Error: Input unacceptable value -')
            print(' only letters and nubers can be used and form ')
            print('can\'t be empty</b></p></font>')
        
    print("</body></html>\n")
    
    
if __name__=='__main__':
    main()
