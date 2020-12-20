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

          self.seekers = tk.Scale(self.divider, orient = tk.HORIZONTAL, from_ = 1, to = 10, label = "# of Jobseekers")

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

     def stop_application(self):
          self.master.destroy()

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

     def create_test(self):
          selected_jobs = self.add_jobs()
          if(selected_jobs == []):
               selected_jobs = [0,1,2,3,4]
          creator_thread = threading.Thread(target = self.create_job_creator,args=[selected_jobs])
          creator_thread.start()
          for i in range(0,self.seekers.get()):
               seeker_thread = threading.Thread(target = self.create_job_seeker)
               seeker_thread.start()
          self.stop_application()

     # Work on sending jobs to the job creator
     def create_job_creator(self, jobs):
          jobC = CreatorClass.JobCreator(jobs)

     def create_job_seeker(self):
          jobS = SeekerClass.JobSeeker()


if __name__ == '__main__':
     root = tk.Tk()
     app = Menu(master = root)
     root.mainloop()
