import os
import uuid
from flask import Flask, session, render_template, request
from flask.ext.socketio import SocketIO,emit
import psycopg2
import psycopg2.extras

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

messages = [{'text':'test', 'name':'testName'}]
searchMsg = [{'text':'test', 'name':'testName'}]
rooms = ["Movies", "Sports", "TV Shows"]
users = {}
global currentRoom 
global subList 

def connectToDB():
  connectionString = 'dbname=mydata user=postgres password=Phoenix host=localhost'
  try:
    return psycopg2.connect(connectionString)
  except:
    print("Can't connect to database")

def updateRoster():
    names = []
    for user_id in  users:
        print users[user_id]['username']
        if len(users[user_id]['username'])==0:
           names.append('Anonymous')
        else:
            names.append(users[user_id]['username'])
    print 'broadcasting names'
    emit('roster', names, broadcast=True)
    
def updateRooms():
    emit('rooms', rooms)    

@socketio.on('connect', namespace='/chat')
def test_connect():
    global currentRoom
    currentRoom = "Movies"
    global subList
    subList = ''
    session['uuid']=uuid.uuid1()
    session['username']='starter name'
    print 'connected'
    
    users[session['uuid']]={'username':'New User'}
    if session['uuid'] in users:
        del users[session['uuid']]

    updateRoster()
    updateRooms()

    del messages[:]
    for message in messages:
        emit('message', message)
        
@socketio.on('moveRoom', namespace='/chat')
def move_Room(chatRoom):
    cRoom = chatRoom
    global currentRoom
    if subList.find(cRoom) >= 1: 
        if cRoom != currentRoom:
            currentRoom = cRoom
            emit('clear')
            conn = connectToDB()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            try:
                if currentRoom == "Movies":
                    query = "SELECT message, username FROM movies"
                elif currentRoom == "Sports":
                    query = "SELECT message, username FROM sports"
                elif currentRoom == "TV Shows":
                    query = "SELECT message, username FROM tvshows"
                
                cur.execute(query)
                rows = cur.fetchall()
                conn.commit()
                cur.close()
                conn.close()
                
                del messages[:]
                for row in rows:
                     str = '***'
                     row = str.join(row)
                     t = row.partition("***")
                     tmp = {'text':t[0], 'name':t[2]}
                     messages.append(tmp)
                     
                     
                for message in messages:
                    emit('message', message)
            
            
            except:
                print("ERROR SELECTING MESSAGES")
        
    else:
        
        emit('setDefault', currentRoom)
        emit('clear')
        conn = connectToDB()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            if currentRoom == "Movies":
                query = "SELECT message, username FROM movies"
            elif currentRoom == "Sports":
                query = "SELECT message, username FROM sports"
            elif currentRoom == "TV Shows":
                query = "SELECT message, username FROM tvshows"
            
            cur.execute(query)
            rows = cur.fetchall()
            conn.commit()
            cur.close()
            conn.close()
            
            del messages[:]
            for row in rows:
                 str = '***'
                 row = str.join(row)
                 t = row.partition("***")
                 tmp = {'text':t[0], 'name':t[2]}
                 messages.append(tmp)
                 
                 
            for message in messages:
                emit('message', message)

        except:
            print("ERROR SELECTING MESSAGES")

@socketio.on('message', namespace='/chat')
def new_message(message):
    
        conn = connectToDB()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        try:
            tmp = {'text':message, 'name':users[session['uuid']]['username']}
            
            if currentRoom == "Movies":
                query = "INSERT INTO movies VALUES (%s, %s) "
            elif currentRoom == "Sports":
                query = "INSERT INTO sports VALUES (%s, %s) "  
            elif currentRoom == "TV Shows":
                query = "INSERT INTO tvshows VALUES (%s, %s) " 
            cur.execute(query, (message, users[session['uuid']]['username']))
            conn.commit()
            cur.close()
            conn.close()
            messages.append(tmp)
            emit('message', tmp, broadcast=True)
        except:
            print("INSERT MESSAGE FAIL")

@socketio.on('search', namespace='/chat')
def new_search(search):
    if search!='':
        conn = connectToDB()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
        
            search = '%'+search+'%'
            
            if subList.find("Movies") >= 1 and subList.find("Sports") < 1 and subList.find("TV Shows") < 1: 
                query = "SELECT message, username FROM movies WHERE message LIKE '%s' " % (search)
            elif subList.find("Movies") >= 1 and subList.find("Sports") >= 1 and subList.find("TV Shows") < 1: 
                query = "SELECT message, username FROM sports WHERE message LIKE '%s' UNION SELECT message, username FROM movies WHERE message LIKE '%s' " % (search, search)  
            elif subList.find("Movies") >= 1 and subList.find("Sports") >= 1 and subList.find("TV Shows") >= 1: 
                query = "SELECT message, username FROM sports WHERE message LIKE '%s' UNION SELECT message, username FROM movies WHERE message LIKE '%s' UNION SELECT message, username FROM tvshows WHERE message LIKE '%s'" % (search, search, search)
        
            cur.execute(query)
            rows = cur.fetchall()
            conn.commit()
            cur.close()
            conn.close()
            
            del searchMsg[:]
            for row in rows:
                 str = '***'
                 row = str.join(row)
                 t = row.partition("***")
                 tmp = {'text':t[0], 'name':t[2]}
                 searchMsg.append(tmp)
                 
            for message in searchMsg:
                emit('search', message)
        
        except:
            print("SEARCH MESSAGE FAIL")
         
@socketio.on('identify', namespace='/chat')
def on_identify(message):
    print 'identify' + message
    users[session['uuid']]={'username':message}
    updateRoster()
    
    
@socketio.on('login', namespace='/chat')
def on_login(pw):
    
    updateRoster()
    
#    if pw or users[session['uuid']]['username'] == "":
        
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT * FROM users WHERE username LIKE '%s' AND password LIKE '%s' " % (users[session['uuid']]['username'], pw)
    cur.execute(query)
    results = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    
    if results == []:
        emit('login')
        
    elif results!=[]:
        emit('run')
        conn = connectToDB()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            query = "SELECT moviessection, sportssection, tvshowssection FROM users WHERE username LIKE '%s' " % (users[session['uuid']]['username']) 
            cur.execute(query)
            result = cur.fetchall()
            rooms = []
            for resul in result:
                str = ','
                resul = str.join(resul)
                rooms.append(resul)
            
            tank = ['True,False,False']
            ryan = ['True,True,False']
            peter = ['True,True,True']

            global subList
            subList = ''
            if rooms == tank:
                subList = " Movies"
            elif rooms == ryan:
                subList = " Movies, Sports"
            elif rooms ==peter:
                subList = " Movies, Sports, TV Shows"
            
            conn.commit()
            cur.close()
            conn.close()
           
        except:
            print("ERROR SELECTING SUBS")
        
        conn = connectToDB()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
           
            query = "SELECT message, username FROM movies"
            
            cur.execute(query)
            rows = cur.fetchall()
            conn.commit()
            cur.close()
            conn.close()
            
            del messages[:]
            for row in rows:
                 str = '***'
                 row = str.join(row)
                 t = row.partition("***")
                 tmp = {'text':t[0], 'name':t[2]}
                 messages.append(tmp)
                 
            for message in messages:
                emit('message', message)
        
        except:
            print("ERROR SELECTING MESSAGES")

@socketio.on('disconnect', namespace='/chat')
def on_disconnect():
    print 'disconnect'
    if session['uuid'] in users:
        del users[session['uuid']]
        updateRoster()

@app.route('/')
def hello_world():
    print 'in hello world'
    return app.send_static_file('index.html')
    return 'Hello World!'

@app.route('/js/<path:path>')
def static_proxy_js(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('js', path))
    
@app.route('/css/<path:path>')
def static_proxy_css(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('css', path))
    
@app.route('/img/<path:path>')
def static_proxy_img(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('img', path))
    
if __name__ == '__main__':
    print "A"

    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
     
