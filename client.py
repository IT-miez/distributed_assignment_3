import threading
import socket

print("*** CLIENT APPLICATION FOR CHATROOMS ***")
nickname = input("Input your nickname: ")
channelOfClient = input("What channel do you want to connect? (1, 2, 3)")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 59000))

def receiveFunction():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "alias?":
                client.send(nickname.encode("utf-8"))
            elif message == "channel?":
                client.send(channelOfClient.encode("utf-8"))
            else:
                print(message)
        except:
            print("Ending client through server")
            client.close()
            break
        
def clientSendMessage():
    while True:
        message = f'{nickname}: {input("")}|{channelOfClient}'
        if message == f'{nickname}: quit|{channelOfClient}':
            print("Closing client")
            client.send(message.encode("utf-8"))
            client.close()
            break
        else:
            client.send(message.encode("utf-8"))

receiveThread = threading.Thread(target=receiveFunction)
receiveThread.start()

sendThread = threading.Thread(target=clientSendMessage)
sendThread.start()