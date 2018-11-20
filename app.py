import genetic
import json
import csv
import io 
import os
from flask import Flask, render_template, request, session, flash,send_file, jsonify, url_for
from settings import APP_STATIC
from flask_googlemaps import GoogleMaps, Map
from celery import Celery

appi = Flask(__name__, template_folder=".")
appi.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
appi.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(appi.name, broker=appi.config['CELERY_BROKER_URL'])
celery.conf.update(appi.config)

# you can set key as config
appi.config['GOOGLEMAPS_KEY'] = "AIzaSyDsanoV7fAVo1jfnBxj_wMYGXfUDUk9QBU"


appi.secret_key = 'super secret key'
appi.config['SESSION_TYPE'] = 'filesystem'


#img = 'C:\\Users\\DanielHernandezCuero\\Documents\\GeneticAlgorithm\\Datos\\hospitalIcon.png'
#img = 'https://drive.google.com/open?id=1YnOYbe7XhjV61C5-vdK_vpXGqmYG3Xra'
#img = 'http://maps.google.com/mapfiles/ms/micons/hospitals.png'



# you can also pass the key here if you preferx
GoogleMaps(appi)


@appi.route("/")
def index():
    return render_template('templates/index.html')

@appi.route("/map",  methods=['GET', 'POST'])
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
    #locations = genetic.GeneticParallelAlgorithm( numPopulation, populationSize, pMutation, numGenerations, tournamentSize, numSurvivors, pMigrationPoblation, pMigration, numSolutions)
    
    task = genetic_task.delay( numPopulation, populationSize, pMutation, numGenerations, tournamentSize, numSurvivors, pMigrationPoblation, pMigration, numSolutions)
    #task = add.delay(5,5)
    #return str(task.id)
    return jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id)}

@appi.route("/loading/<task_id>",  methods=['GET', 'POST'])
def taskstatus(task_id):
    task = add.AsyncResult(task_id)
    print(task)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)
       
@appi.route("/getCSV")
def getCSV():
    try:
        locations = json.loads(session.get('result', None))
        with open("output.csv", "w" ,newline="") as f:
            writer = csv.writer(f)
            writer.writerows(locations)
        return send_file( 'output.csv',mimetype='text/csv', attachment_filename='location.csv', as_attachment=True)
    except Exception as e:
        return str(e)

@appi.route("/uploadCSV")
def uploadCSV():
    return render_template('templates/upload.html')

@appi.route("/processCSV", methods=["POST"])
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


@celery.task
def add(x, y):
    return x + y

@celery.task(bind=True)
def genetic_task( numPopulation, populationSize, pMutation, numGenerations, tournamentSize, numSurvivors, pMigrationPoblation, pMigration, numSolutions):
    result = genetic.GeneticParallelAlgorithm( numPopulation, populationSize, pMutation, numGenerations, tournamentSize, numSurvivors, pMigrationPoblation, pMigration, numSolutions)
    
    mymap = Map(
        identifier="view-side",
        lat=3.431355,
        lng=-76.529650,
        markers=[(loc[1], loc[0], None, None ) for loc in result],
        style= "width: 100%; height: 100%"
    )
    session['result'] = json.dumps(result)
    #return render_template('templates/map.html', mymap=mymap)        
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}

            
if __name__ == "__main__":
    appi.run(debug=True, threaded=True)

