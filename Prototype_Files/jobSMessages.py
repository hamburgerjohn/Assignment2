# Not finished and not part of the assignment
import socket
import random
import time
import sys
import pickle
import messages
import Jobs


PORT = 6000
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())#gets ip
clientId = int(SERVER.replace('.','',-1))*100
print(clientId)
DISCONNECT = "qerty1234" #shared disconnect message
ADDR = (SERVER, PORT) 
val = 'y'
mesgnum = 0

# Connects to server, if no servers available then exit
try:
     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#creates client socket
     client.connect(ADDR) #connects socket to remote host
     print(f"Successfully connected to JobCreator at address {SERVER}")
except:
     print("No job creators are currently online")
     sys.exit(1)

val = 'y'
accept = 'y'

# Client's interaction with the server
while val == 'y':
     mesgnum+=1
     result = ''

     client.sendall(pickle.dumps(messages.ConnMesg(clientId+mesgnum)))  
     msg = pickle.loads(client.recv(1024))
     
     if msg.requestType == 7:
          print("No more jobs available")
          sys.exit(1)
     
     # Cycles through available jobs until no new jobs or one is chosen
     accept = input(f"Do you want to work on job {msg.jobNumber}? y/n")
     while accept != 'y':
          mesgnum+=1
          client.send(pickle.dumps(messages.DecJob(clientId+mesgnum)))
          msg = pickle.loads(client.recv(1024))

          # Checks if JobFull message was sent and thus no jobs available
          if msg.requestType == 7:
               print("All jobs were shown")
               sys.exit(1)

          accept = input(f"Do you want to work on job {msg.jobNumber}? y/n")

     mesgnum+=1
     jobTaken = msg
     client.sendall(pickle.dumps(messages.AccJob(msg.jobNumber, clientId+mesgnum)))
     msg = pickle.loads(client.recv(1024))

     if msg.requestType == 5:
          # Determines what job is done
          jobTaken.job.doJob()

     mesgnum+=1
     client.sendall(pickle.dumps(messages.JobComp(jobTaken.jobNumber,jobTaken.job,clientId+mesgnum)))
     msg = pickle.loads(client.recv(2048))

     # checks for acknowledgement message
     if msg.requestType == 5:
          print("Server recieved job output")
     val = input("Would you like to get a new job? y/n ")

