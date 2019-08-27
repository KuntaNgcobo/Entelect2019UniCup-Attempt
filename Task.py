import numpy as np

class Task:
	def __init__(self, type_, shifts):
		self.type_job = type_
		self.shifts = np.array(shifts)

	def day_shifts(self, day):
		return self.shifts[day*3: (day+1)*3]

	def total_cost(self, shifts):
		temp = 0
		for cost in shifts:
			temp += cost
		return temp

