
#Chromosome class
#CHROMOSOME = [(c1, d1), (c2, d2), ..., (c_k-1, d_k-1), t_max]

import random as rnd


class Chromosome:



	def __init__(self, k, alpha, points=[], deltas=[], fitness=0):
		self.points = points
		self.deltas = deltas
		self.alpha = alpha
		self.fitness = fitness
		self.k = k
		self.chromosome = [] 


	#return the intervals from chromosome partition
	def get_intervals(self):

		k = self.k
		intervals = [(1, self.points[0] + self.deltas[0] - 1)]

		i = 1
		while i < k - 1: 

			c = self.points[i]
			d = self.deltas[i]
			intervals.append((self.points[i-1], c + d - 1))
			i += 1

		intervals.append((self.points[k - 2], self.points[k - 1]))

		return intervals


	#overlaps constrain 1
	def delta_max1(self, diff, alpha):

		delta = diff * alpha / (1 - alpha)

		return int(delta)


	#overlaps constrain 2
	def delta_max2(self, i, alpha):

		delta = alpha * i

		return int(delta)


	#max overlap accepted
	def max_delta(self, d1, d2, alpha):

		delta1 = self.delta_max1(d1, alpha)
		delta2 = self.delta_max2(d2, alpha)

		delta_max = min(delta1, delta2)

		return delta_max


	#check if overlaps respect the constrains
	def check_overlaps(self):

		p1 = self.get_points()
		d1 = self.get_deltas()

		i = len(p1) - 2

		while i >= 0:

			if i == len(p1) - 2:
				x1 = p1[i] - p1[i-1]
				I = p1[i+1] - p1[i]

			elif i == 0:
				x1 = p1[i] - 1
				I = p1[i+1] - p1[i] + d1[i+1]

			else:
				x1 = p1[i] - p1[i-1]
				I = p1[i+1] - p1[i] + d1[i+1]

			new_d = self.max_delta(x1, I, self.alpha)

			if d1[i] > new_d:
				d1[i] = new_d

			i -= 1

		self.set_deltas(d1)


	#create new overlaps 
	def create_overlaps(self):

		p1 = self.get_points()
		d1 = [0 for i in range(len(p1) - 1)]

		i = len(p1) - 2

		while i >= 0:

			if i == len(p1) - 2:
				x1 = p1[i] - p1[i-1]
				I = p1[i+1] - p1[i]

			elif i == 0:
				x1 = p1[i] - 1
				I = p1[i+1] - p1[i] + d1[i+1]

			else:
				x1 = p1[i] - p1[i-1]
				I = p1[i+1] - p1[i] + d1[i+1]

			new_d = self.max_delta(x1, I, self.alpha)

			d1[i] = rnd.randint(0, new_d)

			i -= 1

		self.set_deltas(d1)


	#set a random value of delta in an interval
	def set_random_delta(self, i):

		p1 = self.get_points()
		d1 = self.get_deltas()

		if i == self.k - 2:
			x1 = p1[i] - p1[i-1]
			I = p1[i+1] - p1[i]
		elif i == 0:
			x1 = p1[i] - 1
			I = p1[i+1] - p1[i] + d1[i+1]
		else:
			x1 = p1[i] - p1[i-1]
			I = p1[i+1] - p1[i] + d1[i+1]

		delta_max = self.max_delta(x1, I, self.alpha)
		new_delta = rnd.randint(0, delta_max)

		self.set_delta(new_delta, i)



	def get_k(self):

		return self.k



	def get_point(self, index):

		return self.points[index]



	def set_point(self, new_point, index):

		self.points[index] = new_point



	def get_points(self):

		return self.points



	def set_points(self, new_points):

		for i in range(len(new_points)):
			self.set_point(new_points[i], i)



	def set_points(self, new_points):

		self.points = new_points

		if len(new_points) != len(self.points):
			raise ValueError('New points have different dimension.')



	def get_deltas(self):

		return self.deltas



	def set_delta(self, new_delta, interval):

		self.deltas[interval] = new_delta



	def set_deltas(self, new_deltas):

		self.deltas = new_deltas



	def get_fitness(self):

		return self.fitness



	def set_fitness(self, new_fit):

		self.fitness = new_fit



	def get_chromosome(self):

		c = []

		for i in range(len(self.deltas)):
			c.append((self.points[i], self.deltas[i]))

		c.append(self.points[-1])

		return c
