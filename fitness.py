
# Program extracting first column 
import xlrd
import math

#FitnessValue for Statios in kilometes:

CloaseDistanceStation = 1
FarDistamceStatopn = 3

def fitnessStationValue( location ):  
    loc = ("C:\\Users\\DanielHernandezCuero\\Documents\\GeneticAlgorithm\\Datos\\Estaciones.xlsx") 
    sheet = wb.sheet_by_index(0) 
    sheet.cell_value(0, 0)
    for i in range(1,sheet.nrows): 
        print(sheet.cell_value(i, 0))
        ManhattanDistance = math.sqrt(location[0]- sheet.cell_value(i, 1)) + math.sqrt(location[1]- sheet.cell_value(i, 2)))
    return ManhattanDistance