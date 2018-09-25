import genetic
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    a = genetic.unit()
    print (a)
    return "hola"

if __name__ == "__main__":
    app.run()   