
# Program extracting first column 
import xlrd
import math

#CONSTANTS
#The Earth's radius, 6,371km
EARTH_RADIO = 6.371

#FitnessValue for location vs Stations MIO in kilometers:
#Distance Limits
MIN_DISTANCE_STATION = 1
MAX_DISTANCE_STATION = 3
#Gain points
GOOD_DISTANCE_STATION = 20
AVERAGE_DISTANCE_STATION = 0
BAD_DISTANCE_STATION = -20

#FitnessValue for location vs Cali Clinics/Hospitals  in kilometers:
#Distance Limits
MIN_DISTANCE_HOSPITAL = 1
#Gain points
HEALTH_CENTER_NEAR_POINTS = - 50
NO_HEALTH_CENTER_NEAR_POINTS =  50

#Harvesine Formula 
#Source:
#   https://stackoverflow.com/questions/43700616/why-manhattan-distance-with-haversine-formula-for-geolocalizations-is-not-accura
#   https://stackoverflow.com/questions/32923363/manhattan-distance-for-two-geolocations
#   http://www.movable-type.co.uk/scripts/latlong.html
def ManhattanDistanceInMetricSystem( latitude1, longitude1, latitude2, longitude2):
        deltaLatitude = math.fabs( latitude1 - latitude2)
        deltaLongitude = math.fabs( longitude1 - longitude2)
        a = math.pow(math.sin( deltaLatitude/2),2)
        c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a))
        latitudeDistance = EARTH_RADIO * c 
        a = math.pow(math.sin( deltaLongitude/2),2)
        c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a))
        longitudeDistance = EARTH_RADIO * c
        manhattanDistanceMetricSystem = math.fabs(latitudeDistance) + math.fabs(longitudeDistance)
        return manhattanDistanceMetricSystem
    

#print( ManhattanDistanceInMetricSystem(37.4602, 126.441, 37.5567, 126.924))

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
            print("A coordenate is str from: ", sheet.cell_value(i,0))
            print(sheet.cell_value(i, 1),type(sheet.cell_value(i, 1)))
            print(sheet.cell_value(i, 2),type(sheet.cell_value(i, 2)))
            break
        manhattanDistance = ManhattanDistanceInMetricSystem( location[0], location[1], sheet.cell_value(i, 1), sheet.cell_value(i, 2)) 
    if( manhattanDistance < minManhattanDistance):
        points = GOOD_DISTANCE_STATION
    if( minManhattanDistance > MIN_DISTANCE_STATION and minManhattanDistance < MAX_DISTANCE_STATION):
        points = AVERAGE_DISTANCE_STATION
    if ( minManhattanDistance > MAX_DISTANCE_STATION):
        points = BAD_DISTANCE_STATION
    return points

def fitnessHospitalsDistance( location ):  
    loc = ("C:\\Users\\DanielHernandezCuero\\Documents\\GeneticAlgorithm\\Datos\\Estaciones.xlsx")
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
    sheet.cell_value(0, 0)
    manhattanDistance = 0.0
    minManhattanDistance = math.inf
    points = 0
    for i in range(1,sheet.nrows): 
        if (type(sheet.cell_value(i, 1)) is str or type(sheet.cell_value(i, 2)) is str ):
            print("A coordenate is str from: ", sheet.cell_value(i,0))
            print(sheet.cell_value(i, 1),type(sheet.cell_value(i, 1)))
            print(sheet.cell_value(i, 2),type(sheet.cell_value(i, 2)))
            break
        manhattanDistance = math.sqrt(location[0]- sheet.cell_value(i, 1)) + math.sqrt(location[1]- sheet.cell_value(i, 2))
        if (manhattanDistance < minManhattanDistance):
            minManhattanDistance = manhattanDistance 
    if( manhattanDistance < MIN_DISTANCE_HOSPITAL):
        points = HEALTH_CENTER_NEAR_POINTS
    if ( minManhattanDistance >= MAX_DISTANCE_STATION):
        points = NO_HEALTH_CENTER_NEAR_POINTS
    return points

print( fitnessStationDistance([-71, 13]))

