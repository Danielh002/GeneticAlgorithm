
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
cityInfoRoute = os.path.join(pathfile,"Datos","Comunas.xlsx")
avenuesRoute = os.path.join(pathfile,"Datos","Avenidas.xlsx")

FILE_LOCATIONS = [
    statiosRoute,
    hospitalRoute,  
    fireFightersRoute,
    cityInfoRoute,
    avenuesRoute,
]

STATION_ROUTE_POSITION = 0
HOSPITALS_ROUTE_POSITION = 1
FIREFIGTHER_ROUTE_POSITION = 2
CIRY_INFO_ROUTE = 3
AVENUES_ROUTE = 4




#CAR_ACCIDENT_ROUTE_POSITION = 3
#PERSONAL_INJURIES_ROUTE = 4

###############################################################################
#FitnessValue for location vs Cali Clinics/Hospitals  in kilometers:
#Distance Limits
MIN_DISTANCE_HOSPITAL = 5
#Points:
HEALTH_CENTER_NEAR_POINTS =  - 20
NO_HEALTH_CENTER_NEAR_POINTS =  20
###############################################################################
#FitnessValue for location vs Stations MIO in kilometers:
#Distance Limits
MIN_DISTANCE_STATION = 3
MAX_DISTANCE_STATION = 7
#Points:
GOOD_DISTANCE_STATION = 3
AVERAGE_DISTANCE_STATION = 0
BAD_DISTANCE_STATION = -3
###############################################################################
#FitnessValue for location vs FireFighters in kilometers:
#Distance Limits
MIN_DISTANCE_FIREFIGTHER = 3
MAX_DISTANCE_FIREFIGTHER = 7
#Points
GOOD_DISTANCE_FIREFIGTHER = 5
AVERAGE_DISTANCE_FIREFIGTHER =  0
BAD_DISTANCE_FIREFIGTHER = -5
###############################################################################
#CAR_INJURIES 
CAR_ACCIDENTS_PERCENTILE30 = 90.8
CAR_ACCIDENTS_PERCENTILE70 = 140.2
CAR_ACCIDENTS_POINTS_GOOD = 20
CAR_ACCIDENTS_POINTS_AVERAGE = 0
CAR_ACCIDENTS_POINTS_BAD = -20
###############################################################################
#PersonasInjueriesValor 
PERSONAL_INJURIES_PERCENTILE30 = 236.2
PERSONAL_INJURIES_PERCENTILE70 = 323.9
PERSONAL_INJURIES_POINTS_GOOD = 20
PERSONAL_INJURIES_POINTS_AVERAGE = 0
PERSONAL_INJURIES_POINTS_BAD = -20
###############################################################################
#Mortality 
MORTALITY_PERCENTILE30 = 460.8
MORTALITY_PERCENTILE70 = 639.1
MORTALITY_INJURIES_POINTS_GOOD = 15
MORTALITY_INJURIES_POINTS_AVERAGE = 0
MORTALITY_INJURIES_POINTS_BAD = -15
###############################################################################
#Poblation 
POBLATION_PERCENTILE30 = 69749.7
POBLATION_PERCENTILE70 = 110681.6
POBLATION_INJURIES_POINTS_GOOD = 7
POBLATION_INJURIES_POINTS_AVERAGE = 0
POBLATION_INJURIES_POINTS_BAD = -7
################################################################################
#Avenues
MIN_AVENUES_DISTANCE = 1
AVENUES_SPEED_POINTS_GOOD = 10
AVENUES_SPEED_POINTS_AVERAGE = 0
AVENUES_SPEED_POINTS_BAD = -10



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
    points = 0
    for i in dataCarAccident:
        if( i[3] >= haversineDistance( location[0], location[1], i[1], i[2])):
            if(i[9] <= CAR_ACCIDENTS_PERCENTILE30 and points < CAR_ACCIDENTS_POINTS_BAD ):
                points = CAR_ACCIDENTS_POINTS_BAD
            elif(i[9] > CAR_ACCIDENTS_PERCENTILE30 and i[9] < CAR_ACCIDENTS_PERCENTILE70 and points < CAR_ACCIDENTS_POINTS_AVERAGE):
                points = CAR_ACCIDENTS_POINTS_AVERAGE
            else:
                points = CAR_ACCIDENTS_POINTS_GOOD
    return points

def fitnessPersonalInjueriesCali( location, dataPersonalInjueries):
    points = 0
    for i in dataPersonalInjueries:
        if( i[3] >= haversineDistance( location[0], location[1], i[1], i[2])):
            if(i[4] <= PERSONAL_INJURIES_PERCENTILE30 and points < PERSONAL_INJURIES_POINTS_BAD):
                points = PERSONAL_INJURIES_POINTS_BAD
            elif(i[4] > PERSONAL_INJURIES_PERCENTILE30 and i[10] < PERSONAL_INJURIES_PERCENTILE70 and PERSONAL_INJURIES_POINTS_AVERAGE):
                points = PERSONAL_INJURIES_POINTS_AVERAGE
            else:
                points = PERSONAL_INJURIES_POINTS_GOOD
    return points

def fitnessMortalityCali( location, dataPersonalInjueries):
    points = 0
    for i in dataPersonalInjueries:
        if( i[3] >= haversineDistance( location[0], location[1], i[1], i[2])):
            if(i[8] <= MORTALITY_PERCENTILE30 and points < MORTALITY_INJURIES_POINTS_GOOD):
                points = MORTALITY_INJURIES_POINTS_BAD
            elif(i[8] > MORTALITY_PERCENTILE30 and i[10] < MORTALITY_PERCENTILE70 and MORTALITY_INJURIES_POINTS_AVERAGE):
                points = MORTALITY_INJURIES_POINTS_AVERAGE
            else:
                points = MORTALITY_INJURIES_POINTS_GOOD
    return points

def fitnessPoblationInjuriesCali( location, dataPersonalInjueries):
    points = 0
    for i in dataPersonalInjueries:
        if( i[3] >= haversineDistance( location[0], location[1], i[1], i[2])):
            if(i[7] <= POBLATION_PERCENTILE30 and points < POBLATION_INJURIES_POINTS_BAD):
                points = POBLATION_INJURIES_POINTS_BAD
            elif(i[7] > POBLATION_PERCENTILE30 and i[10] < POBLATION_PERCENTILE70 and POBLATION_INJURIES_POINTS_AVERAGE):
                points = POBLATION_INJURIES_POINTS_AVERAGE
            else:
                points = POBLATION_INJURIES_POINTS_GOOD
    return points

def fitnessAvenuesDistance(location, dataStations ):  
    manhattanDistance = 0.0
    minManhattanDistance = math.inf
    points = 0
    for i in dataStations:
        manhattanDistance = ManhattanDistanceInMetricSystem( location[0], location[1], i[1], i[2]) 
        if( manhattanDistance < minManhattanDistance):
            minManhattanDistance = manhattanDistance
            break
    if( minManhattanDistance < MIN_AVENUES_DISTANCE ):
        if( i[3] < AVENUES_SPEED_POINTS_BAD ):
            points = AVENUES_SPEED_POINTS_BAD
        elif( i[3] >= AVENUES_SPEED_POINTS_BAD and i[3] < AVENUES_SPEED_POINTS_AVERAGE):
            points = AVENUES_SPEED_POINTS_AVERAGE
        elif( i[3] < AVENUES_SPEED_POINTS_BAD ):
            points = AVENUES_SPEED_POINTS_BAD
        else:
            points = AVENUES_SPEED_POINTS_GOOD
    return points
    

def FitnessValue ( individual, dataList ):
    fitnessValueStation = fitnessStationDistance(individual, dataList[STATION_ROUTE_POSITION])
    fitnessValueHospital = fitnessHospitalsDistance(individual, dataList[HOSPITALS_ROUTE_POSITION])
    fitnessValueFireFighthers = fitnessFirefigtherDistance(individual, dataList[FIREFIGTHER_ROUTE_POSITION])
    fitnessValueCarAccidentCali = fitnessCarAccidentCali(individual, dataList[CIRY_INFO_ROUTE])
    fitnessValuesPersonalInjueriesCali = fitnessPoblationInjuriesCali(individual, dataList[CIRY_INFO_ROUTE])
    fitnessValuePoblationCali = fitnessMortalityCali(individual, dataList[CIRY_INFO_ROUTE])
    fitnessValuesAvenuesDistance = fitnessAvenuesDistance(individual, dataList[AVENUES_ROUTE])
    sumPoints = fitnessValueStation + fitnessValueHospital + fitnessValueFireFighthers + fitnessValueCarAccidentCali + fitnessValuesPersonalInjueriesCali + fitnessValuePoblationCali + fitnessValuesAvenuesDistance
    if( sumPoints < 0):
        sumPoints = 0
    elif( sumPoints > 100):
        sumPoints = 100
    return sumPoints
 