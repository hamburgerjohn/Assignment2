import socket
import random
import time
import sys

PORT = 6000
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())#gets ip
DISCONNECT = "qerty1234" #shared disconnect message
ADDR = (SERVER, PORT) 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#creates client socket
client.connect(ADDR) #connects socket to remote host
val = "y"
jobList = ["job 1", "job 2", "job 3"]

def send(msg): #function to send messages to jobcreator
    message = msg.encode(FORMAT) 
    client.send(message) 
    received = client.recv(2048).decode(FORMAT)
    print(received)
    if received.find("job 1") != -1:
        job1()
    elif received.find("job 2") != -1:
        job2()
    elif received.find("job 3") != -1:
        job3()
    elif received.find("terminated") != -1:
        sys.exit(1)

        
#jobs that the seeker can do?       
def job1():
    print("Job Description: wait for 10 seconds ya goob")
    time.sleep(10)
    send("job 1 Completed Successfully :)")

def job2():
    print("Job Description: sort a string")
    msg = "wow dude"
    sorted_number = sorted(msg)
    print(f"job 2 Completed...\nOriginal String: [{msg}] Numbers are now sorted Successfully: {sorted_number}")
    send(f"job 2 Completed Successfully")

def job3():
    print("Job Description: wait 20 seconds")
    time.sleep(20)
    send("job 3 Completed Successfully :)")

try:
    while val == "y":
        val = input("Want a stupid job y/n")
        send(random.choice(jobList))

except:
    sys.exit(1)


    




