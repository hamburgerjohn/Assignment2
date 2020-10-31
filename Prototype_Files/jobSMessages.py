# Not finished and not part of the assignment
import socket
import random
import time
import sys
import messages
import pickle

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
jobList = ["job 1", "job 2", "job 3"]

        
#jobs that the seeker can do? ok      
def job1():
    print("Job Description: wait for 10 seconds ya goob")
    time.sleep(10)
    return "job 1 Completed Successfully :)"

def job2():
    print("Job Description: sort a string")
    msg = "wow dude"
    sorted_number = sorted(msg)
    return f"job 2 Completed...\nOriginal String: [{msg}] Numbers are now sorted Successfully: {sorted_number}"

def job3():
    print("Job Description: wait 20 seconds")
    time.sleep(20)
    return "job 3 Completed Successfully"


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
     client.sendall(pickle.dumps(messages.AccJob(msg.jobNumber, clientId+mesgnum)))

     # Determines what job is done
     if msg.jobNumber == 1:
          result = job1()
     elif msg.jobNumber == 2:
          result = job2()
     elif msg.jobNumber == 3:
          result = job3()

     mesgnum+=1
     client.sendall(pickle.dumps(messages.JobComp(msg.jobNumber,result,clientId+mesgnum)))
     msg = pickle.loads(client.recv(1024))

     # checks for acknowledgement message
     if msg.requestType == 5:
          print("Server recieved job output")
     val = input("Would you like to get a new job? y/n ")

