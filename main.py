import genetic
from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

app = Flask(__name__, template_folder=".")

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyDsanoV7fAVo1jfnBxj_wMYGXfUDUk9QBU"

# you can also pass the key here if you prefer
GoogleMaps(app)

@app.route("/")
def mapview():
    # creating a map in the view
    locations = genetic.GeneticParallelAlgorithm(3, 3 , 1, 50, 50, 10, 2)
    print([(loc[1], loc[0]) for loc in locations])
    mymap = Map(
        identifier="view-side",
        lat=3.431355,
        lng=-76.529650,
        markers=[(loc[1], loc[0]) for loc in locations],
        style= "width: 100%; height: 100%"
    )
    return render_template('index.html', mymap=mymap)

if __name__ == "__main__":
    app.run(debug=True)

