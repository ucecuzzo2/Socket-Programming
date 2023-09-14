from datetime import datetime
import socket
import json
from threading import Thread

# Create and Bind a TCP Server Socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#host_name = socket.gethostname()
host_name = "127.0.0.1"
s_ip = socket.gethostbyname(host_name)
port = 18024
serverSocket.bind((host_name, port))

# Outputs Bound Contents
print("Socket Bound")
print("Server IP: ", s_ip, " Server Port:", port)

# Listens for 10 Users
serverSocket.listen(10)

# Creates a set of clients
client_List = set()
client_address_List = []
chatroom_list = set()
chatroom_address_list = []
username_list = []
msgList = []
msg = ""


# Function to constantly listen for an client's incoming messages and sends them to the other clients
def clientWatch(cs, ca):
    adminFlag = 0
    while True:
        try:
            # Generate blank server message
            server_msg = {
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
                "USERNAME": "Server",
                "FILENAME": None,
                "PAYLOAD_LENGTH": 0,
                "PAYLOAD": None,
                "TIME": None
            }
            # Constantly listens for incoming message from a client

            msg = json.loads(cs.recv(1024).decode())

            if msg['REPORT_REQUEST_FLAG'] == 1:
                print("Processing REPORT_REQUEST")
                server_msg['REPORT_RESPONSE_FLAG'] = 1  # set flag to one
                # print(server_msg['USERNAME'])
                server_msg['PAYLOAD'] = "There are " + str(len(chatroom_list)) + " active users in the chatroom.\n"
                count = 0
                for x in chatroom_list:
                    server_msg['PAYLOAD'] = server_msg['PAYLOAD'] + username_list[count] + " at ip: " + str(
                        chatroom_address_list[count][0]) + " Port: " + str(chatroom_address_list[count][1]) + ".\n"
                    count += 1
                cs.send(json.dumps(server_msg).encode())
                continue

            if msg['JOIN_REQUEST_FLAG']:
                print("Processing JOIN_REQUEST")

                if len(chatroom_list) >= 3:
                    # Fill rejection
                    server_msg['JOIN_REJECT_FLAG'] = 1
                    server_msg[
                        'PAYLOAD'] = "The server rejects the join request. The chatroom has reached its maximum capacity."
                    cs.send(json.dumps(server_msg).encode())
                    continue

                # Check for duplicate usernames
                duplicates = 0
                for name in username_list:
                    if name == msg['USERNAME']:
                        duplicates = 1

                if duplicates:
                    # Fill rejection
                    server_msg['JOIN_REJECT_FLAG'] = 1
                    server_msg['PAYLOAD'] = "The server rejects the join request. Another user is using this username."
                    cs.send(json.dumps(server_msg).encode())
                    continue

                # Generate blank server message template to accept new user
                server_msg_accept_user = {
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
                    "USERNAME": "Server",
                    "FILENAME": None,
                    "PAYLOAD_LENGTH": 0,
                    "PAYLOAD": None,
                    "TIME": None
                }

                # Add user to chatroom
                chatroom_list.add(cs)
                chatroom_address_list.append(ca)

                server_msg_accept_user['JOIN_ACCEPT_FLAG'] = 1
                server_msg_accept_user['USERNAME'] = msg['USERNAME']
                msgHistory = "Welcome to the chatroom!\n Press 'q' to quit, or 'a' to add an attachment.\nChat History:"
                for message in msgList:
                    msgHistory = msgHistory + "\n[" + message['TIME'] + "] " + message['USERNAME'] + ": " + message[
                        'PAYLOAD']
                server_msg_accept_user['PAYLOAD'] = msgHistory
                username_list.append(msg['USERNAME'])

                cs.send(json.dumps(server_msg_accept_user).encode())

                server_msg['PAYLOAD'] = msg['USERNAME'] + " joined the chatroom."
                server_msg['TIME'] = datetime.now().strftime("%H:%M")
                server_msg['USERNAME'] = "Server"

                msgList.append(server_msg)
                for client_socket in chatroom_list:
                    client_socket.send(json.dumps(server_msg).encode())

                continue

            if msg['QUIT_REQUEST_FLAG']:
                print("Processing QUIT_REQUEST")
                if cs in chatroom_list:
                    server_msg['PAYLOAD'] = msg['USERNAME'][:-1] + " left the chatroom."
                    server_msg['TIME'] = msg['TIME']

                    msgList.append(server_msg)
                    for client_socket in chatroom_list:
                        client_socket.send(json.dumps(server_msg).encode())

                    chatroom_list.remove(cs)
                    chatroom_address_list.remove(ca)
                    username_list.remove(msg['USERNAME'][:-1])
                    continue
                else:
                    client_List.remove(cs)
                    client_address_List.remove(ca)
                    cs.close()
                    break

            if msg['ATTACHMENT_FLAG']:
                print("Processing FILE")

                fileName = msg['FILENAME']
                fileInc = open("downloads/" + fileName, "w")

                data = msg['PAYLOAD']
                fileInc.write(data)
                fileInc.close()

            print("Processing MESSAGE_SEND")
            msgList.append(msg)
            for client_socket in chatroom_list:
                client_socket.send(json.dumps(msg).encode())
        except Exception as e:
            print("Error\n")
            print(e)
            client_List.remove(cs)
            client_address_List.remove(ca)


while True:
    # Continues to listen / accept new clients
    client_socket, client_address = serverSocket.accept()

    print(client_address, "Connection Established!")
    # Adds the client's socket to the client set
    client_List.add((client_socket))
    client_address_List.append((client_address))

    # Create a thread that listens for each client's messages
    t = Thread(target=clientWatch, args=(client_socket, client_address))

    # Make a daemon so thread ends when main thread ends
    t.daemon = True

    t.start()

# Close out clients
for cs in client_List:
    cs.close()
# Close socket
s.close()