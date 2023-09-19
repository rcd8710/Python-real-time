import socket
import threading

HOST = '127.0.0.1'
PORT = 4768
ListenerLim = 4
active_clients = []

def listen_message(client,username ):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message !=  "":
            message_sending = username + ": " + message
            send_all_message(message_sending)
        else:
            print("The message send from the client is empty'")


def send_message_client(client,message_sending):
    client.sendall(message_sending.encode())

def send_all_message(message_sending):
    for user in active_clients:
        send_message_client(user[1],message_sending)

def client_handler(client):
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != "":
            active_clients.append((username,client))
            join_message = "SERVER:" + F"{username} added to the chat"
            send_all_message(join_message)
            break
        else:
            print('Client username is empty')
    threading.Thread(target= listen_message,args =(client,username,)).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST}:{PORT}")
    except Exception as e:
        print(f'Error binding to host {HOST} and port {PORT}: {e}')
        return  # Exit the program if binding fails

    server.listen(ListenerLim)

    while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]}:{address[1]}")

        threading.Thread(target=client_handler, args=(client,)).start()

if __name__ == '__main__':
    main()
