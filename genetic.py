from random import randint,choice,uniform
import threading
import time
import math
import xlrd
import fitness
import statistics
import os

PolyCali = [
[-76.5678796,3.3688162],
[-76.564463,3.3653049],
[-76.5606173,3.3633358],
[-76.5507248,3.326448],
[-76.5356404,3.292559],
[-76.5144402,3.2880174],
[-76.4825112,3.315952],
[-76.4712675,3.3484264],
[-76.4705807,3.3745602],
[-76.4664703,3.3993616],
[-76.4675338,3.4030283],
[-76.4655932,3.406438],
[-76.4656602,3.4127433],
[-76.4630048,3.4153724],
[-76.4608697,3.4262853],
[-76.4615775,3.4353452],
[-76.4688945,3.4410857],
[-76.4729607,3.4404646],
[-76.4744519,3.4421567],
[-76.4755999,3.4441433],
[-76.4754175,3.4465154],
[-76.4749776,3.4485448],
[-76.4762973,3.4518166],
[-76.4777993,3.4613051],
[-76.4750527,3.4661886],
[-76.4764636,3.4701672],
[-76.4763725,3.4742742],
[-76.4787652,3.4779477],
[-76.4815656,3.4830669],
[-76.4852244,3.4960465],
[-76.4901596,3.4989701],
[-76.4949231,3.501808],
[-76.5040211,3.4931339],
[-76.5204579,3.4976743],
[-76.5392345,3.4905198],
[-76.5289995,3.4772941],
[-76.5323257,3.46568],
[-76.5370252,3.4556509],
[-76.5470887,3.4604378],
[-76.5577532,3.4618833],
[-76.5853908,3.4618608],
[-76.5704558,3.4502841],
[-76.5517447,3.4460751],
[-76.547582,3.4380966],
[-76.5659067,3.4131542],
[-76.574554,3.4089293],
[-76.5680092,3.400549],
[-76.5602844,3.407034],
[-76.5564648,3.4044798],
[-76.5631164,3.3863053],
[-76.5678796,3.3688162]]
genomeSize = 2
def Seed():
    while True:
        coordX = uniform(3.2896921, 3.5033777)
        coordY = uniform(-76.592577, -76.451471)
        if( InsideCity( coordX, coordY)):
            return [coordY, coordX]

def Selection( poblation, fitnessList):
    inv1 = poblation[fitnessList.index(max(fitnessList))]
    del poblation[fitnessList.index(max(fitnessList))]
    del fitnessList[fitnessList.index(max(fitnessList))]
    return inv1

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
        biggestValue = -99999999
        indv = None
        for i in competitors:            
            if (i[genomeSize] > biggestValue):
                biggestValue = i[genomeSize]
                indv = i
        survivors.append(indv[:genomeSize])
    return survivors

def LoadAListWithData( fileLocation ):
    wb = xlrd.open_workbook(fileLocation) 
    sheet = wb.sheet_by_index(0) 
    sheet.cell_value(0, 0)
    listWithData = []
    for i in range(1,sheet.nrows):
        singleRow = []
        if (type(sheet.cell_value(i, 1)) is str or type(sheet.cell_value(i, 2)) is str ):
            print("A coordenate is str from: ", sheet.cell_value(i,0))
            print(sheet.cell_value(i, 1),type(sheet.cell_value(i, 1)))
            print(sheet.cell_value(i, 2),type(sheet.cell_value(i, 2)))
            break
        else:
            singleRow = [sheet.cell_value(i, c) for c in range(sheet.ncols)]
        listWithData.append(singleRow)
    return listWithData
    
def CreateDataList( fileLocationData ):
    dataList = []
    for i in fileLocationData:
        dataList.append( LoadAListWithData(i))
    return dataList
        
def FitnessEvaluate (poblation, dataList):
    startTime = time.time()
    for individual in poblation:
         individual.append(fitness.FitnessValue(individual, dataList))
         #individual.append(1)
    #print("--- %s seconds ---" % (time.time() - startTime))
    return poblation

def GeneticProcess( populationWithFitness , pMutation, populationSize, tournamentSize, numSurvivos , dataList):
    parent = TournamentSelection( populationWithFitness, tournamentSize, numSurvivos )
    #itnessList  = GetOnlyFitnessList(populationWithFitness) 
    children = []
    for i in range(0, int(len(parent)/2)):
        mother = parent.pop(0)
        father = parent.pop(0)
        Son, Daugther = CrossOVer( mother, father)
        children.append(Mutation(Son, pMutation))
        children.append(Mutation(Daugther, pMutation))
    #while ( len(children) <= populationSize/2):
    #        indv = Selection(populationWithFitness, fitnessList)
    #       del indv[-1]
    #        children.append(indv)
    populationWithFitness = FitnessEvaluate(Poblation( populationSize, children), dataList)

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
        del simpleFitnessList[simpleFitnessList.index(min(simpleFitnessList))]
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

def GetSolution( poblation, numSolutions):
    copyPoblacion = poblation
    i = 0
    simpleFitnessList = GetOnlyFitnessList( copyPoblacion) 
    solution = []
    while ( i < numSolutions):
        inv = copyPoblacion[simpleFitnessList.index(max(simpleFitnessList))]
        del copyPoblacion[simpleFitnessList.index(max(simpleFitnessList))]
        del simpleFitnessList[simpleFitnessList.index(max(simpleFitnessList))]
        solution.append(inv)
        i+=1
    return solution

def Stadistics( poblations):
    mode = 0
    modes = []
    pairMode = []
    media = []
    median = []
    fitnessList = []
    for i in poblations:
        fitnessList.append(GetOnlyFitnessList(i))
    for i in fitnessList:
        pairMode = []
        mode = max(set(i), key=i.count)
        pairMode.append(mode)
        pairMode.append( i.count(mode))
        modes.append(pairMode)
        media.append(sum(i) / float(len(i)))
        median.append(statistics.median(i))
        standarDesviation = round(statistics.pstdev(fitnessList),4)
    print("Modes: ", modes)
    print("Medias: ", media) 
    print("Medians: ", median) 

def FinalStadistics( poblation):
    mode = None
    countMode = None
    media = None
    median = None
    standarDesviation = None
    fitnessList = GetOnlyFitnessList(poblation)
    mode = max(set(fitnessList), key=fitnessList.count)
    countMode = fitnessList.count(mode)
    media = (sum(fitnessList) / float(len(fitnessList)))
    median = (statistics.median(fitnessList))
    standarDesviation = statistics.pstdev(fitnessList)
    print( mode,",", countMode, ",", media, ",", median, ",", standarDesviation)

def Migration( poblations, porcentage, migrationProbability):
    luck = randint(1,100)
    if( luck <= migrationProbability):
        for i in range(0, len(poblations)-1):
            RemovePorcentagePoblation( poblations[i+1], porcentage)
            poblations[i+1].append( CopyPorcentagePoblation(poblations[i], porcentage))
        RemovePorcentagePoblation( poblations[0], porcentage)
        poblations[0].append( CopyPorcentagePoblation(poblations[-1], porcentage))

def GeneticParallelAlgorithm( numPopulation, populationSize, numGenerations, pMutation , tournamentSize, numSurvivos, pMigrationPoblation, pMigration, numSolutions):
    startTime = time.time()
    populations = []
    solution = None
    dataList  = CreateDataList( fitness.FILE_LOCATIONS)
    for i in range(0, numPopulation):
        populations.append( FitnessEvaluate(Poblation(populationSize), dataList))
    threads = []
    while( numGenerations > 0 ):
        for i in range(0, numPopulation):
                threadPoblation = threading.Thread(name='Poblation#'+str(i+1) , target=GeneticProcess, args=( populations[i], pMutation, populationSize, tournamentSize, numSurvivos , dataList))
                threads.append(threadPoblation)
                threadPoblation.start()
        for i in threads:
            i.join()
        Migration( populations, pMigrationPoblation, pMigration)
        numGenerations = numGenerations - 1
    populationInOne = []
    for i in populations:
        populationInOne.extend(i)
    solution = GetSolution( populationInOne, numSolutions)
    print("--- Tiempo ejercucion en segundos: %s  ---" % (time.time() - startTime))
    return solution

def GeneticParallelAlgorithmTest( numPopulation, populationSize, numGenerations, pMutation , tournamentSize, numSurvivos, pMigrationPoblation, pMigration, numSolutions):
    startTime = time.time()
    populations = []
    solution = None
    dataList  = CreateDataList( fitness.FILE_LOCATIONS)
    for i in range(0, numPopulation):
        populations.append( FitnessEvaluate(Poblation(populationSize), dataList))
    threads = []
    while( numGenerations > 0 ):
        for i in range(0, numPopulation):
                threadPoblation = threading.Thread(name='Poblation#'+str(i+1) , target=GeneticProcess, args=( populations[i], pMutation, populationSize, tournamentSize, numSurvivos , dataList))
                threads.append(threadPoblation)
                threadPoblation.start()
        for i in threads:
            i.join()
        Migration( populations, pMigrationPoblation, pMigration)
        numGenerations = numGenerations - 1
    populationInOne = []
    for i in populations:
        populationInOne.extend(i)
    solution = GetSolution( populationInOne, numSolutions)
    print("Coordenadas:  ", solution)
    totalTime =  (time.time() - startTime)
    return [solution[0][2], totalTime]

def main():
    solucion = None
    print("Ingrese parametros los siguientes parametros!!!")
    print("Numero de islas: ")
    numPopulation = int(input())
    print("Tamaño de las islas: ")
    populationSize = int(input())
    print("Numero de generaciones: ")
    numGenerations = int(input())
    print("Probabilidad de mutacion: ")
    pMutation = float(input())
    print("Tamaño del torneo: ")
    tournamentSize = int(input())
    print("Numero de sobrevivientes: ")
    numSurvivos = int(input())
    print("Porcenta de las poblaciones que puede migrar: ")
    pMigrationPoblation = float(input())
    print("Probabilidad de migracion: ")
    pMigration = float(input())
    print("Cantidad de soluciones: ")
    numSolutions = int(input())
    solucion = GeneticParallelAlgorithm( numPopulation, populationSize, numGenerations, pMutation , tournamentSize, numSurvivos, pMigrationPoblation, pMigration, numSolutions)
    print("Soluciones: ")
    for i in solucion:
        print(i)

def getStadistics():
    parametros = [[5, 943, 100, 0.014, 566, 467, 3, 0.338,1], [5, 719, 94, 0.022, 681, 352, 4, 0.498,1], [4, 895, 35, 0.031, 767, 142, 1, 0.111,1],[4, 932, 89, 0.027, 234, 52, 4, 0.469,1]]
    for j in parametros:
        print("Configuracion: ", j)
        for i in range(0,10):
            print("Evaluacion: ", i+1)
            test = GeneticParallelAlgorithm( *j)
    return None

#getStadistics()
#print(GeneticParallelAlgorithm(2, 10, 2 , 0.022, 10 , 1 , 4 , 0.498, 5))
def testFitness():
    dataList  = CreateDataList( fitness.FILE_LOCATIONS)
    var = FitnessEvaluate( [[-76.48788, 3.49188,]], dataList)
    print(var)

#testFitness()
#if __name__ == '__main__':
#    main()

#Stadistics( [[[1,2,1],[3,4,1],[4,6,99]],[[3,3,1],[4,4,2],[5,5,3]]])

#print(GetSolution( [[1,2,3],[1,3,4],[1,3,5]], 2))z|
#Migration( [[[1,2,3],[1,3,4],[1,3,5]],[[2,2,7],[2,3,1],[2,3,9]],[[3,2,0],[3,3,20],[3,3,15]]], 33)
#CopyPorcentagePoblation( [[1,2,1],[3,2,1],[4,5,1],[6,7,1],[8,9,2],[9,8,3],[4,8,2],[9,5,11],[9,5,10],[10,5,15]], 20 )   
#print (TournamentSelection( [[[1,1],1.0], [[2,2],2.0], [[3,3],3.0],[[4,4],4.0]], 2 , 2))
#print (TournamentSelection( [[1,2,1],[3,2,1],[4,5,1],[6,7,1],[8,9,2],[9,8,3]], 2 , 2))
#print (TournamentSelection( [[1,2,-5],[3,2,-3],[4,5,-1],[6,7,-2],[8,9,-4],[9,8,-3]], 2 , 2))
#print (Seed())
#Mutation(1)
#GeneticProcess( [[1,2],[3,2],[4,5],[6,7],[8,9],[9,8]], 1, 6, 5, 2)
#print (getOnlyFitnessList( [[1,2,4],[3,5,6],[7,8,9]]))
#RemovePorcentagePoblation( [[1,2,-1],[3,2,1],[4,5,1],[6,7,1],[8,9,2],[9,8,3],[4,8,-2],[9,5,11],[9,5,-10],[10,5,15]], 15 )