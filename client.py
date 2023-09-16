import random
import socket

import pyfiglet
from rich import print

result = pyfiglet.figlet_format("Welcome To Multiplayer Rock Paper Scissors", font = "digital")
print(result)
print(f"[bold white]Made by Prithwish Mukherjee[/bold white] \n [bold yellow]Github: https://github.com/Hackermanprith [/bold yellow]")
print()
print("[bold yellow]Enter host IP! address: [/bold yellow]")
host = input(" --> ")
print("[bold Green]Enter port number: [/bold Green]")
port = int(input(" -->"))
connect = False
client_socket = socket.socket()
client_socket.connect((host, port))
play = True
name = ""
clientno = 0
colour= ["red","green","yellow","blue","magenta","purple","cyan"]
usr_id = ""
odt_status = 0
def namesetter():
    global name
    data = client_socket.recv(1024).decode('utf-8')
    print(f"[bold magenta]{data}[/bold magenta]")
    msg = input(" --> ")
    name = msg
    client_socket.send(msg.encode('utf-8'))
    usr_id = client_socket.recv(1024).decode('utf-8')


def get_opnames():
    data = client_socket.recv(1024).decode('utf-8')
    print(f"[bold red]{data}[/bold red]")

def playagain():
        msg = input(" --> ").upper()
        msg = msg[0]
        msg = msg.encode('utf-8')
        client_socket.send(msg)
        if msg.decode('utf-8') == "Y":
            odt_status = client_socket.recv(1024).decode('utf-8')
            if odt_status == "1":
                    print(
                        "[bold green]Sorry ! But the other player has quit the game.For playing again please restart[/bold green]")
                    print("[bold green]Thank you for playing the game.[/bold green]")
                    print(
                        "[bold yellow]If you want to support me please donate here:[bold yellow][bold cyan] https://www.buymeacoffee.com/mukherjeepv [/bold cyan]")
                    client_socket.close()
            else:
                data = client_socket.recv(1024).decode('utf-8')
                while data is None:
                    randomcolour = random.randint(1, 6)
                    style = f"[bold {colour[randomcolour]}]"
                    if data is not None:
                        print(f"• {style}{data}{style}")
                        break
                maingamelogicrecival()
        else:
            print("[bold green]Thank you for playing the game.[/bold green]")
            print("[bold yellow]If you want to support me please donate here:[bold yellow][bold cyan] https://www.buymeacoffee.com/mukherjeepv [/bold cyan]")
            client_socket.close()


def maingamelogicrecival():
    odt_status = 0
    message = client_socket.recv(1024).decode()
    randomcolour = random.randint(1, 6)
    style = f"[bold {colour[randomcolour]}]"
    print(f"• {style}{message}{style}")
    while message != "Please enter your choice (R for Rock,P for Paper and S for Scissors)":
        message = client_socket.recv(1024).decode()
        if not message:
            continue
        if message == "Please enter your choice (R for Rock,P for Paper and S for Scissors)":
            randomcolour = random.randint(1, 6)
            print(f"[bold magenta]{name}[/bold magenta], [bold green]{message}[/bold green]")
            break
        randomcolour = random.randint(1, 6)
        style = f"[bold {colour[randomcolour]}]"
        print(f"• {style}{message}{style}")

    val = input(" --> ").upper()
    val = val[0]
    if val != "R" and val != "P" and val != "S" :
        print(f"[bold red]• Please enter a valid choice in the form of R (Rock) ,P(Paper) or S(Scissors) [/bold red]")
        val = input(" --> ").upper()
        val = val[0]
        if val != "R" and val != "P" and val != "S":
            print(
            f"[bold red]• Please enter a valid choice in the form of R (Rock) ,P(Paper) or S(Scissors) [/bold red]")
            val = input(" --> ").upper()
        client_socket.send(val.encode('utf-8'))
    else:
        client_socket.send(val.encode('utf-8'))
    data = None
    trig = 0
    while data is None:
        data = client_socket.recv(1024).decode()
        if data is not None:
            print(f"• {style}{data}{style}")
            break

    while trig <= 3 or data != "Do you want to play again ? (Y for yes and N for No):":
        data = client_socket.recv(1024).decode()
        if data is None:
            trig += 1
            continue
        if data == "Do you want to play again ? (Y for yes and N for No):":
            print(f"• [bold cyan]{data}[/bold cyan]")
            break
        if data == "1":
            odt_status = 1
            print("[bold green]Sorry ! But the other player has quit the game.For playing again please restart[/bold green]")
            print("[bold green]Thank you for playing the game.[/bold green]")
            print("[bold yellow]If you want to support me please donate here:[bold yellow][bold cyan] https://www.buymeacoffee.com/mukherjeepv [/bold cyan]")
            client_socket.close()
            break
        trig += 1
        style = f"[bold {colour[randomcolour]}]"
        print(f"• {style}{data}{style}")
    if odt_status != 1:
         playagain()


if __name__ == '__main__':
    try:
        namesetter()
        get_opnames()
        play = maingamelogicrecival()
        client_socket.close()
    except KeyboardInterrupt:
        print('Interrupted')
        SystemExit(0)
