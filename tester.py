import genetic 
from random import randint,choice,uniform

#x = genetic.GeneticParallelAlgorithmTest(3, 10 , 10 , 0.05, 10, 3, 0.5, 15 ,1)
#print(x)

#numPopulation, populationSize, numGenerations, pMutation , tournamentSize, numSurvivos, pMigrationPoblation, pMigration )
def GenerateNewInv():
    indv = []
    numPopulation = randint(1, 10)
    populationSize = randint(1, 10)
    numGenerations = randint(1, 10)
    pMutation = uniform(0, 0.01)
    numSurvivos = randint(1, 10)
    tournamentSize = randint(numSurvivos, 10)
    pMigrationPoblation = uniform(0, 0.15)
    pMigration = uniform(0, 0.05)
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
    inv2 = poblation[fitnessList.index(max(fitnessList))]
    del poblation[fitnessList.index(max(fitnessList))]
    del fitnessList[fitnessList.index(max(fitnessList))]
    return [inv1, inv2]


def GeneticSimpleAlgorithm(  numGenerations, sizePoblation, pMutation):
    poblation = GeneratePoblation(sizePoblation)
    fitnessList = Evaluate( poblation )
    for i in range(0, numGenerations):
        newPoblation = []
        chosenFathers = Selection( poblation, fitnessList)
        son, daughter = CrossOVer( chosenFathers[0], chosenFathers[1])
        son, daughter = Mutation( son, daughter, pMutation)
        newPoblation.extend((son,daughter))
        newPoblation = GeneratePoblation( sizePoblation, newPoblation)
        poblation = newPoblation.copy()
        fitnessList = Evaluate(poblation )
    solution = poblation[fitnessList.index(max(fitnessList))]
    return [solution, max(fitnessList)]

GeneticSimpleAlgorithm( 20 , 5, 0.015)
#Evaluate( [[1,2],[3,4],[5,6]])