#GENETIC ALGORITHM FOR FINDING K--DENSEST-OVERLAPPING-EPISODES

#CHROMOSOME = [(c1, d1), (c2, d2), ..., (c_k-1, d_k-1), t_max]
#INPUT = G=(V,T,E), k, alpha
#OUTPUT = P = set of overlapping episodes

import random as rnd
import chromosome as chromo
import networkx as nx
import time
from read_file import students_dataset, facebook_dataset, enron_dataset, twitter_dataset
from charikar_heap import charikarHeap


#create a chromosome where intervals have same number of edges
def create_partitioned_chromosome(G, k, t_max, alpha):

	tot = n_edges(G)
	edges_per_interval = tot / k
	points = []
	count = 0

	for i in range(len(G) - 1):
		for el in G[i]:
			count += 1
		if count >= edges_per_interval:
			points.append(i)
			count = 0

	points.append(t_max)
	c = chromo.Chromosome(k, alpha, points)
	c.create_overlaps()

	return c


def n_edges(G):

	count = 0
	for el in G:
		count += len(G[el])

	return count


#create a chromosome where intervals have same dimensions
def create_equal_chromosome(k, t_max, alpha):

	I = t_max / k
	points = []
	i = 1
	k_counter = k

	while k_counter > 1:
		points.append(int(i * I) + 1)
		i += 1
		k_counter -= 1

	points.append(t_max)
	c = chromo.Chromosome(k, alpha, points)
	c.create_overlaps()

	return c


#create a chromosome where intervals are random
def create_random_chromosome(k, t_max, alpha):

	points = [t_max]

	i = 1
	while i < k:

		point = rnd.randint(1, t_max)

		if point not in points:
			points.append(point)
			i += 1

	c = chromo.Chromosome(k, alpha, sorted(points))
	c.create_overlaps()

	return c


#create a population of h chromosomes
def create_population(G, h, k, alpha, t_max):

	population = []

	population.append(create_partitioned_chromosome(G, k, t_max, alpha))
	population.append(create_equal_chromosome(k, t_max, alpha))

	for i in range(h-2): 
		population.append(create_random_chromosome(k, t_max, alpha))

	return population


#fitness function
def fitness_fun(chromosome, G):

	fit = 0
	densest_graph = []
	intervals = chromosome.get_intervals()

	for interval in intervals:

		edge_interval = get_edge_interval(G, interval)
		g = nx.Graph()
		g.add_edges_from(edge_interval)
		S, f = charikarHeap(g)
		fit += f
		densest_graph.append(S)

	chromosome.set_fitness(fit)

	return fit, densest_graph 


#calcule fitness value for each chromosome of population
def fitness(G, population):

	fitness = []
	densest_graph = []

	for el in population:

		fit, S = fitness_fun(el, G) 
		fitness.append(fit)
		densest_graph.append(S)

	return fitness, densest_graph


#get the edges in the given interval
def get_edge_interval(G, interval):

	edges = []
	start = interval[0]
	end = interval[1]
	i = start

	while i <= end:

		ts_edges = G[i-1] 
		for e in ts_edges:
			if e not in edges:
				edges.append(e)	
		i += 1

	return edges


#select the h/3 fittest chromosome of population
def elitist_selection(population, fitness):

	if len(population) != len(fitness):
		raise AttributeError('population and fitness vector must have same dimension')

	n_best = int(len(population)/3)

	if (len(population) - n_best) % 2 == 1:
		n_best += 1

	pop = population[:]
	best_pop = []
	best = 0

	for n in range(n_best):
		for el in pop:
			if el.get_fitness() > best:
				b = el
				best = el.get_fitness()
		best = 0
		best_pop.append(b)
		pop.remove(b)

	return best_pop


#mute randomly an interval of a chromosome
def mutation(chromosome, prob, alpha):
	
	for i in range(chromosome.get_k() - 1):

		p = rnd.random()
		
		if p < prob:
			
			if i == 0:
				if chromosome.get_point(i) == 1:
					new_point = 1
				else:
					new_point = rnd.randint(1, chromosome.get_point(i+1) - 1)
			else:
				new_point = rnd.randint(chromosome.get_point(i-1) + 1, chromosome.get_point(i+1) - 1)

			chromosome.set_point(new_point, i)
			chromosome.set_random_delta(i)

	chromosome.check_overlaps()

	return chromosome


#roulette selection of 2 chromosome of population
def roulette_selection(fitness):

	roulette = make_roulette(fitness)
	parents = []

	while len(parents) < 2:
		parent = select(roulette)

		if parent not in parents:
			parents.append(parent)

	return parents



def make_roulette(fitness):

	tot_fitness = sum(fitness)
	prob_counter = 0
	roulette = []

	for fit in fitness:
		chromo_prob = fit / tot_fitness
		prob_counter += chromo_prob
		roulette.append(prob_counter)

	return roulette



def select(roulette):

	n = rnd.random()
	i = 0
	while n > roulette[i]:
		i += 1

	return i


#crossover of 2 selected chromosome 
def crossover(population, fitness, alpha):

	p_index1, p_index2 = roulette_selection(fitness)
	parent1 = population[p_index1]
	parent2 = population[p_index2]

	points1 = parent1.get_points()
	points2 = parent2.get_points()

	deltas1 = parent1.get_deltas()
	deltas2 = parent2.get_deltas()
	
	p1_dict = create_dict(points1, deltas1)
	p2_dict = create_dict(points2, deltas2)


	k = len(points1)
	if k < 3:
		p = 1
	else:
		p = rnd.randint(1, k-2)

	p1 = list(set(points1[0:p] + points2[p:]))
	p2 = list(set(points2[0:p] + points1[p:]))

	while len(p1) != len(points1):
		new_point = rnd.randint(1, points1[-1] - 1)
		if new_point not in p1:
			p1.append(new_point)

	while len(p2) != len(points2):
		new_point = rnd.randint(1, points2[-1] - 1)
		if new_point not in p2:
			p2.append(new_point)

	p1.sort()
	p2.sort()

	d1 = []
	for el in p1[:-1]:
		if el not in p1_dict:
			if el not in p2_dict:
				delta = rnd.randint(1000,10000)
				d1.append(delta)
			else:
				d1.append(p2_dict[el])
		else:
			d1.append(p1_dict[el])

	d2 = []
	for el in p2[:-1]:
		if el not in p1_dict:
			if el not in p2_dict:
				delta = rnd.randint(1000,10000)
				d2.append(delta)
			else:
				d2.append(p2_dict[el])
		else:
			d2.append(p1_dict[el])

	s1 = chromo.Chromosome(k, alpha, p1, d1)
	s2 = chromo.Chromosome(k, alpha, p2, d2)
	s1.check_overlaps()
	s2.check_overlaps()

	return s1, s2


def create_dict(points, deltas):

	p_dict = {}

	for i in range(len(points)):
		if i < len(points) - 1:
			if points[i] not in p_dict:
				p_dict[points[i]] = deltas[i]

	return p_dict


def print_population(pop):

	print('Population:')
	for el in pop:
		print(el.get_chromosome(), '-->', el.get_fitness())


#offspring of population
def iteration(G, population, fit, alpha):

	h = len(population)
	k = population[0].get_k()
	new_pop = []

	elite = elitist_selection(population, fit)
	n_elite = len(elite)

	for el in elite:
		new_pop.append(el)

	while len(new_pop) < h:
		s1, s2 = crossover(population, fit, alpha)
		new_pop.append(s1)
		new_pop.append(s2)

	for el in new_pop[1:]: 
		el = mutation(el, 1/(k-1), alpha)

	fit, S = fitness(G, new_pop)

	return new_pop, fit, S


#genetic algorithm
def genetic_algo(G, n_population, n_generation, k, alpha, t_max):

	print('Start computing...')
	print()

	start = time.time()
	population = create_population(G, n_population, k, alpha, t_max)
	fit, S = fitness(G, population)

	print('GENERATION: 1')
	f = sum(fit)

	#print_population(population)

	print('Fitness: %f' %f)
	fittest = max(fit)
	index = fit.index(fittest)
	print('Fittest: %f' %fittest)

	print()
	diff = 0

	for g in range(n_generation - 1):

		population, fit, S = iteration(G, population, fit, alpha) 

		print('GENERATION:',g+2)
		#print_population(population)
		print('Fitness: %f' %sum(fit))

		gen_fittest = max(fit)
		print('Fittest: %f' %gen_fittest)
		diff += gen_fittest - fittest

		if gen_fittest > fittest:
			fittest = gen_fittest
			index = fit.index(fittest)
	
		f = sum(fit)
		print()

	print('End of computation...\n')

	total_time = time.time() - start

	best_chromo = population[index]

	if n_generation > 1:
		print('Total difference [ from Gen 1 to Gen', g+2,']: ', diff)
	
	return population, fittest, total_time, best_chromo



#start test of genetic algorithm
def start(dataset, h, g, k, alpha, students_t_max):

	final_pop, final_fit, total_time, best_chromo = genetic_algo(dataset, h, g, k, alpha, students_t_max)

	print('Fittest: %f' %final_fit)
	print('Finished in %f seconds' %total_time)
	print('Best chromosome: ')
	print(best_chromo.get_chromosome())




if __name__ == '__main__':

	k = 5
	alpha = 0.2
	h = 10
	g = 10

	#TS = facebook_dataset()
	#TS = enron_dataset()
	#TS = twitter_dataset()
	TS = students_dataset()

	t_max = list(TS.keys())[-1] + 1
	print()

	start(TS, h, g, k, alpha, t_max)
	
