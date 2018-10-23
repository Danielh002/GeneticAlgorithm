import genetic
import json
import csv
from flask import Flask, render_template, request, session, flash

from flask_googlemaps import GoogleMaps, Map

app = Flask(__name__, template_folder=".")


# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyDsanoV7fAVo1jfnBxj_wMYGXfUDUk9QBU"

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


img = 'C:\\Users\\DanielHernandezCuero\\Documents\\GeneticAlgorithm\\Datos\\hospitalIcon.png'

# you can also pass the key here if you preferx
GoogleMaps(app)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/map",  methods=['GET', 'POST'])
def mapview():
    numPopulation =  int(request.args.get('numPopulation'))
    populationSize = int(request.args.get('populationSize'))
    pMutation = int(request.args.get('pMutation'))
    numGenerations = int(request.args.get('numGenerations'))
    tournamentSize = int(request.args.get('tournamentSize'))
    numSurvivors = int(request.args.get('numSurvivors'))
    pMigrationPoblation = int(request.args.get('pMigrationPoblation'))
    pMigration = int(request.args.get('pMigration'))
    numSolutions = int(request.args.get('numSolutions'))
    # creating a map in the view
    #locations = genetic.GeneticParallelAlgorithm(3, 1000 , 1, 50, 50, 10, 20)
    locations = genetic.GeneticParallelAlgorithm( numPopulation, populationSize, pMutation, numGenerations, tournamentSize, numSurvivors, pMigrationPoblation, pMigration, numSolutions)
    mymap = Map(
        identifier="view-side",
        lat=3.431355,
        lng=-76.529650,
        markers=[(loc[1], loc[0], None ) for loc in locations],
        style= "width: 100%; height: 100%"
    )
    session['result'] = json.dumps(locations)
    return render_template('map.html', mymap=mymap)

@app.route("/getCSV")
def getCSV():
    locations = json.loads(session.get('result', None))
    with open("output.csv", "w" ,newline="") as f:
        writer = csv.writer(f)
        writer.writerows(locations)
    flash('You were successfully logged in')
    return ('', 204)

if __name__ == "__main__":

    app.run(debug=True, threaded=True)

