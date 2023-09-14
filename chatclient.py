import os
import socket
import json
from threading import Thread
from datetime import datetime
from time import sleep
import pathlib

# Sets the preselected IP and port for the chat server
# Enter your machine's IP address for the host_name. Alternatively, you can enter "localhost"
host_name = "127.0.0.1"
port = 18024
global in_chatroom
in_chatroom = 0
name = "testName"  # initial name
FORMAT = "utf-8"

# Creates the TCP socket
new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting to", host_name, port, "...")
new_socket.connect((host_name, port))
print("Connected.")


# Thread to listen for messages from the server
def listen_for_messages():
    global in_chatroom
    while True:
        message_received = json.loads(new_socket.recv(1024).decode())
        if message_received['REPORT_RESPONSE_FLAG']:
            print("\n" + message_received['PAYLOAD'])
        elif message_received['JOIN_REJECT_FLAG']:
            print("\n" + message_received['PAYLOAD'])
            in_chatroom = 0

        elif message_received['JOIN_ACCEPT_FLAG']:
            print("\n" + message_received['PAYLOAD'])
            in_chatroom = 1
            continue
        elif message_received['QUIT_ACCEPT_FLAG']:
            in_chatroom = 0
        elif message_received['ATTACHMENT_FLAG']:

            fileName = message_received['FILENAME']
            fileInc = open("downloads/" + fileName, "w")

            data = message_received['PAYLOAD']
            fileInc.write(data)
            print("\n[" + message_received['TIME'] + "] " + message_received['USERNAME'] + ": " + data)
            fileInc.close()
        else:
            print("\n[" + message_received['TIME'] + "] " + message_received['USERNAME'] + ": " + message_received[
                'PAYLOAD'])


t = Thread(target=listen_for_messages)

t.daemon = True

t.start()

while True:
    # Generate blank message
    message_menu = {
        "REPORT_REQUEST_FLAG": 0,
        "REPORT_RESPONSE_FLAG": 0,
        "JOIN_REQUEST_FLAG": 0,
        "JOIN_REJECT_FLAG": 0,
        "JOIN_ACCEPT_FLAG": 0,
        "NEW_USER_FLAG": 0,
        "QUIT_REQUEST_FLAG": 0,
        "QUIT_ACCEPT_FLAG": 0,
        "ATTACHMENT_FLAG": 0,
        "NUMBER": 0,
        "USERNAME": None,
        "FILENAME": None,
        "PAYLOAD_LENGTH": 0,
        "PAYLOAD": None,
        "TIME": None
    }
    print("Please select one of the following options:\n",
          "1. Get a report of the chatroom from the server\n", "2. Request to join the chatroom.\n",
          "3. Quit the program.")
    menu_input = input("")

    if int(menu_input) == 1:
        print("Your choice:", menu_input)
        message_menu['REPORT_REQUEST_FLAG'] = 1  # set to one
        message_menu['PAYLOAD'] = host_name + "and port: " + str(port)
        new_socket.send(json.dumps(message_menu).encode())  # sends the report flag to server
        sleep(0.5)

    elif int(menu_input) == 2:
        print("Your choice:", menu_input)
        # Prompts the client for a username
        message_menu['JOIN_REQUEST_FLAG'] = 1
        name = input("Enter your a username: ")
        message_menu['USERNAME'] = name
        message_menu["TIME"] = datetime.now().strftime("%H:%M")
        new_socket.send(json.dumps(message_menu).encode())  # send the name
        sleep(0.5)
    elif int(menu_input) == 3:
        print("exit")
        message_menu['QUIT_REQUEST_FLAG'] = 1
        new_socket.send(json.dumps(message_menu).encode())
        new_socket.close()
        # sleep(0.5)
        break

    while in_chatroom:
        # Generate blank message
        message_sending = {
            "REPORT_REQUEST_FLAG": 0,
            "REPORT_RESPONSE_FLAG": 0,
            "JOIN_REQUEST_FLAG": 0,
            "JOIN_REJECT_FLAG": 0,
            "JOIN_ACCEPT_FLAG": 0,
            "NEW_USER_FLAG": 0,
            "QUIT_REQUEST_FLAG": 0,
            "QUIT_ACCEPT_FLAG": 0,
            "ATTACHMENT_FLAG": 0,
            "NUMBER": 0,
            "USERNAME": None,
            "FILENAME": None,
            "PAYLOAD_LENGTH": 0,
            "PAYLOAD": None,
            "TIME": None
        }
        # Adds Username and Time to message
        message_sending['USERNAME'] = name
        message_sending['TIME'] = datetime.now().strftime("%H:%M")

        # Recieves input from the user for a message
        message_text = input()

        # Allows the user to exit the chat room
        if message_text.lower() == "q":
            message_sending['QUIT_REQUEST_FLAG'] = 1
            message_sending['USERNAME'] = name + "X"
            new_socket.send(json.dumps(message_sending).encode())
            in_chatroom = 0
            sleep(0.5)
            break

        if message_text.lower() == 'a':
            file_info = input("Please enter the file path and name: ")
            f_open = open(file_info, "r")  # open the file
            data = f_open.read()
            message_sending['ATTACHMENT_FLAG'] = 1  # set flag to one
            message_sending['FILENAME'] = "coolfile1.txt"  # send file to server
            message_sending['PAYLOAD'] = data  # send file to server
            new_socket.send(json.dumps(message_sending).encode())
            continue

        # Adds payload to the message
        message_sending['PAYLOAD'] = message_text

        # Sends the message to the server
        new_socket.send(json.dumps(message_sending).encode())

# close the socket

new_socket.close()