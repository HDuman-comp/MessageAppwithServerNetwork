import socket
import threading
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


HOST = '127.0.0.1'
PORT = 5022

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def listen_for_messages_from_server():
    while True:
        try:
            message = client.recv(2048).decode("utf-8")
            if message != '':
                username = message.split("-")[0]
                content = message.split("-")[1]


                current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                formatted_message = f"[{username}]: {content}"
                formatted_message = f"[{current_date}] {formatted_message}"


                message_text.insert(tk.END, formatted_message + "\n")
                message_text.tag_add("color", f"{message_text.index(tk.END)} linestart", f"{message_text.index(tk.END)} lineend")
                message_text.tag_config("color", foreground="#FF8300", font=("Arial", 10, "bold"))  # Set color for message
                message_text.tag_add("name", f"{message_text.index(tk.END)} linestart + 1c", f"{message_text.index(tk.END)} lineend - 1c")
                message_text.tag_config("name", foreground="#008000", font=("Arial", 10, "bold"))  # Set color for name
                message_text.tag_add("date", f"{message_text.index(tk.END)} linestart", f"{message_text.index(tk.END)} linestart + 20c")
                message_text.tag_config("date", foreground="#FF0000", font=("Arial", 10, "bold"))  # Set color for date

                message_text.see(tk.END)
        except ConnectionAbortedError:
            break


def send_message_to_server():
    message = message_entry.get()
    if message != '':
        client.sendall(message.encode())
        message_entry.delete(0, tk.END)
    else:
        messagebox.showinfo("Empty Message", "Message cannot be empty")


def communicate_to_server():
    username = username_entry.get()
    if username != '':
        client.sendall(username.encode())
        threading.Thread(target=listen_for_messages_from_server).start()
        send_button.config(state=tk.NORMAL)
    else:
        messagebox.showinfo("Empty Username", "Username cannot be empty")
        exit(0)


def connect_to_server():
    try:
        client.connect((HOST, PORT))
        connect_button.config(state=tk.DISABLED)
        communicate_to_server()
    except Exception as e:
        messagebox.showerror("Connection Error", f"Unable to connect to the server: {e}")
        exit(0)


def exit_client():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        client.close()
        exit(0)



window = tk.Tk()
window.title("Chat Client")


window.configure(bg="#F7F7F7")


username_label = tk.Label(window, text="Username:", bg="#F7F7F7")
username_label.pack()
username_entry = tk.Entry(window)
username_entry.pack()


connect_button = tk.Button(window, text="Connect", command=connect_to_server, bg="#FF8300", fg="white", font=("Arial", 12, "bold"))
connect_button.pack(pady=10)


message_text = tk.Text(window, bg="#FFFFFF")
message_text.pack(fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
message_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=message_text.yview)


message_label = tk.Label(window, text="Message:", bg="#F7F7F7")
message_label.pack()
message_entry = tk.Entry(window)
message_entry.pack()


send_button = tk.Button(window, text="Send", command=send_message_to_server, state=tk.DISABLED, bg="#008000", fg="white", font=("Arial", 12, "bold"))
send_button.pack(pady=10)


exit_button = tk.Button(window, text="Exit", command=exit_client, bg="#FF0000", fg="white", font=("Arial", 12, "bold"))
exit_button.pack(pady=10)


window.mainloop()
