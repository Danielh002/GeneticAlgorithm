
# Program extracting first column 
import xlrd
import math
import time

FILE_LOCATIONS = [
    "C:\\Users\\DanielHernandezCuero\\Documents\\GeneticAlgorithm\\Datos\\Estaciones.xlsx",
     "C:\\Users\\DanielHernandezCuero\\Documents\\GeneticAlgorithm\\Datos\\Hospitales.xlsx",  
     "C:\\Users\\DanielHernandezCuero\\Documents\\GeneticAlgorithm\\Datos\\Bomberos.xlsx",      
]

STATION_ROUTE_POSITION = 0
HOSPITALS_ROUTE_POSITION = 1
FIREFIGTHER_ROUTE_POSITION = 2

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
    
def fitnessStationDistanceV2( location, dataStations ):  
    manhattanDistance = 0.0
    minManhattanDistance = math.inf
    points = 0
    for i in dataStations:
        manhattanDistance = ManhattanDistanceInMetricSystem( location[0], location[1], i[1], i[2]) 
        if( manhattanDistance < minManhattanDistance):
            minManhattanDistance = manhattanDistance
    if( minManhattanDistance < MIN_DISTANCE_STATION ):
        points = GOOD_DISTANCE_STATION
    if( minManhattanDistance > MIN_DISTANCE_STATION and minManhattanDistance < MAX_DISTANCE_STATION):
        points = AVERAGE_DISTANCE_STATION
    if( minManhattanDistance > MAX_DISTANCE_STATION):
        points = BAD_DISTANCE_STATION
    return points


def fitnessHospitalsDistance( location, dataHospitals):  
    manhattanDistance = 0.0
    minManhattanDistance = math.inf
    points = 0
    for i in dataHospitals:
        manhattanDistance = ManhattanDistanceInMetricSystem( location[0], location[1], i[1], i[2]) 
        if( manhattanDistance < minManhattanDistance):
            minManhattanDistance = manhattanDistance
    if( minManhattanDistance < MIN_DISTANCE_HOSPITAL):
        points = HEALTH_CENTER_NEAR_POINTS
    if( minManhattanDistance >= MAX_DISTANCE_STATION):
        points = NO_HEALTH_CENTER_NEAR_POINTS
    return points

def fitnessFirefigtherDistance( location, dataFireFigther):  
    manhattanDistance = 0.0
    minManhattanDistance = math.inf
    points = 0
    for i in dataFireFigther:
        manhattanDistance = ManhattanDistanceInMetricSystem( location[0], location[1], i[1], i[2]) 
        if( manhattanDistance < minManhattanDistance):
            minManhattanDistance = manhattanDistance
    if( minManhattanDistance < MIN_DISTANCE_FIREFIGTHER ):
        points = GOOD_DISTANCE_STATION
    if( minManhattanDistance > MIN_DISTANCE_FIREFIGTHER and minManhattanDistance < MAX_DISTANCE_FIREFIGTHER):
        points = AVERAGE_DISTANCE_FIREFIGTHER
    if( minManhattanDistance > MAX_DISTANCE_FIREFIGTHER):
        points = BAD_DISTANCE_FIREFIGTHER
    return points


def FitnessValue ( individual, dataList ):
    fitnessValueStation = fitnessStationDistanceV2(individual, dataList[STATION_ROUTE_POSITION])
    fitnessValueHospital = fitnessHospitalsDistance(individual, dataList[HOSPITALS_ROUTE_POSITION])
    fitnessValueFireFighthers = fitnessFirefigtherDistance(individual, dataList[FIREFIGTHER_ROUTE_POSITION])
    return fitnessValueStation + fitnessValueHospital + fitnessValueFireFighthers
 