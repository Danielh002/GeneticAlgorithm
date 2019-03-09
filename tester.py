import genetic,time
from random import randint,choice,uniform

#x = genetic.GeneticParallelAlgorithmTest(3, 10 , 10 , 0.05, 10, 3, 0.5, 15 ,1)
#print(x)

#numPopulation, populationSize, numGenerations, pMutation , tournamentSize, numSurvivos, pMigrationPoblation, pMigration )
def GenerateNewInv():
    indv = []
    numPopulation = randint(1, 10)
    populationSize = randint(1, 100000)
    numGenerations = randint(10, 1000)
    pMutation = uniform(0.001, 0.05)
    tournamentSize = randint(1, populationSize)
    numSurvivos = randint(1, round(populationSize/2))
    pMigrationPoblation = randint(1, 5)
    pMigration = uniform(0.01, 0.5)
    indv = [ numPopulation, populationSize, numGenerations, pMutation, tournamentSize, numSurvivos, pMigrationPoblation, pMigration]
    return indv

def GeneratePoblation( sizePoblation , basePopulation = None ):
    poblation = []
    if basePopulation == None:
        for i in range(0, sizePoblation):
            poblation.append(GenerateNewInv())
    elif len(basePopulation) == sizePoblation:
            poblation = basePopulation 
    else:
        for i in range(0, (sizePoblation - len(basePopulation))):
            basePopulation.append(GenerateNewInv())
            poblation = basePopulation
    return poblation

def GenerateNewPoblation( poblation , fitnessList, newPoblation, sizePoblation ):
    while ( len(newPoblation) < sizePoblation):
        newPoblation.append( Selection(poblation, fitnessList))
    return newPoblation

def CrossOVer( mother, father):
    position = (randint(1, 7))
    firstMotherPart = mother[:position]
    secondMotherPart = mother[position:]
    firstfatherPart = father[:position]
    secondfatherPart = father[position:]
    firstMotherPart.extend(secondfatherPart)
    firstfatherPart.extend(secondMotherPart)
    return firstMotherPart, firstfatherPart

def Mutation( individual, individual2, mutationProbability ):
    luck = uniform(1,100)
    if( luck <= mutationProbability):
        whichGene = randint(0, 7)
        newIndividual = GenerateNewInv()
        individual[whichGene] = newIndividual[whichGene]
    luck = uniform(1,100)
    if( luck <= mutationProbability):
        whichGene = randint(0, 7)
        newIndividual = GenerateNewInv()
        individual2[whichGene] = newIndividual[whichGene]
    return individual,individual2

def Evaluate( poblation ):
    fitnessList = []
    for i in  poblation:
        fitnessList.append( genetic.GeneticParallelAlgorithmTest( i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], 1))
    return fitnessList

def Selection( poblation, fitnessList):
    inv1 = poblation[fitnessList.index(max(fitnessList))]
    del poblation[fitnessList.index(max(fitnessList))]
    del fitnessList[fitnessList.index(max(fitnessList))]
    return inv1


def GeneticSimpleAlgorithm(  numGenerations, sizePoblation, pMutation):
    startTime = time.time()
    poblation = GeneratePoblation(sizePoblation)
    fitnessList = Evaluate( poblation )
    for i in range(0, numGenerations):
        newPoblation = []
        for j in range(0, int(sizePoblation/2)):
            father = Selection( poblation, fitnessList)
            mother = Selection( poblation, fitnessList)
            son, daughter = CrossOVer( father, mother)
            son, daughter = Mutation( son, daughter, pMutation) 
            newPoblation.extend((son,daughter))
            newPoblation = GenerateNewPoblation( poblation, fitnessList, newPoblation, sizePoblation)   
        poblation = newPoblation.copy()
        fitnessList = Evaluate(poblation )
        print(numGenerations-i, " Generaciones restantes" )
    solution = poblation[fitnessList.index(max(fitnessList))]
    print("--- Tiempo ejercucion tester: %s  ---" % (time.time() - startTime))
    return [solution, max(fitnessList)]

print(GeneticSimpleAlgorithm( 100 , 20, 0.015))
#Evaluate( [[1,2],[3,4],[5,6]])