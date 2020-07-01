import numpy as np
import sys
from random import shuffle

# Initialize Variables

numberofqueens = 8
score = 28
mutation_rate = 0.1
mutate_flag = True
maximum_iterations = 100000

#Define Individual Attributes

class Attributes:
	def __init__(self):
		self.sequence = None
		self.fitness = None
		self.survival = None
	def setSequence(self, val):
		self.sequence = val
	def setFitness(self, fitness):
		self.fitness = fitness
	def setSurvival(self, val):
		self.survival = val


# Fitness Function- Evaluate row, column and diagonal clashes
        
def Fitness(chromosome = None):
# Row Clashes
	clashes = 0;
	row_col_clashes = abs(len(chromosome) - len(np.unique(chromosome)))
	clashes += row_col_clashes
# Diagonal Clashes
	for i in range(len(chromosome)):
		for j in range(i,len(chromosome)):
			if ( i != j):
				dx = abs(i-j)
				dy = abs(chromosome[i] - chromosome[j])
				if(dx == dy):
					clashes += 1
	return 28-clashes

# Generate Individual Sequence
    
def CreateChromosome():
	global numberofqueens
	init_distribution=list(range(numberofqueens))
	shuffle(init_distribution)
	return init_distribution

# Generate a Population of Individuals
    
def CreateInitialPopulation(self,population_size = 100):
	pop=[]
	population = [Attributes() for i in range(population_size)]
	for i in range(population_size):
		p=CreateChromosome()
		pop.append(p)
		population[i].setSequence(p)
		population[i].setFitness(Fitness(population[i].sequence))		
	return population

# Generate 2 Parents for Crossover
    
def CreateParent():
	globals()	
	parent1, parent2 = None, None
	summation_fitness = np.sum([x.fitness for x in population])
	lenp=len(population)	
	for each in population:
		each.survival = each.fitness/(summation_fitness*1.0)
		parent1_random = np.random.randint(lenp)
		parent2_random = np.random.randint(lenp)
		parent1=population[parent1_random]
		parent2=population[parent2_random]
	if parent1 is not None and parent2 is not None:
		return parent1, parent2
	else:
		sys.exit(-1)

# Create one child through crossover
        
def Crossover(parent1, parent2):
	globals()
	n = len(parent1.sequence)
	b = np.random.randint(n, size=1)
	c = b[0]
	child = Attributes()
	child.sequence = []	
	child.sequence.extend(parent1.sequence[0:c])
	for i in parent2.sequence[c:]:
		if i in child.sequence:
			continue
		child.sequence.append(i)
	for j in range(n):
		if j in child.sequence:
			continue
		child.sequence.append(j)		
	child.setFitness(Fitness(child.sequence))
	return child

#  Random Mutation
    
def Mutate(child):
	if child.survival:	    
		if child.survival < mutation_rate:
			child.sequence=np.random.shuffle(child.sequence)
			#print("mutate child {}".format(child.sequence))
	return child

# Iterate over existing population to produce new population(children)
    
def Iterate(counter):
	print (" #"*10 ,"Executing Genetic  generation : ", counter , " #"*10)
	globals()
	newpopulation = []
	pop =[]
	for i in range(len(population)):
		parent1, parent2 = CreateParent()
		child = Crossover(parent1, parent2)
		cnt=0
		while child.sequence in pop:
			child = Crossover(parent2, parent1)
			cnt+=1
			if cnt > 10 and cnt < 20:
				child = Crossover(parent1, parent2)
			if cnt >= 20 and cnt <=100:
				shuffle(child.sequence)
			if cnt > 100:
				break;
		pop.append(child.sequence)
		if(mutate_flag):
			child = Mutate(child)
		newpopulation.append(child)
	return newpopulation

# Stop if the desired N-Queen sequence is acheived
    
def CorrectSequence():
	globals()
	fitnessvals = [pos.fitness for pos in population]
	if score in fitnessvals:
		return True
	if maximum_iterations == counter:
		return True
	return False

# Main Function
    
population = CreateInitialPopulation(100)
counter = 0
while not CorrectSequence():
	population = Iterate(counter)
	print("population count:{}".format(len(population)))
	counter +=1 

print ("Iteration number : {}".format(counter)) 
for individual in population:
	if individual.fitness == 28:
		print (individual.sequence)
		break