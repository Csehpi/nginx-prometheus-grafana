from flask import Flask, Response
from prometheus_client import Counter, Gauge, generate_latest
import logging
import random
import requests
import time

logger = logging.getLogger(__name__)
app = Flask(__name__)

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

#config = configparser.ConfigParser()
#config.read('config.ini')
#return config['openweathermap']['api']

api_calls = Counter(
    'api_calls',
    'Number of api calls.'
)
temp_change = Gauge(
    'temperature_change',
    'Temperature change')

lat = "47.498"
lon = "19.0399"
api_key = "6c0d5d6a24a282ef0bf337bc100df5c8"

@app.route('/metrics', methods=['GET'])
def get_weather_data():
    """Returns all data as plaintext."""
    one_hour_back_unix = int(time.time()) - 3600
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&APPID={api_key}"
    print(url)
    r1 = requests.get(url).json()['current']['temp']
    url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={one_hour_back_unix}&units=metric&appid={api_key}"
    print(url)
    r2 = requests.get(url).json()['current']['temp']
    api_calls.inc()
    temp_change.set(r1-r2)
    print(r1, r2, one_hour_back_unix)
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
