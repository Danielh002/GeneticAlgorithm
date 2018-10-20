
# Program extracting first column 
import xlrd
import math


#CONSTANTS
#The Earth's radius, 6,371km
EARTH_RADIO = 6371

#FitnessValue for location vs Stations MIO in kilometers:
#Distance Limits
MIN_DISTANCE_STATION = 7
MAX_DISTANCE_STATION = 3
#Gain points
GOOD_DISTANCE_STATION = 20
AVERAGE_DISTANCE_STATION = 0
BAD_DISTANCE_STATION = -20

#FitnessValue for location vs Cali Clinics/Hospitals  in kilometers:
#Distance Limits
MIN_DISTANCE_HOSPITAL = 5
#Gain points
HEALTH_CENTER_NEAR_POINTS =  -50
NO_HEALTH_CENTER_NEAR_POINTS =  50

#FitnessValue for location vs FireFighters in kilometers:
#Distance Limits
MIN_DISTANCE_FIREFIGTHER = 3
MAX_DISTANCE_FIREFIGTHER = 7
#Gain points
GOOD_DISTANCE_FIREFIGTHER = 50
AVERAGE_DISTANCE_FIREFIGTHER =  0
BAD_DISTANCE_FIREFIGTHER = -50

#Harvesine Formula 
#Source:
#   https://stackoverflow.com/questions/43700616/why-manhattan-distance-with-haversine-formula-for-geolocalizations-is-not-accura
#   https://stackoverflow.com/questions/32923363/manhattan-distance-for-two-geolocations
#   http://www.movable-type.co.uk/scripts/latlong.html
#   https://www.latlong.net/lat-long-dms.html

#3.370720, -76.536617
#3.367075, -76.528985
#930.09 m (3.051,49 pies)


#source = (45.070060, 7.663708)
#target = (45.072800, 7.665540)

#MI CASA : 3.471766, -76.524704
#Chipi 3.476348, -76.526826

def ManhattanDistanceInMetricSystem( latitude1, longitude1, latitude2, longitude2):
    dlatitude1, dlongitude1, dlatitude2, dlongitude2 = map(math.radians, [latitude1, longitude1, latitude2, longitude2])
    deltaLatitude = math.fabs( dlatitude1 - dlatitude2)
    deltaLongitude = math.fabs( dlongitude1 - dlongitude2)
    a = math.pow(math.sin( deltaLatitude/2),2)
    c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a))
    latitudeDistance = EARTH_RADIO * c 
    a = math.pow(math.sin( deltaLongitude/2),2)
    c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a))
    longitudeDistance = EARTH_RADIO * c
    manhattanDistanceMetricSystem = math.fabs(latitudeDistance) + math.fabs(longitudeDistance)
    return manhattanDistanceMetricSystem
    


def fitnessStationDistance( location ):  
    loc = ("C:\\Users\\DanielHernandezCuero\\Documents\\GeneticAlgorithm\\Datos\\Estaciones.xlsx")
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
    sheet.cell_value(0, 0)
    manhattanDistance = 0.0
    minManhattanDistance = math.inf
    points = 0
    for i in range(1,sheet.nrows): 
        if (type(sheet.cell_value(i, 1)) is str or type(sheet.cell_value(i, 2)) is str ):
            #print("A coordenate is str from: ", sheet.cell_value(i,0))
            #print(sheet.cell_value(i, 1),type(sheet.cell_value(i, 1)))
            #print(sheet.cell_value(i, 2),type(sheet.cell_value(i, 2)))
            break
        manhattanDistance = ManhattanDistanceInMetricSystem( location[0], location[1], sheet.cell_value(i, 1), sheet.cell_value(i, 2)) 
        
        if( manhattanDistance < minManhattanDistance):
            #print(sheet.cell_value(i, 0))
            minManhattanDistance = manhattanDistance
            #print(minManhattanDistance)
    if( minManhattanDistance < MIN_DISTANCE_STATION ):
        points = GOOD_DISTANCE_STATION
    if( minManhattanDistance > MIN_DISTANCE_STATION and minManhattanDistance < MAX_DISTANCE_STATION):
        points = AVERAGE_DISTANCE_STATION
    if( minManhattanDistance > MAX_DISTANCE_STATION):
        points = BAD_DISTANCE_STATION
    return points

def fitnessHospitalsDistance( location ):  
    loc = ("C:\\Users\\DanielHernandezCuero\\Documents\\GeneticAlgorithm\\Datos\\Hospitales.xlsx")
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
    sheet.cell_value(0, 0)
    manhattanDistance = 0.0
    minManhattanDistance = math.inf
    points = 0
    for i in range(1,sheet.nrows): 
        if (type(sheet.cell_value(i, 1)) is str or type(sheet.cell_value(i, 2)) is str ):
            #print("A coordenate is str from: ", sheet.cell_value(i,0))
            #print(sheet.cell_value(i, 1),type(sheet.cell_value(i, 1)))
            #print(sheet.cell_value(i, 2),type(sheet.cell_value(i, 2)))
            break
        manhattanDistance = ManhattanDistanceInMetricSystem( location[0], location[1], sheet.cell_value(i, 1), sheet.cell_value(i, 2)) 
        if (manhattanDistance < minManhattanDistance):
            minManhattanDistance = manhattanDistance 
    if( minManhattanDistance < MIN_DISTANCE_HOSPITAL):
        points = HEALTH_CENTER_NEAR_POINTS
    if( minManhattanDistance >= MAX_DISTANCE_STATION):
        points = NO_HEALTH_CENTER_NEAR_POINTS
    return points

def fitnessFirefigtherDistance( location ):  
    loc = ("C:\\Users\\DanielHernandezCuero\\Documents\\GeneticAlgorithm\\Datos\\Bomberos.xlsx")
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
    sheet.cell_value(0, 0)
    manhattanDistance = 0.0
    minManhattanDistance = math.inf
    points = 0
    for i in range(1,sheet.nrows): 
        if (type(sheet.cell_value(i, 1)) is str or type(sheet.cell_value(i, 2)) is str ):
            #print("A coordenate is str from: ", sheet.cell_value(i,0))
            #print(sheet.cell_value(i, 1),type(sheet.cell_value(i, 1)))
            #   print(sheet.cell_value(i, 2),type(sheet.cell_value(i, 2)))
            break
        manhattanDistance = ManhattanDistanceInMetricSystem( location[0], location[1], sheet.cell_value(i, 1), sheet.cell_value(i, 2)) 
        if( manhattanDistance < minManhattanDistance):
            minManhattanDistance = manhattanDistance
    if( minManhattanDistance < MIN_DISTANCE_FIREFIGTHER ):
        points = GOOD_DISTANCE_STATION
    if( minManhattanDistance > MIN_DISTANCE_FIREFIGTHER and minManhattanDistance < MAX_DISTANCE_FIREFIGTHER):
        points = AVERAGE_DISTANCE_FIREFIGTHER
    if( minManhattanDistance > MAX_DISTANCE_FIREFIGTHER):
        points = BAD_DISTANCE_FIREFIGTHER
    return points

def FitnessValue ( individual):
    fitnessValueStation = fitnessStationDistance(individual)
    fitnessValueHospital = fitnessHospitalsDistance(individual)
    fitnessValueFireFighthers = fitnessFirefigtherDistance(individual)
    return fitnessValueStation + fitnessValueHospital + fitnessValueFireFighthers

#print(fitnessStationDistance([-71,3.5]))
#print( FitnessValue([-71, 13]))
#print( ManhattanDistanceInMetricSystem( 45.070060,  7.663708, 45.072800, 7.665540))
#print( ManhattanDistanceInMetricSystem( 3.471766,  -76.524704, 3.476348, -76.526826))

 