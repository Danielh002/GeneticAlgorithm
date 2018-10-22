mport json
import csv
 
my_list = [1,2,3,4,5,6]
json_str = json.dumps(my_list)
print(json_str)

my_list2 = [ [1,2],[1,3]]
json_str2 = json.dumps(my_list2)
print( json_str2)
data  = json.loads(json_str2)
print(data)
# make sure to use the json.dumps and not json.dump
# they have different purposes

with open("output.csv", "w" ,newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)