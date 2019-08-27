import Task
import Worms
import numpy as np

# File Input Start

file_input = open("map_2.input",'r')
line = file_input.readline().strip("\n").split(",")
worker_count = {"B":eval(line[0]),"M":eval(line[1]),"S":eval(line[2]),"X":eval(line[3])}
specialities = np.array([["B", "D"],["M", "R"],["S", "R"],["X", "A"]])


# File Input End

# Upload Workers Start

workers = []
counter = 0
for worker_num in line:
	tw = specialities[counter]
	for i in range(eval(worker_num)):
		workers.append(Worms.Worm(tw[0], tw[1]))
	counter += 1

 #worms = np.array(workers)

# Upload Workers End

# Upload Tasks start

total_tasks = []

for i in file_input:
	row = i.strip("\n").split(",")
	shs = []
	for i in range(1, len(row)):
		shs.append(eval(row[i]))
	shift = Task.Task(row[0],shs)
	total_tasks.append(shift)

 #total_tasks = np.array(total_tasks)

# Upload Tasks end

# Constants

max_shifts = len(total_tasks[0].shifts)
max_days = max_shifts/3
current_day = -1 # Means it has started

# Constants


######### Functions ###############

def check_weekend_need(aWorm):
    temp = 0 # shifts free back to back
    length = len(aWorm.worked_schedule)
    if(length < 15):
        return False

    for shift in aWorm.worked_schedule[length - 15:length]:
        if(shift == "F"):
            temp += 1
        else:
            temp = 0

        if(temp >= 3):
            return True

    return False

def check_consec_shifts(aWorm):
	length = len(aWorm.worked_schedule)
	if(length < 3):
		return False


	for i in range(length-2, length):
		if(aWorm.worked_schedule[i] == "F"):
			return False

	return True

def check_to_resign(aWorm): # checks if worms should retire
    temp = 0 #numbers of back
    length = len(aWorm.worked_schedule)
    if(aWorm.motivation > 42):
        aWorm.employed = False
        return True

    if(length >= 15 and aWorm.employed):
        return False

    for shift in aWorm.worked_schedule[length - 15:length]:
        if(shift == "F"):
            temp += 1
        else:
            temp = 0

        if(temp < 3):
           return False

    aWorm.employed = False 
    return True

def check_night_shift(aWorm):
 	if(aWorm.consective_night_shifts > 5):
 		return True
 	return False




######### Functions ###############

DJ = []
RJ = []
PJ = []
AJ = []

for i in range(max_shifts):
	if(i%3 == 0):
		current_day += 1
	DJ = total_tasks[0].day_shifts(current_day)
	RJ = total_tasks[1].day_shifts(current_day)
	PJ = total_tasks[2].day_shifts(current_day)
	AJ = total_tasks[3].day_shifts(current_day)
		#print(RJ)
	for worm in workers:
		sp = worm.speciality_task
		time = ""

		if(i%3 == 0):
			time = "M"
		elif(i%3 == 1):
			time = "Af"
		else:
			time == "E"


		if( check_to_resign(worm) ):
			worm.motivation += 1
			worm.work_shift("F", time)
			continue

		if( check_consec_shifts(worm) ):
			worm.motivation += 1
			worm.work_shift("F", time)
			continue

		if(check_weekend_need(worm)):
			worm.weekend += 1
			worm.motivation += 1
			worm.work_shift("F", time)
			continue
		elif(worm.weekend > 3):
			worm.work_shift("F", time)
			worm.weekend = 0
		
		if(check_night_shift(worm) and i%3 == 2):
			worm.motivation += 1
			worm.work_shift(sp, time)
			continue

		
		if(worm.speciality_task == "D"):
			if( DJ[0]) > 0:
				DJ[0] =  DJ[0] - 1 
			elif( DJ[1]) > 0:
				DJ[1] =  DJ[1] - 1 
			elif( DJ[2]) > 0:
				DJ[2] =  DJ[2] - 1 

			worm.motivation -= 1
		elif(worm.speciality_task == "R"):
			if( RJ[0]) > 0:
				RJ[0] = RJ[0] - 1 
			elif( RJ[1]) > 0:
				RJ[1] =  RJ[1] - 1 
			elif( RJ[2]) > 0:
				RJ[2] =  RJ[2] - 1 

			worm.motivation -= 1
		elif(worm.speciality_task == "P"):
			if( PJ[0]) > 0:
				PJ[0] =  PJ[0] - 1 
			elif( PJ[1]) > 0:
				PJ[1] =  PJ[1] - 1 
			elif( PJ[2]) > 0:
				PJ[2] =  PJ[2] - 1 

			worm.motivation -= 1
		elif(worm.speciality_task == "A"):
			if( AJ[0]) > 0:
				AJ[0] =  AJ[0] - 1 
			elif( AJ[1]) > 0:
				AJ[1] =  AJ[1] - 1 
			elif( AJ[2]) > 0:
				AJ[2] =  DJ[2] - 1 

			worm.motivation -= 1
		worm.work_shift(sp, time)

	
	for worm in workers:
		if(DJ[i%3] != 0 and i != max_shifts - 1 and worm.type_worker == "D"):
			worm.worked_schedule[i+1] += DJ[i%3]

		if(AJ[i%3] != 0 and i != max_shifts - 1 and worm.type_worker == "A"):
			worm.worked_schedule[i+1] += AJ[i%3]

		if(RJ[i%3] != 0 and i != max_shifts - 1 and worm.type_worker == "R"):
			worm.worked_schedule[i+1] += RJ[i%3]

		if(PJ[i%3] != 0 and i != max_shifts - 1 and worm.type_worker == "P"):
			worm.worked_schedule[i+1] += PJ[i%3]


for worm in workers:
	worm.display_work_schedule()

