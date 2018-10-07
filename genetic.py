from random import randint,choice,uniform
import threading
import time
import math

PolyCali = [
        [-76.5647898,3.3697588],
        [-76.5619907,3.3650495],
        [-76.5370137,3.2942727],
        [-76.5158135,3.2897311],
        [-76.5133244,3.3390015],
        [-76.5021665,3.3544243],
        [-76.5083033,3.3682836],
        [-76.5083462,3.3925533],
        [-76.4824946,3.4126011],
        [-76.4667706,3.4007754],
        [-76.4541531,3.4417283],
        [-76.4749668,3.4611769],
        [-76.4810186,3.4980172],
        [-76.4918332,3.503843],
        [-76.5053944,3.4948476],
        [-76.5218312,3.499388],
        [-76.5362519,3.4922121],
        [-76.5303728,3.4790078],
        [-76.533699,3.4673937],
        [-76.5383985,3.4573646],
        [-76.5484621,3.4621515],
        [-76.5591266,3.463597],
        [-76.5867642,3.4635745],
        [-76.5718292,3.4519978],
        [-76.5531181,3.4477888],
        [-76.5489554,3.4398103],
        [-76.5672801,3.4148679],
        [-76.5759274,3.410643],
        [-76.5670223,3.3991354],
        [-76.5616578,3.4087477],
        [-76.5550916,3.4132192],
        [-76.5562501,3.3905466],
        [-76.5647898,3.3697588]
    ]
genomeSize = 2


def Seed():
    while True:
        coordX = uniform(3.2896921, 3.5033777)
        coordY = uniform(-76.592577, -76.451471)
        if( InsideCity( coordX, coordY)):
            return [coordY, coordX]

def Poblation( sizePoblation , basePopulation = None ):
    poblation = []
    if basePopulation == None:
        for i in range(0, sizePoblation):
            poblation.append(Seed())
    else:
        for i in range(0, (sizePoblation - len(basePopulation))):
            basePopulation.append(Seed())
            poblation = basePopulation
    return poblation

def InsideCity(y,x, poly = PolyCali):
    n = len(poly)
    inside = False
    p2x = 0.0
    p2y = 0.0
    xints = 0.0
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside

def CrossOVer( mother, father):
    position = (randint(1, genomeSize-1))
    firstMotherPart = mother[:position]
    secondMotherPart = mother[position:]
    firstfatherPart = father[:position]
    secondfatherPart = father[position:]
    firstMotherPart.extend(secondfatherPart)
    firstfatherPart.extend(secondMotherPart)
    return firstMotherPart, firstfatherPart

def Mutation( individual, mutationProbability ):
    luck = randint(1,100)
    if( luck <= mutationProbability):
        whichGene = randint(0, genomeSize-1)
        newIndividual = Seed()
        individual[whichGene] = newIndividual[whichGene]
    return individual

def TournamentSelection( population , tournamentSize, numSurvivors):
    competitors = []
    survivors = []
    for i in range(0, numSurvivors):
        for i in range(0,tournamentSize):
            competitors.append(choice(population))
        biggestValue = 0
        indv = None
        for i in competitors:            
            if (i[genomeSize] > biggestValue):
                biggestValue = i[genomeSize]
                indv = i
        survivors.append(indv[:genomeSize])
    return survivors

def Fitness( indivdual ):
    return individual.append(uniform(0, 100))

def FitnessEvaluate (poblation):
    for individual in poblation:
         individual.append(uniform(0, 100))
    return poblation

def GeneticProcess( populationWithFitness , pMutation, populationSize, tournamentSize, numSurvivos):
    parent = TournamentSelection( populationWithFitness, tournamentSize, numSurvivos )
    children = []
    for i in range(0, int(len(parent)/2)):
        mother = parent.pop(0)
        father = parent.pop(0)
        Son, Daugther = CrossOVer( mother, father)
        children.append(Mutation(Son, pMutation))
        children.append(Mutation(Daugther, pMutation))
    populationWithFitness = FitnessEvaluate(Poblation( populationSize, children))

def GeneticParallelAlgorithm( numPopulation, populationSize,  pMutation , numGenerations, tournamentSize, numSurvivos):
    startTime = time.time()
    populations = []
    solution = None
    for i in range(0, numPopulation):
        populations.append( FitnessEvaluate(Poblation(populationSize)))
    threads = []
    while( numGenerations > 0 ):
        for i in range(0, numPopulation):
                threadPoblation = threading.Thread(name='Poblation#'+str(i+1) , target=GeneticProcess, args=( populations[i], pMutation, populationSize, tournamentSize, numSurvivos))
                threads.append(threadPoblation)
                threadPoblation.start()
        for i in threads:
            i.join()
        #Migration( populations, 5)
        numGenerations = numGenerations - 1
    populationInOne = []
    for i in populations:
        populationInOne.extend(i)
    solution = GetSolution( populationInOne, 100)
    print("--- %s seconds ---" % (time.time() - startTime))
    print(solution)
    return solution

def GetOnlyFitnessList( evaluatePoblation):
    simpleFitnessList = []
    for i in evaluatePoblation:
        simpleFitnessList.append(i[genomeSize])
    return simpleFitnessList

def RemovePorcentagePoblation( poblation, porcentage):
    i = 0
    numToRemove = math.ceil(len(poblation) * (porcentage/100))
    simpleFitnessList = GetOnlyFitnessList( poblation) 
    while ( i < numToRemove ):
        del poblation[ simpleFitnessList.index(min(simpleFitnessList))]
        i+=1

def CopyPorcentagePoblation( poblation, porcentage):
    i = 0
    numToRemove = math.ceil(len(poblation) * (porcentage/100))
    simpleFitnessList = GetOnlyFitnessList( poblation) 
    copyIndv = None
    while ( i < numToRemove ):
        copyIndv = poblation[ simpleFitnessList.index(max(simpleFitnessList))]
        i+=1
    return copyIndv

def GetSolution( poblation, porcentage):
    i = 0
    numToAdd = math.ceil(len(poblation) * (porcentage/100))
    simpleFitnessList = GetOnlyFitnessList( poblation) 
    solution = []
    while ( i < numToAdd):
        inv = poblation[ simpleFitnessList.index(max(simpleFitnessList))]
        solution.append(inv)
        i+=1
    return solution

def Migration( poblations, porcentage ):
    for i in range(0, len(poblations)-1):
        RemovePorcentagePoblation( poblations[i+1], porcentage)
        poblations[i+1].append( CopyPorcentagePoblation(poblations[i], porcentage))
    RemovePorcentagePoblation( poblations[0], porcentage)
    poblations[0].append( CopyPorcentagePoblation(poblations[-1], porcentage))

#GetSolution( [[1,2,3],[1,3,4],[1,3,5]], 100)
#Migration( [[[1,2,3],[1,3,4],[1,3,5]],[[2,2,7],[2,3,1],[2,3,9]],[[3,2,0],[3,3,20],[3,3,15]]], 33)
#RemovePorcentagePoblation( [[1,2,1],[3,2,1],[4,5,1],[6,7,1],[8,9,2],[9,8,3],[4,8,2],[9,5,11],[9,5,10],[10,5,15]], 1 )
#CopyPorcentagePoblation( [[1,2,1],[3,2,1],[4,5,1],[6,7,1],[8,9,2],[9,8,3],[4,8,2],[9,5,11],[9,5,10],[10,5,15]], 20 )   
GeneticParallelAlgorithm(3, 3 , 1, 50, 50, 10)
#print (TournamentSelection( [[[1,1],1.0], [[2,2],2.0], [[3,3],3.0],[[4,4],4.0]], 2 , 2))
#print (TournamentSelection( [[1,2,1],[3,2,1],[4,5,1],[6,7,1],[8,9,2],[9,8,3]], 2 , 2))
#print (Seed())
#Mutation(1)
#print (GeneticProcess( [[1,2],[3,2],[4,5],[6,7],[8,9],[9,8]], 1, 6, 5, 2))
#print (getOnlyFitnessList( [[1,2,4],[3,5,6],[7,8,9]]))

