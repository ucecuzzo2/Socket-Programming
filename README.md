Certainly, here's the updated README with the requested change:

```markdown
# Multi-Client Chat Application with Python

This Python program is a multi-client chat application built with Python 3.11. It establishes a TCP connection using sockets to enable real-time, text-based communication in a shared chatroom. Clients can connect, exchange messages, and even share files with one another within the chatroom. This README provides an overview of the program, its features, and instructions for usage.

## Usage Instructions

1. **Running the Program**:
   - Before proceeding with any other steps, ensure you have Python 3.11 or later installed on your system.

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

## Note

- Ensure that your network configuration allows incoming and outgoing connections on the specified port (default is often 8080).

- Use this application responsibly and consider privacy and ethical concerns when sharing files and messages.

- Security considerations are essential. It's recommended to use secure connections and authentication mechanisms if deploying this application in a real-world environment.

---

Thank you for using this Multi-Client Chat Application! We hope it provides an interactive and collaborative platform for communication and file sharing. If you have any questions or need assistance, please refer to the documentation or contact the project maintainers.
```

This update places the "Running the Program" step at the top of the usage instructions.
