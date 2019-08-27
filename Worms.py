import numpy as np
import scipy as sp

class Worm:
    def __init__(self, type_worker, speciality_task):
        self.motivation = 15
        self.type_worker = type_worker
        self.speciality_task = speciality_task
        self.weekend = 0
        self.onWeekend = False
        self.employed = True # Shows employment status - False means retired
        self.consective_shifts = 0
        self.consective_days = 0
        self.consective_night_shifts = 0
        self.worked_schedule = []
        self.prevNight = False
    	

    def display_work_schedule(self):
        temp = "" + self.type_worker
        for shift in self.worked_schedule:
            temp += " " +str(shift)
        print(temp)

    def work_shift(self, type_job, time):
        if(time == "E" and type_job!="F"):
            self.consective_night_shifts += 1
            self.prevNight = True
        elif(time == "E" and type_job=="F"):
            self.consective_night_shifts = 0
            self.prevNight = False

        self.worked_schedule.append(type_job)
        return np.array(self.worked_schedule)

    







    