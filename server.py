import socket
from game import Game
from player import Player
import time
from _thread import *
import threading

LOCK = threading.Lock()

HOST = '127.0.0.1'
PORT = 42069
available_players = []
players = []

def connect_client(client_socket):
    """connects players and arranges games"""
    bars = "====================================================================================================" 
    welcome_msg = bars + "\n" + "Welcome to Johns Tic-Tac-Toe! Type login [username] to create a username, then play to start a game!" + "\n" + bars + "\n"+ "type 'help' for a list of commands"
    client_socket.send(welcome_msg.encode("utf-8"))
    global players
    player = None
    while True:
        cmd = client_socket.recv(4096)
        cmd = cmd.decode("utf-8")
        request = cmd.split(" ")

        if request[0] == 'login' and request[1]:    # create username for user
            username = request[1]
            
            for p in players:
                if p.username == username:
                    username += "1" 

            LOCK.acquire()
            # Create player with this threads client socket and given username
            player = Player(username, client_socket)
            players.append(player)
            LOCK.release()
            client_socket.send(f"Welcome: {player.username}".encode("utf-8"))
        
        elif request[0] == 'play' and player is not None: # find a player and create a game, ignore if the player has not logged in yet
                player.send("WAIT, searching for a game...")
                LOCK.acquire()
                player.setAvailable()
                available_players.append(player)
                LOCK.release()
                opponent = None

                if len(available_players) % 2 == 1: # if there is no available match to be made for a client, wait for match
                    while player.state == 'a':
                        continue
                    while player.state == 'b': # another player will make a game with waiting player, loop will break in other thread when game ends
                        continue

                elif opponent is None: # search for player who is available 
                    for op in players:
                        if op.state == "a" and op.state != "b" and op.username != player.username:
                            opponent = op

                    if opponent is None: # if no available games, wait until a new client connects
                        time.sleep(1)

                    else:
                        # when opponenet is found start game with player and opponent
                        print("Game made")
                        LOCK.acquire()
                        game = Game(opponent, player) # make a game object
                        print(f"Game started with {opponent.username} and {player.username}")
                        opponent.setBusy()
                        player.setBusy()
                        LOCK.release()
                        
                        # play game
                        play(game)
                        
                        LOCK.acquire()
                        available_players.remove(player)
                        player.setLoggedIn()
                        opponent.setLoggedIn()
                        available_players.remove(opponent)
                        LOCK.release()

        elif request[0] == 'play' and player is None:
            client_socket.send("Please login before searching for a game.".encode("utf-8"))

        elif request[0] == "players":
            players_string = ""
            for player in players:
                players_string += player.username + "\n"
            client_socket.send(players_string.encode("utf-8"))

        elif request[0] == 'exit':
            client_socket.send("Goodbye!".encode("utf-8"))
            LOCK.acquire()
            players.remove(player)
            LOCK.release()
            client_socket.close()
            break

        elif request[0] == 'help':
            commands = "'play': search for a game." + "\n" + "'players': display list of current players." + "\n" + "'exit': disconnect from the server and close the client."
            client_socket.send(commands.encode("utf-8"))
        else:
            client_socket.send("That is not a command".encode("utf-8"))


def play(game):
    """runs the game"""
    game_over = False
   # game.turn.conn.recv(4096).decode("utf-8")
   # game.waiting.conn.recv(4096).decode("utf-8")
    while game_over == False:
        game.turn.send(game.display_board() + "Your move, enter a number 0 through 8 to make a move:" + "\n")
        game.waiting.send(game.display_board() + "WAIT The other player is taking their turn." + "\n")
        move = game.turn.conn.recv(4096).decode("utf-8")
        valid = game.valid_move(move)

        while valid == False: # if incorrect input, prompt until it is correct
            game.turn.send(game.display_board() + "Invalid move, enter a number 0 through 8 to make a move." + "\n")
            move = game.turn.conn.recv(4096).decode("utf-8")
            valid = game.valid_move(move)

        if valid:             # update board if it is a valid move
            game.make_move(int(move))
            game_response = game.checkWinDraw() # check if that was a game ending/winning move

            if game_response == "301 NEXT":
                game.changeTurn()

            elif game_response == "300 WIN":
                game.turn.send(game.display_board() + "You win! Type play to search for another game, or exit to disconnect")
                game.waiting.send(game.display_board() + "You lost! Type play to search for another game, or exit to disconnect")
                game_over = True

            elif game_response == "300 DRAW" :
                game.turn.send(game.display_board() + "Draw! Type play to search for another game, or exit to disconnect")
                game.waiting.send(game.display_board() + "Draw! Type play to search for another game, or exit to disconnect")
                game_over = True


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print("socket binded to port", PORT)

# put the socket into listening mode
s.listen(5)
print("socket is listening")
while True:
    client_socket, addr = s.accept()
    print('Connected to a client')
    #start_new_thread(connect_client, (clientSock,))
    start_new_thread(connect_client, (client_socket,))
s.close()


