from random import randint,choice,uniform

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
        whichGene = randint(0, genomeSize-2)
        newIndividual = Seed()
        individual[whichGene] = newIndividual[whichGene]
    return individual

def TournamentSelection( population , tournamentSize, numSurvivors):
    competitors = []
    survivors = []
    for i in range(0, numSurvivors):
        for i in range(0,tournamentSize):
            competitors.append(choice(population))
        for i in com:
            biggestValue = 0
            indvPosition = 0
            if ( competitors[i][1] > biggestValue):
                biggestValue = competitors[i][1]
                indvPosition = i
        survivors.append( competitors[indvPosition][0])
    return survivors

def Fitness( indivdual ):
    return individual.append(uniform(0, 100))

def FitnessEvaluate (poblation):
    for individual in poblation:
         individual.append(uniform(0, 100))
    return poblation


def GeneticProcess( population, pMutacion, populationSize, tournamentSize, numSurvivos):
    parent = TournamentSelection( population, tournamentSize, numSurvivos )
    children = []
    for i in range(0, int(populationSize/2) - 1):
        Son, Daugther = CrossOVer(  parent.pop, parent.pop)
        children.append(Mutation(Son, pMutacion))
        children.append(Mutation(Daugther, pMutacion))
    children = FitnessEvaluate(Poblation( populationSize, children))
    return children
   
#print (TournamentSelection( [[[1,1],1.0], [[2,2],2.0], [[3,3],3.0],[[4,4],4.0]], 2 , 2))
print (TournamentSelection( [[1,2,1],[3,2,1],[4,5,1],[6,7,1],[8,9,2],[9,8,3]], 2 , 2))
#print (Seed())
#Mutation(1)

#print (GeneticProcess( [[1,2],[3,2],[4,5],[6,7],[8,9],[9,8]], 1, 6, 5, 2))
