from socket import *
from threading import *

clients=[]
names =[]

def clientThread(client):
    initname = client.recv(1024).decode('utf-8')
    bayrak = True
    while True:
        try:
            if bayrak:
                names.append(initname)
                print(initname, 'baglandi')
                bayrak = False

            if client.recv(1024).decode('utf8') == "kanka fotoğraf geliyo":
                filepath = client.recv(1024).decode('utf-8')
                filepath = filepath.split("/")[-1]
                file = open(filepath, "wb")
                image_chunk = client.recv(1024)

                while image_chunk:
                    file.write(image_chunk)
                    image_chunk = client.recv(1024)
                file.close()

            message = client.recv(1024).decode('utf-8')


            for c in clients:
                if c != client:
                    index = clients.index(client)
                    name = names[index]
                    c.send((name + ':' + message).encode('utf-8'))

        except:
            index = clients.index(client)
            clients.remove(client)
            name = names[index]
            names.remove(name)
            print(name + 'cikti')
            break


server = socket(AF_INET, SOCK_STREAM)

ip= 'localhost'
port = 8081

server.bind((ip,port))
server.listen()
print('Server dinlemede')

while True:
    client, address = server.accept()
    clients.append(client)
    print('Baglanti yapildi', address[0]+ ':' + str(address[1]))
    thread = Thread(target=clientThread, args=(client,))
    thread.start()