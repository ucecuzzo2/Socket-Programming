# Multi-Client Chat Application with Python

This Python program is a multi-client chat application built with Python 3.11. It establishes a TCP connection using sockets to enable real-time, text-based communication in a shared chatroom. Clients can connect, exchange messages, and even share files with one another within the chatroom. This README provides an overview of the program, its features, and instructions for usage.

## Usage Instructions

1. **Running the Program**:
   - Before proceeding with any other steps, ensure you have Python 3.11 or later installed on your system and run it on a preferred IDE.

2. **Server Setup**:
   - Run the server script via Terminal (typically named `chatserver.py`) on a machine with a static IP address. The server will listen for incoming client connections.

3. **Client Setup**:
   - Run the client script via Terminal (typically named `chatclient.py`) on the machines from which you want to connect. The clients should provide the server's IP address to connect to the chatroom.

4. **Join the Chatroom**:
   - Clients can specify a username when connecting. Once connected, they can send and receive messages within the chatroom.

5. **Text Messaging**:
   - Type messages in the client console and hit Enter to send them. Messages will be displayed in real-time for all connected clients.

6. **File Sharing**:
   - Clients can use a specific command or feature to send files to other users. Ensure that files are located in the appropriate directories on the sender and receiver's machines.

7. **Disconnect and Exit**:
   - To disconnect from the chatroom, clients can use an exit command or close the client script.


---

Thank you for using this Multi-Client Chat Application. We hope it provides an interactive and collaborative platform for communication and file sharing. If you have any questions or need assistance, please refer to the documentation or contact the project maintainers.
