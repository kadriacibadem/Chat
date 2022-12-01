import os.path
from socket import *
from threading import *
from tkinter import *
from tkinter import filedialog as fd
from PIL import ImageTk, Image
import requests
client = socket(AF_INET, SOCK_STREAM)
ip= 'localhost'
port = 8081

client.connect((ip, port))

pencere = Tk()
pencere.title('Chat')


messages =Text(pencere, width=50)
messages.grid(row=0, column=0, padx=10, pady=10)
yourMessage = Entry(pencere, width=50)
yourMessage.insert(0, 'Isminiz')
yourMessage.grid(row=1,column=0,padx=10,pady=10)
yourMessage.focus()
yourMessage.select_range(0, END)

def sendMessage():
    clientMessage = yourMessage.get()
    messages.insert(END, '\n'+ 'Sen: ' + clientMessage)
    client.send(clientMessage.encode('utf-8'))
    yourMessage.delete(0, END)


def openFile():
    client.send("kanka fotoğraf geliyo".encode("utf-8"))
    filepath = fd.askopenfilename()
    client.send(filepath.encode("utf-8"))
    file = open(filepath,"rb")
    data = file.read(40960000)

    client.send(data)
    file.close()
bmessageGonder = Button(pencere, text= 'Gonder',command=sendMessage)
bmessageGonder.grid(row=2,column=0,padx=5,pady=5)

dosyaSec = Button(pencere, text = 'Dosya Sec', command=openFile)
dosyaSec.grid(row=3,column=0,padx=5,pady=5)



def recvMessage():
    global my_image
    while True:
        serverMessage = client.recv(1024).decode('utf-8')
        if serverMessage == "kanka fotoğraf geliyo":
            print("if içerisi")
            filepath = client.recv(1024).decode('utf-8')
            file = open("./images/"+filepath, "wb")
            image_chunk = client.recv(40960000)
            file.write(image_chunk)
            file.close()
            print(filepath)
            #my_image = ImageTk.PhotoImage(Image.open(requests.get(filepath, stream=True).raw))
            #position = messages.index(INSERT)
            #messages.image_create(END, image=my_image)

        else:
            messages.insert(END, '\n' + serverMessage)




recvThread = Thread(target=recvMessage)
recvThread.daemon= True
recvThread.start()

pencere.mainloop()