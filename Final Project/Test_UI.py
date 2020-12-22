import tkinter as tk
import CreatorClass
import SeekerClass
import threading
import time
import os
import platform

class Menu(tk.Frame):
     def __init__(self, master = None):
          super().__init__(master)
          self.master = master
          self.pack()
          self.create_widgets()

     # Creates the UI to allow the User to select which jobs to use and how many JobSeekers to create
     def create_widgets(self):
          self.one_to_one_label = tk.Label(self, text = "One to One Jobs")

          self.one_to_one_jobs = tk.Listbox(self, height = 5, selectmode = tk.MULTIPLE, exportselection = False)
          self.one_to_one_jobs.insert(0, 'Check if online')
          self.one_to_one_jobs.insert(1, 'Live IP addresses')
          self.one_to_one_jobs.insert(2, 'Status of port')
          self.one_to_one_jobs.insert(3, 'Trace Route')
          self.one_to_one_jobs.insert(4, 'Spy on Neighbours')

          self.one_to_many_label = tk.Label(self, text = "One to Many Jobs")
          self.one_to_many_jobs = tk.Listbox(self, height = 5,selectmode = tk.MULTIPLE, exportselection = False)
          self.one_to_many_jobs.insert(0, 'ICMP Flood')
          self.one_to_many_jobs.insert(1, 'TCP Flood')
          
          self.divider = tk.Frame(self)

          self.seekers = tk.Scale(self.divider, orient = tk.HORIZONTAL, from_ = 1, to = 6, label = "# of Jobseekers")

          self.create = tk.Button(self.divider, text = "Create test", command = self.create_test)
          self.quit = tk.Button(self.divider, text = "QUIT", fg = "red", command = self.stop_application)

          self.one_to_one_label.grid(column = 1, row = 1, padx = 20, pady = 10)
          self.one_to_one_jobs.grid(column = 1, row = 2,padx = 20, pady = 10)
          self.one_to_many_label.grid(column = 2, row = 1,padx = 20, pady = 10)
          self.one_to_many_jobs.grid(column = 2, row = 2,padx = 20, pady = 10)
          self.divider.grid(column = 1, row = 3, columnspan = 2)
          self.seekers.pack(padx = 20, pady = 10)
          self.create.pack(padx = 20, pady = 10)
          self.quit.pack(padx = 20, pady = 10)
     
     # Destroys the UI
     def stop_application(self):
          self.master.destroy()
     
     # Reads the selected Jobs, modifies their values to fit the values used by JobCreator 
     # and returns the array of jobs
     def add_jobs(self):
          one_jobs = list(self.one_to_one_jobs.curselection())
          for  i in range(0,len(one_jobs)):
               if(one_jobs[i] == 2):
                    one_jobs[i] = 4 
               elif(one_jobs[i] == 3 or one_jobs[i] == 4):
                    one_jobs[i] += 2
          many_jobs = list(self.one_to_many_jobs.curselection())
          for i in range(0, len(many_jobs)):
               many_jobs[i] += 2
          all_jobs = one_jobs + many_jobs
          return all_jobs

     # Creates thread to handle the creation of JobCreators and JobSeekers
     # A small pause is made between threads so the previous one is able to 
     # finish manipulating files
     def create_test(self):
          selected_jobs = self.add_jobs()
          if(selected_jobs == []):
               selected_jobs = [0,1,2,3,4]
          creator_thread = threading.Thread(target = self.create_job_creator,args=[selected_jobs])
          creator_thread.start()
          #Sleep to allow for Creator to create files
          time.sleep(1) 
          for i in range(0,self.seekers.get()):
               seeker_thread = threading.Thread(target = self.create_job_seeker)
               seeker_thread.start()
               #Sleep to allow for Seeker to create files
               time.sleep(0.5) 

          self.stop_application()

     # Creates a new JobCreator
     def create_job_creator(self, jobs):
          jobC = CreatorClass.JobCreator(jobs)

     # Creates a new JobSeeker
     def create_job_seeker(self):
          jobS = SeekerClass.JobSeeker()

if __name__ == '__main__':
     root = tk.Tk()
     app = Menu(master = root)
     root.mainloop()
