import threading
import socket

host = "127.0.0.1"
port = 59000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
nicknames = []
channels = {
     "1": [],
     "2": [],
     "3": []
}


# MULTI CHANNEL CHATROOM
def channel1(message):
    for client in channels["1"]:
          client.send(message.encode("utf-8"))

def channel2(message):
    for client in channels["2"]:
          client.send(message.encode("utf-8"))

def channel3(message):
    for client in channels["3"]:
          client.send(message.encode("utf-8"))


def handleClient(client):
     while True:
        try:
          message = client.recv(1024).decode()
          message, givenChannel = message.split("|")

          if message.startswith("/pm "):
              recipient, privateMessage = message.split(" ", 2)[1:]
              recipientIndex = nicknames.index(recipient)
              recipientClient = clients[recipientIndex]
              recipientClient.send(f"PM from {privateMessage}".encode("utf-8"))

          if(givenChannel == "1"):
               channel1(message)
               print("Sent a message to channel 1")
          elif(givenChannel == "2"):
               channel2(message)
               print("Sent a message to channel 2")
          elif(givenChannel == "3"):
               channel3(message)
               print("Sent a message to channel 3")
          print(message)
          print(givenChannel)

        except:
          index = clients.index
          clients.remove(client)
          client.close()
          nickname = nicknames[index]
          channel1(f'{nickname} has disconnected.'.encode('utf-8'))
          nicknames.remove(nickname)
          break



# CONNECT TO CLIENTS
def connectToClients():
     while True:
          print("Server is running...")
          client, address = server.accept()
          print(f'connection is established with {str(address)}')

          client.send('alias?'.encode('utf-8'))
          nickname = client.recv(1024)

          client.send('channel?'.encode('utf-8'))
          givenChannel = client.recv(1024)

          nicknames.append(nickname)
          clients.append(client)

          if(givenChannel.decode("utf-8") in channels):
              channels[givenChannel.decode("utf-8")].append(client)
              print(f"Added to list of channel {givenChannel}")
          else:
               print(f"Invalid channel: {givenChannel}")
               client.send("Invalid channel number.".encode("utf-8"))
               client.close()
               continue

          print(f'The alias of this client is {nickname}'.encode('utf-8'))
          ##channel1(f'{nickname} has connected to the channel'.encode('utf-8'))
          client.send("you are now connected!".encode("utf-8"))
          
          thread = threading.Thread(target = handleClient, args=(client,))
          thread.start()


connectToClients()