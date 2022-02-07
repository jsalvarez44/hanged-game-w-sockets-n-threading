import socket
import threading
import sys

username = input("Enter your username: ")
password = input("Enter your password: ")

host = '192.168.1.9'
port = 30000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


def recieve_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message == "@username":
                client.send(username.encode('utf-8'))
            elif message == "@exit":
                client.close()
                sys.exit()
            elif message == "\nIts your turn! Guess a letter:":
                print(message)
                send_message = input('')
                client.send(send_message.encode('utf-8'))
            else:
                print(message)
        except:
            client.close()
            sys.exit()


recieve_thread = threading.Thread(target=recieve_messages)
recieve_thread.start()
