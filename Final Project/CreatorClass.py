import socket 
import threading
import time
import sys
import pickle
import random
import struct
import math
import tkinter as tk
import os
from os import path

class JobCreator():
     # Binds the Socket and initializes UI and other class variables
     def __init__(self, jobs = [0,1,2,3,4,5,6]):

          fileNumber = 1

          while(path.exists(f"Seeker{fileNumber}.log")): #removes all seeker.log files once new creator is run
              os.remove(f"Seeker{fileNumber}.log")
              fileNumber += 1

          self.file = open("Creator.log",'w') #redirects creates file to output to

          # Used to map recieved job numbers to text for easier understanding
          self.job_list = {}
          self.job_list[0] = 'Check if online'
          self.job_list[1] = 'Live IP addresses'
          self.job_list[2] = 'ICMP Flood'
          self.job_list[3] = 'TCP Flood'
          self.job_list[4] = 'Status of port'
          self.job_list[5] = 'Trace Route'
          self.job_list[6] = 'Spy on Neighbours'

          # Creates the UI of the JobCreator
          self.root = tk.Tk()
          self.jobs = jobs
          self.create_widgets()
          self.grid_counter = [0,1]

          self.PORT = 6000
          self.SERVER = socket.gethostbyname(socket.gethostname()) # Get IP
          self.ADDR = (self.SERVER,self.PORT)
          self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates server socket
          self.clients = []
          self.traceinfo = [[True, math.inf, None], [True, math.inf, None], [True, math.inf, None], [True, math.inf, None], [True, math.inf, None]]
          self.iplist = ["192.168.1.6", "www.google.ca", "docs.python.org", "www.minecraft.net", "cs.uwaterloo.ca"]
          self.multijobqueue = [0,0]
          self.threadList=[]
          self.selectedThreads = []
          self.numOfBots = 0
          self.jobQueue = 0
          self.attackChoice = ""
          self.TCPTarget = ['',0]
          self.ICMPTarget = ''
          self.subnets = ["192.168.1.1/24"]


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

          # --- Port Binding ---

          try: # checks if port is being used 
              self.server.bind(self.ADDR)
              self.add_main_text(f"Port :{self.PORT} bound successfully.")
              self.run()
          except:
              self.add_main_text(f"Port :{self.PORT} is being used.") 

          self.root.mainloop()

     # --- Function Definitions ---

     # Creates the UI of the JobCreator
     def create_widgets(self):
          self.window = tk.Frame(self.root)
          job_text = ''
          for i in self.jobs:
               if i in self.job_list:
                    job_text += f"{self.job_list[i]}:"
                    
          self.job_label = tk.Label(self.window, text = f"Jobs in Use = {job_text}")
          self.main_label = tk.Label(self.window, text = "Main Display")
          self.main_display = tk.Text(self.window, state = 'disabled', yscrollcommand = True, width = 50)
          self.quit = tk.Button(self.window, text = "Disconnect", command = self.disconnect)

          self.window.pack()
          self.job_label.grid(column = 0, row = 0)
          self.main_label.grid(column = 0, row = 1)
          self.main_display.grid(column = 0, row = 2)
          self.display = threading.local()
          self.quit.grid(column = 0, row = 3)

     # Used to write to the main text box
     def add_main_text(self, text):
          self.main_display['state'] = 'normal'
          self.main_display.insert(tk.INSERT, text)
          self.main_display.see('end')
          self.main_display['state'] = 'disabled'
          self.file.write(text)
          self.file.flush()
          self.root.update()

     # Used to write to the individual text boxes
     def add_text(self, text, display):
          display['state'] = 'normal'
          display.insert(tk.INSERT, text)
          display.see('end')
          display['state'] = 'disabled'
          self.file.write(text)
          self.file.flush()
          self.root.update()

     # Destroys the UI and ends the process
     def disconnect(self):
          self.root.destroy()
          sys.exit(0)

     # Sends a message to the JobSeeker
     def send(self, conn, addr, v, display):
         self.add_text(f"\nSending the following message to client @ {addr}\n\t{v}\n", display)
         m = pickle.dumps(v)
         conn.send(m)

     # Checks if incoming client is reporting job success
     def ifsuccess(self, conn, addr, v, display): 
         if v[1] == self.JOB_COMPLETE: # Client reported success
             self.add_text(f"Client @ {addr} has completed their task\n", display)
             if len(v) > 2:
                 self.add_text(f" with the following return value:\n\t\"{v[2]}\"\n", display)
             self.send(conn, addr, [ self.COMPLETION_ACK ], display)
         elif v[1] == self.JOB_INCOMPLETE:
             self.add_main_text(f"Client @ {addr} has not completed their task\n", display)
             self.send(conn, addr, [ self.COMPLETION_ACK ], display)

     # Give job to a client
     def hire(self, conn, addr, v, display): 
          jobNum = int(random.choice(self.jobs))

          # Check if Online
          if jobNum == 0:
               ip = random.choice(self.iplist)
               self.send(conn, addr, [ self.JOB_ASSIGNMENT, jobNum+1, ip ], display)

          # Live IP Addresses
          elif jobNum == 1:
               subnet = random.choice(self.subnets)
               self.send(conn, addr, [self.JOB_ASSIGNMENT, jobNum+1, subnet], display)
     
          # ICMP Flood
          elif jobNum == 2:
               self.multijobqueue[0] += 1
               if(self.multijobqueue[0] == 1):
                    # ensures that all jobseeker recieve the same target
                    self.ICMPTarget = random.choice(self.iplist)
               while (self.multijobqueue[0] < 2):
                    time.sleep(0.5)
               # Allows for other jobseekers to join
               time.sleep(5)
               self.send(conn, addr, [ self.JOB_ASSIGNMENT, jobNum+1, self.ICMPTarget], display)
               self.multijobqueue[0] = 0

          # TCP Flood
          elif jobNum == 3:
               self.multijobqueue[1] += 1
               if(self.multijobqueue[1] == 1):
                    self.TCPTarget[0] = random.choice(self.iplist)
                    self.TCPTarget[1] = random.randint(0,65535)
               while (self.multijobqueue[1] < 2):
                    time.sleep(0.5)
               # Allows for other jobseekers to join
               time.sleep(5)
               self.send(conn, addr, [ self.JOB_ASSIGNMENT, jobNum+1, self.TCPTarget[0], self.TCPTarget[1]], display)
               self.multijobqueue[1] = 0

          # Check Port Status
          elif jobNum == 4:
               ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
               port = random.randint(0, 65535)
               self.send(conn, addr, [ self.JOB_ASSIGNMENT, jobNum+1, ip, port ], display)

          # Trace route
          elif jobNum == 5:  
               reachable = False
               target = ""
               while not reachable:
                    target = random.randint(0, len(self.iplist)-1)
                    reachable = self.traceinfo[target][0]

               self.send(conn, addr, [self.JOB_ASSIGNMENT, jobNum + 1, self.iplist[target]], display)

          # Spy on neighbours
          elif jobNum == 6:
               self.send(conn, addr, [self.JOB_ASSIGNMENT, jobNum+1, addr], display)

          else:
               self.add_text("That is not a valid job number.")
               self.hire(conn, addr, v)

     # Connects the JobSeeker and monitors for their messages
     def connect_client(self, conn, addr):
          # Creates the label and new textbox for the newly connected Jobseeker
          display_label = tk.Label(self.window, text = f"{addr}")
          display = tk.Text(self.window, state = 'disabled', yscrollcommand = True, width = 50)
          self.grid_counter[0] += 1
          if(self.grid_counter[0] > 3):
               self.grid_counter[0] = 1
               self.grid_counter[1] += 2
          display_label.grid(column = self.grid_counter[0], row = self.grid_counter[1], padx = (10,0))
          display.grid(column = self.grid_counter[0], row = self.grid_counter[1]+1, padx = (10,0))

          self.add_text("New connection established.\n", display)
          connected = True
          try: # Check if client disconnected by not sending disconnect message
               while connected:
                    m = conn.recv(2048)
                    v = pickle.loads(m)
                    self.add_text(f"Received the following message from the client @ {addr}:\n\t{v}\n", display)
                    if v[0] == self.DISCONNECT: # Client requested disconnect
                         connected = False
                         self.add_main_text(f"Client @ {addr} has requested disconnect.\n")   
                         self.handledisconnect(conn,addr)
                         self.add_text(f"\tDisconnected.\n", display)
                         display_label.destroy()
                         display.destroy()
                         self.add_main_text(f"\n{len(self.clients)} active connections.\n")
                
                    elif v[0] == self.JOB_REQUEST: # Client requested job
                         self.add_text(f"Client @ {addr} is requesting a job\n", display)
                         self.hire(conn, addr, v, display)
                
                    elif v[0] == self.JOB_REPORT: # Client is reporting job status
                         self.add_text(f"Client @ {addr} is reporting back\n", display)
                         self.ifsuccess(conn, addr, v, display)
          except:
               # Removes the label and textbox from the UI
               display_label.destroy()
               display.destroy()
               self.add_main_text(f"Client @ {addr} has disconnected on exception.\n")
               self.handledisconnect(conn,addr)
               self.add_main_text(f"{len(self.clients)} active connections.\n")
     
     # Handles events when a JobSeeker disconnects
     def handledisconnect(self, conn, addr):
          for x in self.traceinfo:
               if x[1] == conn:
                    x[1] = None
                    x[2] = math.inf
          
          # Resets grid counter if all clients disconnected
          if len(self.clients) == 0:
               self.grid_counter = [0,1]

          conn.close()
          self.clients.remove(addr)

     # Listens for connections and starts a new thread to handle the JobSeeker
     def start(self):
          self.server.listen() # Listen for incoming connections
          self.add_main_text(f"Running on address {self.SERVER}:{self.PORT}\n")
          while True:
               conn, addr = self.server.accept(); # Server accepts the connection from the client
               self.clients.append(addr)

               # Create thread for each client, connect_client invoked by run() method
               thread = threading.Thread(target=self.connect_client, args=(conn, addr)) 

               # Makes it so all threads close when main thread is closed
               thread.daemon = True
               self.threadList.append([conn, addr])
               self.add_main_text(f"\n{len(self.clients)} active connections.\n")
               thread.start() # Start thread


     # --- Start ---
     def run(self):
          self.add_main_text("Starting...\n")
          self.add_main_text("Started.\n")
          thread = threading.Thread(target = self.start)
          # Makes it so all threads close when main thread is closed
          thread.daemon = True
          thread.start()


     # Returns the list of active threads
     def getThreads(self):
          return self.threadList

if __name__ == '__main__':
     jobC = JobCreator()
