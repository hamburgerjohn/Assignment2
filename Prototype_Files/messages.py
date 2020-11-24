# Not finished and not part of the assignment
# Defines the messages sent between the client and host

# Sent by client to signify they want a job

class ConnMesg: 
     requestType = 1
     messageId = 0
     
     def __init__(self, ID):
          self.messageId = ID

# Sent by server containing job number and description
class JobMesg:
     requestType = 2
     messageId = 0
     job = ''
     jobNumber = 0

     def __init__(self, job, jobNumber):

          self.jobNumber = jobNumber
          self.jobDesc = "This is a job"
          self.job = job
          self.messageId = 1

# Sent by client to signal they are working on a job
class AccJob:
     requestType = 3
     jobNumber = 0
     messageId = 0

     def __init__(self, jobNum, Id):
          self.jobNumber = jobNum
          self.messageId = Id
          
# Sent by client to signal they do not want a specific job
class DecJob:
     requestType = 4
     messageId = 0

     def __init__(self, Id):
          self.messageId = Id

# Sent by server to confirm job completed
class AckMesg:
     requestType = 5
     messageId = 0

     def __init__(self, mesgId):
          self.messageId = mesgId

# Sent by client when job is finished
class JobComp:
     requestType = 6
     jobNumber = 0
     jobResult = ''
    # job = None
     messageId = 0

     def __init__(self, jobN, jobR, mesgId):
          self.jobNumber = jobN
          self.jobResult = jobR
          #self.job = job
          self.messageId = mesgId


# Sent by server when no jobs are available
class JobFull:
     requestType = 7
