import socket
import sys
from playsound import playsound
 


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '127.0.0.1'
PORT = 42069

s.connect((HOST, PORT))

#Initial response
response="WAIT"

"""Client loop. Always either waiting for further instructions and not taking user input
or taking user input and returning server response exits game when win/lose or draw message received"""
while True:

    while "WAIT" in response: # wait for other player to finish their turn
        response = str(s.recv(4096).decode("utf-8"))
        print(response)

    #if "win" in response or "lost" in response or "Draw" in response:
     #   sys.exit()

    #Take user input from command line interface
    userInput = input(">>> ")
    if(userInput == ''):
        continue

    #Send user input to server, and collect response
    s.send(userInput.encode("utf-8"))
    response = s.recv(4096).decode("utf-8")

    print(response)

    if "win" in response:
        playsound("C:/Users/johnw/OneDrive/Desktop/tictactoe/win.mp3")

    if "lost" in response:
       playsound("C:/Users/johnw/OneDrive/Desktop/tictactoe/lose.mp3")

	#quit program if user chooses to exit
    if "Goodbye" in response:
    	sys.exit()

s.close()