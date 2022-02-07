import socket
import random
import time

host = '0.0.0.0'
port = 30000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()
print(f"Server running on {host}:{port}")
print()

clients = []
usernames = []
points = []
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x', 'y', 'z']
sayings = [
    "de tal palo, tal astilla",
    "al mal tiempo, buena cara",
    "no es oro todo lo que reluce",
    "a la tercera va la vencida",
    "mas vale prevenir que lamentar",
    "al que madruga, dios lo ayuda",
    "tira la piedra y esconde la mano",
    "el habito no hace al monje",
    "mas vale tarde que nunca",
    "cria fama y ponte a dormir",
    "dios aprieta pero no ahoga",
    "quien mucho abarca, poco aprieta",
    "preguntando se llega a roma",
    "una golondrina no hace verano",
    "mucho ruido y pocas nueces",
    "el que espera, desespera",
    "no hay mal que dure cien años"
]
roulette = [1, 2, 5, 10, 20, 50]
found_letters = []  # letters that the player found
guess_letters = []  # all letters that the player guess


def get_random_saying():
    return random.choice(sayings)


def check_saying(saying):
    parser = ""
    for letter in saying:
        if letter in letters:
            if letter in found_letters:
                parser += letter
            else:
                parser += '_'
        else:
            parser += letter

    print("Saying: ", parser)
    if parser == saying:
        return True
    else:
        return False


def count_letters(letter, saying):
    counter = 0

    for _letter in saying:
        if letter == _letter:
            counter += 1

    return counter


def check_leaderboard():
    for i in range(1, len(points)):
        for j in range(0, len(points)-i):
            if points[j+1] > points[j]:
                aux = points[j]
                points[j] = points[j+1]
                points[j+1] = aux

                aux = usernames[j]
                usernames[j] = usernames[j+1]
                usernames[j+1] = aux
                
                aux = clients[j]
                clients[j] = clients[j+1]
                clients[j+1] = aux

    for i in range(len(points)):
        print(f"{(i+1)}. {usernames[i]} - {points[i]} points!")
        clients[i].send(f"\nYou're the number {(i+1)}!".encode('utf-8'))
        clients[i].send("@exit".encode('utf-8'))


def play_game():
    n_clients = len(clients)
    flag = True
    saying = get_random_saying()
    i = 0

    while flag:
        if check_saying(saying):
            print("\nYOU WON!")
            flag = False  # break the infinite while

            check_leaderboard()
        else:
            clients[i].send("\nIts your turn! Guess a letter:".encode('utf-8'))
            while True:
                try:
                    letter = clients[i].recv(1024).decode('utf-8')
                    letter = letter.lower()

                    RS = random.choice(roulette)

                    print("\nRoulette: ", roulette)
                    time.sleep(2)
                    print("Random Selection: ", RS)

                    if letter not in guess_letters:
                        if letter in saying:
                            found_letters.append(letter)
                            n_letters = count_letters(letter, saying)

                            if n_letters > 1:
                                message = f"GOOD! You found {str(n_letters)} letters!"
                                clients[i].send(message.encode('utf-8'))
                            else:
                                clients[i].send("GOOD! You found a letter!".encode('utf-8'))
                            points[i] += RS * n_letters
                        else:
                            clients[i].send("BAD! Wrong letter!".encode('utf-8'))
                            points[i] -= RS

                        guess_letters.append(letter)

                        message = f"Points: {points[i]}".encode('utf-8')
                        clients[i].send(message)
                    else:
                        message = f"Letter '{letter}' has already been guessed, try another one!".encode('utf-8')
                        clients[i].send(message)
                    time.sleep(1)
                    break
                except:
                    index = clients.index(clients[i])
                    username = usernames[index]
                    broadcast(f"Server: {username} disconnected!".encode('utf-8'), clients[i])
                    clients.remove(clients[i])
                    usernames.remove(username)
                    clients[i].close()
                    flag = False
                    break
            i += 1

            if i == n_clients:
                i = 0


def countdown():
    print("\nREADY TO START?")
    time.sleep(2)
    print("3!")
    time.sleep(1)
    print("2!")
    time.sleep(1)
    print("1!")
    time.sleep(1)
    print("GO!")


def single_player():
    print()
    recieve_connections(1)  # only 1 client
    countdown()
    play_game()


def multiplayer():
    print("\nNUMBER OF PLAYERS")
    print("Press 1 for 2 PLAYERS")
    print("Press 2 for 3 PLAYERS")

    while True:
        players = input("Enter your option: ")
        if players in ["1", "2"]:
            break
        else:
            print("Enter a correct option!")

    n_players = int(players) + 1
    print()
    recieve_connections(n_players)  # multiclients
    countdown()
    play_game()


def game():
    print("GUESS THE SAYING!!")
    print("Press 1 for Singleplayer")
    print("Press 2 for Multiplayer")

    while True:
        option = input("Enter your option: ")
        if option == "1":
            single_player()
            break
        if option == "2":
            multiplayer()
            break
        else:
            print("Enter a correct option!")


def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)


def recieve_connections(players):
    if players > 1:
        print(f"Waiting for {players} players!")
    else:
        print(f"Waiting for {players} player!")

    while len(clients) < players:
        client, address = server.accept()

        client.send("@username".encode('utf-8'))
        username = client.recv(1024).decode('utf-8')

        clients.append(client)
        usernames.append(username)
        points.append(0)

        print(f"{username} is connected with {str(address)}")

        message = f"Server: {username} joined the game!".encode('utf-8')
        broadcast(message, client)
        client.send("Connected to the server!".encode('utf-8'))
        client.send("You have 0 points!".encode('utf-8'))


game()
