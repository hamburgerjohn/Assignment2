import socket
import time
import sys
import pickle
import argparse
from scapy.all import *

PORT = 6000
SERVER = socket.gethostbyname(socket.gethostname()) # Get IP
ADDR = (SERVER, PORT) 
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create client socket
conn.connect(ADDR) # Connects socket to remote host
print(f"Connected to server @ {ADDR}\n")
val = "y"

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

# --- Function Definitions ---

def send(v): # Function to send messages to the server
    # Pickle the message
    m = pickle.dumps(v)
    conn.send(m)

    if v[0] == DISCONNECT: 
        print(f"Disconnecting from server @ {ADDR}")
        val = "n"
    else: 
        print(f"Waiting for server @ {ADDR}\n")
        m = conn.recv(2048)
        v = pickle.loads(m)
        if v[0] == JOB_ASSIGNMENT:
            print(f"Received a job assignment from server @ {ADDR}")
            if v[1] == 1:
                job1(v)
            elif v[1] == 2:
                job2(v)
            elif v[1] == 3:
                job3(v)
        elif v[0] == COMPLETION_ACK:
            print(f"Server @ {ADDR} acknowledged completion\n")
        
def job1(v):
    print(f"\nWorking on job 1 for @ {ADDR}")
    print(v)
    host = v[2]
    print(f"\nPinging host @ {host}")
    p = sr1(IP(dst=host,ttl=20)/ICMP(), timeout=2, verbose=0)
    
    if p == None:
        print(f"The host @ {host} is not online.\n")
        send([ JOB_REPORT, JOB_COMPLETE, JOB_FAILURE ])
    else:
        print(f"The host @ {host} is online.\n")
        send([ JOB_REPORT, JOB_COMPLETE, JOB_SUCCESS ])
        
def job2(v):
    print(f"\nWorking on job 2 for @ {ADDR}")
    host = v[2]
    port = v[3]
    sport = RandShort()

    print(f"Scanning {host}:{port} from :{sport}")

    pkt = sr1(IP(dst=host)/TCP(sport=sport, dport=port, flags="FPU"), timeout=1, verbose=0)
    
    if pkt != None:
        if pkt.haslayer(TCP):
            if pkt[TCP].flags == 20:
                send([ JOB_REPORT, JOB_COMPLETE, "Closed" ])
            else:
                print("port, TCP flag {pkt[TCP].flag|")
        elif pkt.haslayer(ICMP):
            send([ JOB_REPORT, JOB_COMPLETE, "ICMP resp / filtered"])
        else:
            send([ JOB_REPORT, JOB_COMPLETE, "Unknown resp"])
    else:
        send([ JOB_REPORT, JOB_COMPLETE, "Open / filtered"])

def job3(v):
    print(f"Working on job 3 for @ {ADDR}")
    subnet = v[2]
    print("Target Subnet: " + subnet)
    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    req = ether/arp
    res = srp(req, timeout=2, verbose=0)[0]
    IPs = []
    for sent, rec in res:
        IPs.append(rec.psrc)
    if not IPs:
        print("No live IP Addresses")
        send([ JOB_REPORT, JOB_COMPLETE, JOB_FAILURE ])
    else:
        print("Live IP Addresses: " + str(IPs))
        send([ JOB_REPORT, JOB_COMPLETE, JOB_SUCCESS ])

# --- Start ---

try:
    while True:
        val = input("Would you like a job? (y/n): ")
        if val == "y":
            send([ JOB_REQUEST ])
        else:
            send([ DISCONNECT ])
            sys.exit(0)
except:
    sys.exit(1)

    




