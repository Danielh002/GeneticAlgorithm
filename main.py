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

#icons http://tancro.e-central.tv/grandmaster/markers/google-icons/mapfiles-ms-micons.htmlz



hospitalicon = 'http://127.0.0.1:5000/static/hospitalsIcon.png'
stationIcon = 'http://127.0.0.1:5000/static/busIcon.png'
fireFigtherIcon = 'http://127.0.0.1:5000/static/firefigtherIcon.png'
blueIcon = 'http://127.0.0.1:5000/static/blueIcon.png'
greenIcon = 'http://127.0.0.1:5000/static/greenIcon.png'
orangeIcon = 'http://127.0.0.1:5000/static/orangeIcon.png'

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
    locations = genetic.GeneticParallelAlgorithm( numPopulation, populationSize, numGenerations, pMutation,  tournamentSize, numSurvivors, pMigrationPoblation, pMigration, numSolutions)
    session['result'] = json.dumps(locations)
    marks = ColorMarks(locations)
    marks.extend(specialMarkersTuples())
    mymap = Map(
        identifier="view-side",
        lat=3.431355,
        lng=-76.529650,
        markers = marks,
        style= "width: 100%; height: 100%"
    )
    
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
        pair.append(float(i[0]))
        pair.append(float(i[1]))
        app.logger.info(i[0])
        pair.append(float(i[2]))
        
        locations.append(pair)
    
    marks = ColorMarks(locations)
    mymap = Map(
        identifier="view-side",
        lat=3.431355,
        lng=-76.529650,
        markers=marks,
        style= "width: 100%; height: 100%"
    )
    session['result'] = json.dumps(locations)
    return render_template('templates/map.html', mymap=mymap)

def specialMarkersTuples():
    markList = []
    mark = {
		"icon" : None,
		"lat" : None,
		"lng" : None,
		"infobox" : None,
	}
    stations = genetic.LoadAListWithData( genetic.fitness.statiosRoute)
    hospital = genetic.LoadAListWithData( genetic.fitness.hospitalRoute)
    fireFigther = genetic.LoadAListWithData( genetic.fitness.fireFightersRoute)
    for i in stations:
        mark["infobox"] = i[0]
        mark["lat"] = i[2]
        mark["lng"] = i[1]
        mark["icon"] = stationIcon      
        markList.append(mark.copy())  
    for i in hospital:
        mark["infobox"] = i[0]
        mark["lat"] = i[2]
        mark["lng"] = i[1]
        mark["icon"] = hospitalicon
        markList.append(mark.copy())  
    for i in fireFigther:
        mark["infobox"] = i[0]
        mark["lat"] = i[2]
        mark["lng"] = i[1]
        mark["icon"] = fireFigtherIcon
        markList.append(mark.copy())        
    return markList

def ColorMarks( solutions ):
    markList = []
    mark = {
		"icon" : None,
		"lat" : None,
		"lng" : None,
		"infobox" : None,
	}
    for i in solutions:
        mark["lat"] = i[1]
        mark["lng"] = i[0]
        mark["infobox"] = "<b> Lat, Log: </b>" + str(round(i[1],5)) + ", " + str(round(i[0],5)) + "<br>" + "<b>" + "Aptitud: </b>" + str(i[2])
        if i[2] < 70:
            mark["icon"] = greenIcon
        elif i[2] >= 70 and i[2] < 75:
            mark["icon"] = blueIcon
        else:
            mark["icon"] = orangeIcon
        markList.append(mark.copy())
    return markList







 

if __name__ == "__main__":
    app.run(debug=True, threaded=True)

