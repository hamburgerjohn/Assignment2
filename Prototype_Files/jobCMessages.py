# Not finished and not part of the assignment
import socket 
import threading
import messages
import pickle
import Jobs
import time
import sys

PORT = 6000
SERVER = socket.gethostbyname(socket.gethostname())#gets ip
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates server socket
DISCONNECT = "qerty1234" #shared disconnect message with clients
jobs = [Jobs.ICMPFlood('192.168.2.10'),Jobs.ICMPFlood('192.168.2.12'),Jobs.ICMPFlood('192.168.2.120')]
jobProg = []
jobComp = []

try: #checks if port is being used 
	server.bind(ADDR)
except:
	print("Port is being used") 
	quit()


def connect_client(conn, addr): #handles connected clients
	complete = True
	jobNumber = 0
	print("New Job Seeker has Connected")

	try:
		while True:
			msg = pickle.loads(conn.recv(1024))
			print(msg.messageId)
			print(msg.requestType)


			if msg.requestType == 1:
				try:
					conn.sendall(pickle.dumps(messages.JobMesg(jobs[jobNumber],jobNumber)))
				except Exception as e : #if there are no jobs available
					#print(e.message)
					conn.sendall(pickle.dumps(messages.JobFull))

			elif msg.requestType == 3:
				complete = False
				jobNumber = msg.jobNumber
				
				jobProg.append(jobNumber)
				if isinstance(jobs[jobNumber], Jobs.MultiJob):
					print("Is a multipart Job")
					jobs[jobNumber].addJobTaker(addr)
					print("Now Wait")
					while jobs[jobNumber].takers < 2:
						print("Waiting")
						time.sleep(1)
					conn.sendall(pickle.dumps(messages.AckMesg))
				else:
					print("Is not a multipart Job")
					jobs[jobNumber].setJobTaker(addr)
					conn.sendall(pickle.dumps(messages.AckMesg))

			elif msg.requestType == 4:
				try:
					jobNumber+=1
					conn.sendall(pickle.dumps(messages.JobMesg(jobs[jobNumber],jobNumber)))
				except:
					conn.sendall(pickle.dumps(messages.JobFull))

			elif msg.requestType == 6:
				complete = True
				print(f"Jobseeker at {addr} return {msg.jobResult} for job {msg.jobNumber}.")
				jobProg.remove(jobNumber)
				jobComp.append({jobNumber, msg.jobResult})
				jobNumber = 0
				conn.sendall(pickle.dumps(messages.AckMesg))


	except:
		if complete == False:
			jobProg.remove(jobNumber)
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
