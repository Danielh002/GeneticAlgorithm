
# Program extracting first column 
import xlrd
import math
import time
import os

#CONSTANTS
#The Earth's radius, 6,371km
EARTH_RADIO = 6371

pathfile = os.getcwd()
statiosRoute = os.path.join(pathfile,"Datos","Estaciones.xlsx")
hospitalRoute = os.path.join(pathfile,"Datos","Hospitales.xlsx")
fireFightersRoute = os.path.join(pathfile,"Datos","Bomberos.xlsx")
carAccidentsRoute = os.path.join(pathfile,"Datos","AccidentesTransitoCali.xlsx")
personalInjuriesRoute = os.path.join(pathfile,"Datos","AccidentesTransitoCali.xlsx")



FILE_LOCATIONS = [
    statiosRoute,
    hospitalRoute,  
    fireFightersRoute,
    carAccidentsRoute,
    personalInjuriesRoute,
]

STATION_ROUTE_POSITION = 0
HOSPITALS_ROUTE_POSITION = 1
FIREFIGTHER_ROUTE_POSITION = 2
CAR_ACCIDENT_ROUTE_POSITION = 3
PERSONAL_INJURIES_ROUTE = 4

###############################################################################
#FitnessValue for urgencies  in kilometers:
MAX_POINTS_CAR_ACCIDENTS = 25
MAX_POINTS_PERSONAL_INJURIES = 25
#FitnessValue for location vs Cali Clinics/Hospitals  in kilometers:
#Distance Limits
MIN_DISTANCE_HOSPITAL = 5
#Gain points
HEALTH_CENTER_NEAR_POINTS =  - 25
NO_HEALTH_CENTER_NEAR_POINTS =  25
###############################################################################
#FitnessValue for location vs Stations MIO in kilometers:
#Distance Limits
MIN_DISTANCE_STATION = 3
MAX_DISTANCE_STATION = 7
#Gain points
GOOD_DISTANCE_STATION = 15
AVERAGE_DISTANCE_STATION = 0
BAD_DISTANCE_STATION = -15
###############################################################################
#FitnessValue for location vs FireFighters in kilometers:
#Distance Limits
MIN_DISTANCE_FIREFIGTHER = 3
MAX_DISTANCE_FIREFIGTHER = 7
#Gain points
GOOD_DISTANCE_FIREFIGTHER = 10
AVERAGE_DISTANCE_FIREFIGTHER =  0
BAD_DISTANCE_FIREFIGTHER = -10




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


def haversineDistance(latitude1, longitude1, latitude2, longitude2):
    longitude1, latitude1, longitude2, latitude2 = map( math.radians, [longitude1, latitude1, longitude2, latitude2])
    dlon = longitude2 - longitude1 
    dlat = latitude2 - latitude1 
    a = math.sin(dlat/2)**2 + math.cos(latitude1) * math.cos(latitude2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    return c * EARTH_RADIO  

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
    
def fitnessStationDistance(location, dataStations ):  
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

def fitnessCarAccidentCali( location, dataCarAccident):
    sumAccidents = 0
    points = 0
    total = 2278
    for i in dataCarAccident:
        if( i[3] >= haversineDistance( location[0], location[1], i[1], i[2])):
            sumAccidents = sumAccidents + i[4]
    points = (sumAccidents*MAX_POINTS_CAR_ACCIDENTS)/total
    return points

def fitnessPersonalInjueriesCali( location, dataPersonalInjueries):
    sumAccidents = 0
    points = 0
    total = 6955
    for i in dataPersonalInjueries:
        if( i[3] >= haversineDistance( location[0], location[1], i[1], i[2])):
            sumAccidents = sumAccidents + i[4]
    points = (sumAccidents*MAX_POINTS_PERSONAL_INJURIES)/total
    return points


def FitnessValue ( individual, dataList ):
    fitnessValueStation = fitnessStationDistance(individual, dataList[STATION_ROUTE_POSITION])
    fitnessValueHospital = fitnessHospitalsDistance(individual, dataList[HOSPITALS_ROUTE_POSITION])
    fitnessValueFireFighthers = fitnessFirefigtherDistance(individual, dataList[FIREFIGTHER_ROUTE_POSITION])
    fitnessValueCarAccidentCali = fitnessCarAccidentCali(individual, dataList[CAR_ACCIDENT_ROUTE_POSITION])
    fitnessPersonalInjueriesCali = fitnessCarAccidentCali(individual, dataList[PERSONAL_INJURIES_ROUTE])
    sumPoints = fitnessValueStation + fitnessValueHospital + fitnessValueFireFighthers + fitnessValueCarAccidentCali + fitnessPersonalInjueriesCali
    if( sumPoints < 0):
        sumPoints = 0
    elif( sumPoints > 100):
        sumPoints = 100
    return sumPoints
 