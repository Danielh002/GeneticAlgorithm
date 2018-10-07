import genetic
from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

app = Flask(__name__, template_folder=".")

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyCmYELcAqYLc4hUs-mRyE6BIpKXEl0pdaI"

# you can also pass the key here if you prefer
GoogleMaps(app)

@app.route("/")
def mapview():
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)],
        style= "width: 100%; height: 100%"
    )
    return render_template('index.html', mymap=mymap)

if __name__ == "__main__":
    app.run(debug=True)

