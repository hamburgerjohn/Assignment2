import socket 
import threading
import time
import sys
import pickle
import random
import struct

PORT = 6000
SERVER = socket.gethostbyname(socket.gethostname()) # Get IP
ADDR = (SERVER,PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates server socket
iplist = [ "192.168.1.6", "www.google.ca", "www.uwindsor.ca", "www.minecraft.net" ]
subnets = ["192.168.1.1/24"]

# --- Shared Messages ---

DISCONNECT =        "disconnect"
JOB_REQUEST =       "jobrequest"
JOB_REPORT =        "jobreport"
JOB_COMPLETE =      "completed"
JOB_INCOMPLETE =    "incomplete"
JOB_ASSIGNMENT =    "assignment"
JOB_SUCCESS =       "success"
JOB_FAILURE =       "failure"
COMPLETION_ACK =    "goodjob"

# --- Port Binding ---

try: # checks if port is being used 
    server.bind(ADDR)
    print(f"Port :{PORT} bound successfully.")
except:
    print(f"Port :{PORT} is being used.") 
    quit()

# --- Function Definitions ---

def send(conn, addr, v):
    print(f"\nSending the following message to client @ {addr}\n\t{v}\n")
    m = pickle.dumps(v)
    conn.send(m)

def ifsuccess(conn, addr, v): # Checks if incoming client is reporting job success
    if v[1] == JOB_COMPLETE: # Client reported success
        print(f"Client @ {addr} has completed their task", end="")
        if len(v) > 2:
            print(f" with the following return value:\n\t\"{v[2]}\"")
        send(conn, addr, [ COMPLETION_ACK ])
    elif v[1] == JOB_INCOMPLETE:
        print(f"Client @ {addr} has not completed their task")
        send(conn, addr, [ COMPLETION_ACK ])

def hire(conn, addr, v): # Give job to a client
    jobNum = random.randint(0, 2)

    if jobNum == 0:
        ip = random.choice(iplist)
        send(conn, addr, [ JOB_ASSIGNMENT, jobNum+1, ip ])
    if jobNum == 1:
        ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        port = random.randint(0, 65535)
        send(conn, addr, [ JOB_ASSIGNMENT, jobNum+1, ip, port ])
    if jobNum == 2:
        subnet = random.choice(subnets)
        send(conn, addr, [JOB_ASSIGNMENT, jobNum+1, subnet])

def connect_client(conn, addr):
    print(f"New connection established.")
    connected = True
    try: # Check if client disconnected by not sending disconnect message
        while connected:
            m = conn.recv(2048)
            v = pickle.loads(m)
            print(f"Received the following message from the client @ {addr}:\n\t{v}\n")

            if v[0] == DISCONNECT: # Client requested disconnect
                connected = False
                print(f"Client @ {addr} has requested disconnect.")   
                conn.close()
                print(f"\tDisconnected.")
                print(f"\n{threading.activeCount()-2} active connections.")
                
            elif v[0] == JOB_REQUEST: # Client requested job
                print(f"Client @ {addr} is requesting a job")
                hire(conn, addr, v)
                
            elif v[0] == JOB_REPORT: # Client is reporting job status
                print(f"Client @ {addr} is reporting back")
                ifsuccess(conn, addr, v)
    except:
        print(f"Client @ {addr} has disconnected on exception.")
        conn.close()
        print(f"{threading.activeCount()-2} active connections.\n")
            
def start():
    server.listen() # Listen for incoming connections
    print(f"Running on address {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept(); # Server accepts the connection from the client
        thread = threading.Thread(target=connect_client, args=(conn, addr)) # Create thread for each client, connect_client invoked by run() method
        thread.start() # Start thread
        print(f"\n{threading.activeCount()-2} active connections.")

def liveConnections():
    print(f"Live Connections: {list(liveIPs.values())}")

# --- Start ---

print("Starting...")
for i in range(0): # Just for fun
    time.sleep(1)
    print(".")
print("Started.")
start()
