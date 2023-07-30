import socket
import threading
import tkinter as tk
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 5022

LISTENER_LIMIT = 5
active_clients = []
client_list = []


def listen_for_messages(client, username):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                final_message = username + '-' + message
                send_message_to_all(final_message)
            else:
                print(f"The message sent from client {username} is empty")
        except ConnectionResetError:
            remove_client(client, username)
            break


def send_message_to_client(client, message):
    client.sendall(message.encode())


def send_message_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)


def remove_client(client, username):
    client.close()
    active_clients.remove((username, client))
    update_client_list()


def client_handler(client):
    while True:
        try:
            username = client.recv(2048).decode("utf-8")
            if username != '':
                active_clients.append((username, client))
                prompt_message = "SERVER-" + f"{username} added to the chat"
                send_message_to_all(prompt_message)
                break
            else:
                print("Client username is empty")
        except ConnectionResetError:
            break

    threading.Thread(target=listen_for_messages, args=(client, username)).start()
    update_client_list()


def update_client_list():
    client_list.delete(0, tk.END)
    for user in active_clients:
        client_list.insert(tk.END, user[0])


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print(f"Server is running on {HOST}:{PORT}")
    except Exception as e:
        print(f"Unable to bind to host {HOST} and port {PORT}: {e}")
        return

    server.listen(LISTENER_LIMIT)

    while True:
        try:
            client, address = server.accept()
            print(f"Successfully connected to client {address[0]}:{address[1]}")
            threading.Thread(target=client_handler, args=(client,)).start()
        except KeyboardInterrupt:
            print("Server stopped by the user.")
            break
        except Exception as e:
            print(f"Error while accepting client connection: {e}")

    server.close()


def exit_server():
    if len(active_clients) > 0:
        messagebox.showinfo("Active Clients", "There are active clients connected to the server. Please disconnect all clients before exiting.")
    else:
        window.destroy()



if __name__ == "__main__":
    window = tk.Tk()
    window.title("Chat Server")

    window.configure(bg="#F7F7F7")

    server_info_label = tk.Label(window, text=f"Server Host: {HOST}\nServer Port: {PORT}", bg="#F7F7F7", font=("Arial", 12, "bold"))
    server_info_label.pack(pady=10)

    client_list_label = tk.Label(window, text="Active Clients:", bg="#F7F7F7", font=("Arial", 12, "bold"))
    client_list_label.pack()

    client_list = tk.Listbox(window, bg="#FFFFFF", width=30, font=("Arial", 10))
    client_list.pack(fill=tk.BOTH, expand=True)

    exit_button = tk.Button(window, text="Exit", command=exit_server, bg="#FF0000", fg="#FFFFFF", font=("Arial", 12, "bold"))
    exit_button.pack(pady=10)

    threading.Thread(target=start_server).start()

    window.mainloop()
