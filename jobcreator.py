import socket 
import threading

PORT = 6000
SERVER = socket.gethostbyname(socket.gethostname())#gets ip
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates server socket
DISCONNECT = "qerty1234" #shared disconnect message with clients
jobAvail = [1,1,1]

try: #checks if port is being used 
    server.bind(ADDR)
except:
    print("Port is being used") 
    quit()

def ifsuccess(conn,addr,msg):#checks if incomming client is reporting job success

    if msg.find("Successfully") != -1:
        print(f"Job Seeker @ {addr} has completed their task")
        conn.send("Thank you".encode(FORMAT))
        a = [int(i) for i in msg.split() if i.isdigit()]
        jobNum = a[0] - 1

        if msg.find(f"job {jobNum + 1}") != -1:
            jobAvail[jobNum] = 1
        
        return True
    
    else:
        print(f"Job Seeker @ {addr} is requesting {msg}")
        return False
            
def hire(conn,addr,msg):#gives job to client

    a = [int(i) for i in msg.split() if i.isdigit()]
    jobNum = a[0] -1
    
    if jobAvail[jobNum] == 1:
        conn.send(f"You have been assigned job {jobNum + 1} report back plz".encode(FORMAT))
        jobAvail[jobNum] = 0
  
    else:
        conn.send("job is unavailable".encode(FORMAT))

def connect_client(conn, addr): #handles connected clients
    print("New Job Seeker has Connected")
    connected = True
    try: #checks if client disconnected by not sending disconnect message
        while connected:
            msg = conn.recv(2048).decode(FORMAT) #decodes received string from byte format to utf-8

            if msg == DISCONNECT: #checks if disconnect message was sent by client
                connected = False
                print(f"Job Seeker @ {addr} has disconnected") 
                conn.close()

            else:
                if not ifsuccess(conn,addr,msg):#checks if client completed task successfully
                        hire(conn,addr,msg)#offers client a job
                    
    except:
        print(f"Job Seeker @ {addr} has disconnected") 
        conn.close()         
         
def start():
    server.listen() #listens for connections from clients
    print(f"Job Creator is running on address {SERVER}")
    while True:
        conn, addr = server.accept() #server accepts the connection from client via 3-way handshake
        thread = threading.Thread(target=connect_client, args=(conn,addr))#creates thread for each client, connect_client invoked by run() method 
        thread.start()#starts thread
        print(f"Number of Job Seekers connected {threading.activeCount()-1} ")#prints how many clients/threads are connected/alive
    
print("Job Creator has been activated")
start()

