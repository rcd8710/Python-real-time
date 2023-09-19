import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.0.0.1'  # The host where the server is running
PORT = 4768

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket



FONT = ("Helvetica,18")
beige = '#F5F5DC'
bisque1 = '#FFE4C4'
coral = '#FF7f50'
dark_salmon = '#E9967A'
Button_Font = ("Helvetica,15")
small_Font = ("Helvetica,13")
brown2 = "#EE3B3B"
black ="#1B1212"

root = tk.Tk()
root.geometry('700x550')
root.title('webroom client')
root.resizable(False,False)

def message_add(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END,message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    try:
        client.connect((HOST, PORT))  # Attempt to connect to the server
        print(f"Connected to server at {HOST} {PORT}")
        message_add("You have sucessfully connected")
    except:
        messagebox.showerror("Cannot connect to server" , f"Unable to connect to host {HOST} {PORT}")
        exit(0)
    username = username_textbox.get()
    if username != "":
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username")
        exit(0)
    threading.Thread(target=serverListener, args=(client,)).start()
    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)


def send_message():
    message = message_textbox.get()
    if message != "":
        client.sendall(message.encode())
        message_textbox.delete(0,len(message))
    else:
        messagebox.showerror("Message is empty")


root.grid_rowconfigure(0,weight=1)
root.grid_rowconfigure(0,weight=4)
root.grid_rowconfigure(0,weight=1)
Head_frame = tk.Frame(root,width=700,height=75,bg = bisque1)
Head_frame.grid(row=0,column=0,sticky=tk.NSEW)
mid_frame = tk.Frame(root,width=700,height = 400,bg = beige)
mid_frame.grid(row=1,column=0,sticky=tk.NSEW)
bottom_frame = tk.Frame(root,width=700,height= 75,bg =bisque1)
bottom_frame.grid(row=2,column=0,sticky=tk.NSEW)

user_label = tk.Label(Head_frame,text = "Enter username:",font = FONT,bg = bisque1,fg="#1B1212")
user_label.pack(side =tk.LEFT,padx=10 )

username_textbox = tk.Entry(Head_frame, font = FONT,bg = beige, fg="#1B1212",width=20)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(Head_frame,text="JOIN",font=FONT,bg= brown2,fg =black,command=connect)
username_button.pack(side=tk.LEFT,padx=15)

message_textbox = tk.Entry(bottom_frame, font = FONT,bg = beige, fg="#1B1212",width=40)
message_textbox.pack(side=tk.LEFT,padx= 10)

message_button = tk.Button(bottom_frame,text='SEND',font=Button_Font,bg=brown2,fg=black,command=send_message)
message_button.pack(side=tk.LEFT,padx=10)

message_box = scrolledtext.ScrolledText(mid_frame,font=small_Font,bg = beige,fg = black,width=80, height=25)
message_box.pack(side=tk.TOP)
message_box.config(state=tk.DISABLED)
        # The port the server is listening on

def serverListener(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != "":
            username = message.split(":")[0]
            content = message.split(":")[1]

            message_add(f'[{username}] {content}')
        else:
            messagebox.showerror("Error","Message taken from client is empty")





def main():
    root.mainloop()


if __name__ == '__main__':
    main()
