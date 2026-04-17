import flask
import json
import os

app = flask.Flask(__name__)


# GRID COORDINATE INFORMATION
# longitude determines letter from alphabet
# latitude determines number up to height
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
height = 15

if not os.path.exists('logs.json'):
    with open('logs.json', 'x') as f:
        json.dump(list(), f)



with open('logs.json', 'r') as f:
    data = json.load(f)

@app.route('/')
def index():
    return flask.render_template("./index.html")

@app.route('/contact', methods=["POST"])
def contact():
    try:
        callsign = flask.request.form['callsign']
        location = flask.request.form['location']
        indoors = flask.request.form['indoors']
        low_power = flask.request.form['low_power'] 
        print(callsign)
        print(location)
        print(indoors)
        print(low_power)

        indoors = indoors == 'on'
        low_power = low_power == 'on'

        lat, lon = location.split(' ')

        lat = float(lat)
        lon = float(lon)

        # lat range is -73.6677 to -73.685
        # lon range is 42.725 to 42.734

        lon += 73.6677
        lat -= 42.725

        lon /= 73.685 - 73.6677
        lat /= 42.734 - 42.725

        lon *= -len(alphabet)
        lat *= height

        # Then turn it into letters

        lon -= .5
        lat -= .5

        lon = round(lon)
        lat = round(lat)
        print(lon)
        print(lat)

        lon = alphabet[lon]

        data.append({
            'callsign': callsign,
            #'location': [lat, lon],
            'location': lon + str(lat),
            'indoors': indoors,
            'low_power': low_power
        })
        with open('logs.json', 'w') as f:
            json.dump(data, f, indent = 4)
        return flask.redirect('/?success=true')
    except Exception as e:
        print(e)
        return flask.redirect('/?success=false')

if __name__ == '__main__':
    app.run()
