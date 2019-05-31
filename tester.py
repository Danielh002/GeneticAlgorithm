import genetic,time
from random import randint,choice,uniform

#x = genetic.GeneticParallelAlgorithmTest(3, 10 , 10 , 0.05, 10, 3, 0.5, 15 ,1)
#print(x)

#numPopulation, populationSize, numGenerations, pMutation , tournamentSize, numSurvivos, pMigrationPoblation, pMigration )
def GenerateNewInv():
    indv = []
    numPopulation = randint(1, 5)
    populationSize = randint(10, 1000)
    numGenerations = randint(10, 100)
    pMutation = round(uniform(0.001, 0.05), 3)
    tournamentSize = randint(1, populationSize)
    numSurvivos = randint(1, round(tournamentSize/2))
    pMigrationPoblation = randint(1, 5)
    pMigration = round(uniform(0.01, 0.5),3)
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
        if( len(newPoblation) < sizePoblation/2):
            newPoblation.append( Selection(poblation, fitnessList))
        else:
            newPoblation.append(GenerateNewInv())
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
        #fitnessList.append(1)
        fitnessList.append( genetic.GeneticParallelAlgorithmTest( i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], 1))
    return fitnessList

def Selection( poblation, fitnessList):
    inv1 = poblation[fitnessList.index(max(fitnessList))]
    del poblation[fitnessList.index(max(fitnessList))]
    del fitnessList[fitnessList.index(max(fitnessList))]
    return inv1

def GeneticSimpleAlgorithm(  numGenerations, sizePoblation, pMutation):
    numPoblation = 0
    print("Inician pruebas")
    startTime = time.time()
    poblation = GeneratePoblation(sizePoblation)
    print("Poblaciones iniciales")
    for i in poblation:
        print("Poblacion: ", i)
    fitnessList = Evaluate( poblation)
    for i in range(0, numGenerations):
        print("Generacion #: ", i+1)
        newPoblation = []
        for j in range(0, int(sizePoblation/4)):
            father = Selection( poblation, fitnessList)
            mother = Selection( poblation, fitnessList)
            son, daughter = CrossOVer( father, mother)
            son, daughter = Mutation( son, daughter, pMutation) 
            newPoblation.extend((son,daughter))
        newPoblation = GenerateNewPoblation( poblation, fitnessList, newPoblation, sizePoblation)
        poblation = newPoblation.copy()  
        print("Poblaciones nuevas")
        for i in poblation:
            print("Poblacion : ", i)
        fitnessList = Evaluate(poblation)
        print("Poblaciones Evaluadas")
        while ( numPoblation< len(poblation)):
            print("Poblacion : ", poblation[numPoblation], "Valor Aptitud : ", fitnessList[numPoblation])
            numPoblation+=1
        print("Mejor individuo de la poblacion: ")
        print(poblation[fitnessList.index(max(fitnessList))], max(fitnessList) )
    solution = poblation[fitnessList.index(max(fitnessList))]
    print("--- Tiempo ejercucion tester: %s  ---" % (time.time() - startTime))
    return [solution, max(fitnessList)]

print(GeneticSimpleAlgorithm( 20 , 10, 0.015))
#Evaluate( [[1,2],[3,4],[5,6]])
