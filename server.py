import socket
import threading
import time
from requests import get

print('My public IP address is: {}'.format(get('https://api.ipify.org').text))
print("Server is starting....")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 1169))
server.listen()

clients = []
nicknames = []
Scorecard = [0, 0, 0, 0.]
global clientno
clientno = 0


def send_oppenents():
    msg = f"Both the players have joined. \n • Your Opponent is : {nicknames[0]}"
    clients[0].send(f"Your Opponent is : {nicknames[1]}".encode('utf-8'))
    time.sleep(1)
    msg = f"Both the players have joined. \n • Your Opponent is : {nicknames[0]}"
    clients[1].send(msg.encode('utf-8'))

def emptyup():
    i = 1
    while i >= 0:
        clients.pop(i)
        nicknames.pop(i)
        i-=1
        print("Server status: Resseting")
        Scorecard[0] = 0
        Scorecard[1] = 0
        Scorecard[2] = 0
        print("Server status: Readying up")
        time.sleep(1)
        print("Server status: Ready")

def ComputeResults(choices):
    if choices[0] == choices[1]:
        Scorecard[2] += 1
        return 2
    elif choices[0] == "R":
        if choices[1] == "P":
            Scorecard[1] += 1
            return 1
        else:
            Scorecard[0] += 1
            return 0
    elif choices[0] == "P":
        if choices[1] == "S":
            Scorecard[1] += 1
            return 1
        else:
            Scorecard[0] += 1
            return 0
    elif choices[0] == "S":
        if choices[1] == "R":
            Scorecard[1] += 1
            return 1
        else:
            Scorecard[0] += 1
            return 0


def SendResults(userwon):
    try:
        choice = []
        i = 0
        if userwon != 2:
            for client in clients:
                if i == userwon:
                    client.send(f"Congrats {nicknames[i]}!! You have won. Current score board is: ".encode('utf-8'))
                    client.send(
                        f"Won:{Scorecard[i]}, Drawn:{Scorecard[2]} and Lost:{abs((Scorecard[0] + Scorecard[1])-Scorecard[i])}".encode(
                            'utf-8'))
                else:
                    client.send(f"Sorry {nicknames[i]}!! You have lost. Current score board is: ".encode('utf-8'))
                    client.send(f"Won:{Scorecard[i]}, Drawn:{Scorecard[2]} and Lost:{abs((Scorecard[0] + Scorecard[1])-Scorecard[i])}".encode('utf-8'))
                i += 1
        else:
            for client in clients:
                client.send(f"Sorry {nicknames[i]}!! Both of you have drawn.\n Current score board is: ".encode('utf-8'))
                client.send(
                    f"Won:{Scorecard[i]}, Drawn:{Scorecard[2]} and Lost:{abs((Scorecard[0] + Scorecard[1])-Scorecard[i])}".encode('utf-8'))
                i += 1
        time.sleep(1)
        i = 0
        f = open("Datasstats", "a")
        f.write(f"{nicknames[0]}:{Scorecard[0]} {nicknames[1]}:{Scorecard[1]} Drawn:{Scorecard[2]}\n")
        f.write(f"{nicknames[0]}:{choices[0]} {nicknames[1]}:{choices[1]} {userwon}\n")
        f.close()
        for client in clients:
            print(f"Sending the choice to {nicknames[i]}")
            client.send("Do you want to play again ? (Y for yes and N for No):".encode('utf-8'))
            msg = client.recv(1024).decode('utf-8')
            choice.append(msg)
            print(f"Received the reply choice from {nicknames[i]}")
            i += 1
            if msg == "N":
                if i > 1:
                    clients[i - 2].send("1".encode('utf-8'))
                clients[i].send("1".encode('utf-8'))
                client.close()
                i = 1
                while i >= 0:
                    clients.pop(i)
                    nicknames.pop(i)
                    i-=1
                print("Server status: idle")
                Scorecard[0] = 0
                Scorecard[1] = 0
                Scorecard[2] = 0

            print(len(clients))

        for client in clients:
            client.send("Both of you have decided to play another round! Game staring in 1s".encode('utf-8'))
        Mainganmelogic()
    except:
        print("Server status: Resseting")
        Scorecard[0] = 0
        Scorecard[1] = 0
        Scorecard[2] = 0
        print("Server status: Readying up")
        time.sleep(1)
        print("Server status: Ready")
        emptyup()
        Mainganmelogic()



def MainGamelogic():
    try:
        global choices
        choices = []
        x = True
        i = 0
        for client in clients:
            if i == 0:
                time.sleep(0.5)
                clients[i + 1].send("Waiting for the other player to enter their choice".encode('utf-8'))
            client.send("Please enter your choice (R for Rock,P for Paper and S for Scissors)".encode('utf-8'))
            choices.append(client.recv(1024).decode())
            print(f"Received the choice from {nicknames[i]}")
            i+=1
            if i == 1:
                clients[0].send("Waiting for the other player to enter their choice".encode('utf-8'))
        s = ComputeResults(choices)
        SendResults(s)
    except:
        print("Server status: Resseting")
        Scorecard[0] = 0
        Scorecard[1] = 0
        Scorecard[2] = 0
        print("Server status: Readying up")
        time.sleep(1)
        print("Server status: Ready")
        emptyup()
        Mainganmelogic()

def getaconnection():
    global client, address
    client, address = server.accept()
    print(f"Connected with {str(address)}")
    client.send("Please give us your nick name ".encode('utf-8'))
    nickname = client.recv(1024).decode('utf-8')
    nicknames.append(nickname)
    clients.append(client)
    print(f"Nickname of the client is {nickname}")
    client.send(str((len(clients)-1)).encode('utf-8'))
    client.send("Connected to the server!".encode('utf-8'))
    time.sleep(1)
    client.send("Please wait till another player joins".encode('utf-8'))
    print("Server status: waiting for another player to join")
def Mainganmelogic():
    while True:
        if len(clients) != 2:
            while len(clients) != 2:
                getaconnection()
        send_oppenents()
        MainGamelogic()
        print("Round Over")
        print("Server status: idle")



print("Server has started")
Mainganmelogic()

