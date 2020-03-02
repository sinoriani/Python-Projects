from flask import Flask, render_template,session , redirect , url_for  , request
from flask_socketio import SocketIO, emit , join_room , leave_room
from flask_session import Session


app = Flask(__name__)
rooms = {}
games = {}


app.config[ 'SECRET_KEY' ] = 'jsbcfsbfjefebw237u3gdbdc'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
socketio = SocketIO( app , manage_session = False )

#Partie is the Game object
from .gamelogic import Partie

sessions = {}

@app.route( '/' )
@app.route('/home')
def home():
  return render_template( './index.html' )

def messageRecived():
  print( 'message was received!!!' )

def find_client_room_name(uid):
  for r in rooms.keys():
    if uid in rooms[r].values():
      return r
  
  return None

@socketio.on('join')
def on_join(data):

    #client information
    clientId = data['clientId']
    room = find_client_room_name(clientId)  
    username = sessions[clientId] 

    print(username + ' has entered the room.')

    join_room(room)
    #emit a response to the room that the client joined
    data['message'] = 'has joined the room!'
    emit('my response',data , room = room )

    if rooms[room]['nbOfPlayers'] == 2:
      #begin game
      user1 = rooms[room]["player1"]
      user2 = rooms[room]["player2"]
      rooms[room]['game'] = Partie() 
      print(rooms,sessions,sep='\n')
      #method in the Partie(Game) object that launches the game
      rooms[room]['game'].jouer(sessions[user1],sessions[user2])

      emit('start game' , {'n1' : user1 , 'n2': user2 } , room = room )
      print('sending start game' , {'n1' : user1 , 'n2': user2 })


@socketio.on('redirect to game page')
def on_game_page(data):
    username = data['user_name']
    room = data['room_name']
    clientId = data['clientId']
    sessions[clientId] = username

    if room in rooms:
      if rooms[room]['nbOfPlayers'] >= 2:
        #room is full
        print('room is full!')
        emit('room full')
        return
      else:
        #add one to the room's number of connected clients
        rooms[room]['nbOfPlayers'] += 1
    else:
      rooms[room] = {}
      #set to one the new room's number of connected clients
      rooms[room]['nbOfPlayers'] = 1
    
    playerNumber = rooms[room]['nbOfPlayers']
    rooms[room]["player{}".format(playerNumber)] = clientId

    
    emit('redirect', {'url': url_for('game',id = game) })

@app.route('/game/<id>')
def game(id):
  #print(rooms, session)
  if( id in sessions):
    user = sessions[id]
    return render_template('./game.html',content = user , room = find_client_room_name(id))
  else:
    return redirect(url_for("home"))
    

@socketio.on('my event')
def handle_message(data):
  data['user_name'] = sessions[ data['userid']]
  if not 'message' in data:
    data['message'] = 'Has joined le room!'
  
  print('sending response to room : ',  find_client_room_name( data['userid'] ) )
  emit( 'my response', data, callback=messageRecived, room = find_client_room_name( data['userid'] )   )

@socketio.on("logout")
def logout_handler(data):
  id = data['userid']
  if(id in sessions):
    print( 'user: ' , sessions[id] , ' disconnected')
    
    data['user_name'] = sessions[ id ]
    data['message'] = 'Has left the room!'
    room_name = find_client_room_name(id)
    emit( 'my response', data, callback=messageRecived , room =  room_name  )
    
    leave_room(room_name)
    rooms[room_name]['nbOfPlayers'] -= 1

    #find the key storing the id of the player who is leaving the room and delete it 
    for key,value in rooms[room_name].items():    
      if value == id:
        del rooms[room_name][key]
        break
    print('logout-handler : deleted user from room! ', rooms[room_name])

    if rooms[room_name]['nbOfPlayers'] == 1: 
      onPlayerLeaveGame(room_name)
    elif( rooms[room_name]['nbOfPlayers'] <= 0):
      del rooms[room_name]

    del sessions[id]
    print('logout_handler : deleted user! ' , sessions )


def onPlayerLeaveGame(room_name):
  if 'player1' in rooms[room_name]:
    winnerId = rooms[room_name]["player1"]
  elif "player2" in rooms[room_name]:
    winnerId = rooms[room_name]["player2"]
    rooms[room_name]['player1'] = rooms[room_name]["player2"]
    del rooms[room_name]["player2"]
  else:
    print("ERROR! room doesn't have correct number of players! - onPlayerLeaveGame")
  winnerName = sessions[winnerId]
    
  rooms[room_name]['game'] = None
  print("onPlayerLeaveGame : rooms :", rooms)
  #JS will set the this remaining player who wins to player1 ( myNumber variable in js)
  emit('client_left_game', {'winnerName':winnerName} , room = room_name)

  
@socketio.on('restart_ready')
def set_player_ready(data):
  _id = data['clientId']
  room = find_client_room_name(_id)
  playerNumber = data['playerNumber']
  game = rooms[room]['game']

  game.joueurs[playerNumber-1].set_pret(True)

  if(game.joueurs[0].pret == True and game.joueurs[1].pret == True):
    game.recommencer()
    emit('start game',{},room = room)



def startGame(user1,user2,gameId):
  games[gameId] = Partie()
  games[gameId].jouer(user1,user2)


@socketio.on('client position assign')
def assign_position(data):
  position = [ data['pos'][0] , data['pos'][1]]
  _id = data['userid']
  room = find_client_room_name(_id)
  game = rooms[room]['game']
  resultat , gagnant = game.tour(position)
  if resultat['etat'] == 'gagnant':
    data['winnerName'] = gagnant
    #joueurs means players
    #set_pret sets the ready value of the player
    game.joueurs[0].set_pret(False)
    game.joueurs[1].set_pret(False)
  elif resultat['etat'] == 'nul':
    game.joueurs[0].set_pret(False)
    game.joueurs[1].set_pret(False)


  emit('position assigned response',{'winnerName' : gagnant, 'pos': position , 'etat':resultat['etat'] ,'currentPlayer' : game.joueur_courant.numero}, room = room)

if __name__ == '__main__':
  socketio.run( app, host='0.0.0.0' ,debug = True )

   