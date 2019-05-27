import genetic
import json
import csv
import io 
import os
from flask import Flask, render_template, request, session, flash,send_file
from settings import APP_STATIC
from flask_googlemaps import GoogleMaps, Map

app = Flask(__name__, template_folder=".")


# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyDsanoV7fAVo1jfnBxj_wMYGXfUDUk9QBU"


app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


#img = 'C:\\Users\\DanielHernandezCuero\\Documents\\GeneticAlgorithm\\Datos\\hospitalIcon.png'
#img = 'https://drive.google.com/open?id=1YnOYbe7XhjV61C5-vdK_vpXGqmYG3Xra'
hospitalicon = 'http://maps.google.com/mapfiles/ms/micons/hospitals.png'
stationIcon = 'http://maps.google.com/mapfiles/ms/micons/bus.png'
fireFigtherIcon = 'http://maps.google.com/mapfiles/ms/micons/firedept.png'

# you can also pass the key here if you preferx
GoogleMaps(app)


@app.route("/")
def index():
    return render_template('templates/index.html')

@app.route("/map",  methods=['GET', 'POST'])
def mapview():
    numPopulation =  int(request.args.get('numPopulation'))
    populationSize = int(request.args.get('populationSize'))
    pMutation = float(request.args.get('pMutation'))*100
    numGenerations = int(request.args.get('numGenerations'))
    tournamentSize = int(request.args.get('tournamentSize'))
    numSurvivors = int(request.args.get('numSurvivors'))
    pMigrationPoblation = int(request.args.get('pMigrationPoblation'))
    pMigration = float(request.args.get('pMigration'))*100
    numSolutions = int(request.args.get('numSolutions'))
    specialMarkers = specialMarkersTuples()
    locations = genetic.GeneticParallelAlgorithm( numPopulation, populationSize, numGenerations, pMutation,  tournamentSize, numSurvivors, pMigrationPoblation, pMigration, numSolutions)
    calculateLocations = locations.copy()
    for i in locations:
        i.insert(2,None)
    print(locations)
    locations.extend(specialMarkers)
    mymap = Map(
        identifier="view-side",
        lat=3.431355,
        lng=-76.529650,
        markers=[(loc[1], loc[0], None, loc[2] ) for loc in locations],
        style= "width: 100%; height: 100%"
    )
    session['result'] = json.dumps(calculateLocations)
    return render_template('templates/map.html', mymap=mymap)

@app.route("/getCSV")
def getCSV():
    try:
        locations = json.loads(session.get('result', None))
        with open("output.csv", "w" ,newline="") as f:
            writer = csv.writer(f)
            writer.writerows(locations)
        return send_file( 'output.csv',mimetype='text/csv', attachment_filename='location.csv', as_attachment=True)
    except Exception as e:
        return str(e)

@app.route("/uploadCSV")
def uploadCSV():
    return render_template('templates/upload.html')

@app.route("/processCSV", methods=["POST"])
def processCSV():
    locations = []
    f = request.files['data_file']
    if not f:
        return "No file"
    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = list(csv.reader(stream))
    for i in csv_input:
        pair = []
        pair.append(i[0])
        pair.append(i[1])
        locations.append(pair)  
    mymap = Map(
        identifier="view-side",
        lat=3.431355,
        lng=-76.529650,
        markers=[(loc[1], loc[0], None, None ) for loc in locations],
        style= "width: 100%; height: 100%"
    )
    session['result'] = json.dumps(locations)
    return render_template('templates/map.html', mymap=mymap)

def specialMarkersTuples():
    stations = genetic.LoadAListWithData( genetic.fitness.statiosRoute)
    hospital = genetic.LoadAListWithData( genetic.fitness.hospitalRoute)
    fireFigther = genetic.LoadAListWithData( genetic.fitness.fireFightersRoute)
    for i in stations:
        i.pop(0)
        i.append(stationIcon)
    for i in hospital:
        i.pop(0)
        i.append(hospitalicon)
    for i in fireFigther:
        i.pop(0)
        i.append(fireFigtherIcon)
    stations.extend(hospital)
    stations.extend(fireFigther)
    return stations

if __name__ == "__main__":
    app.run(debug=True, threaded=True)

