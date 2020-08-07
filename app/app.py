from flask import Flask, Response
from prometheus_client import Counter, Gauge, generate_latest
import logging
import requests
import time

logger = logging.getLogger(__name__)
app = Flask(__name__)

api_calls = Counter(
    'api_calls',
    'Number of api calls with Counter'
)
temp_change = Gauge(
    'temperature_change',
    'Temperature change with Gauge')

# Budapest coordinates
lat = "47.498"
lon = "19.0399"
api_key = "<Openweather API key>"


@app.route('/metrics', methods=['GET'])
def get_weather_data():
    # Current weather data for Budapest
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&APPID={api_key}"
    r1 = requests.get(url).json()['current']['temp']
    logger.info(f"Getting current ({int(time.time())}) weather data for Budapest. Used URL: {url}")

    # One hour earlier weather data for Budapest
    one_hour_back_unix = int(time.time()) - 3600
    url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={one_hour_back_unix}&units=metric&appid={api_key}"
    r2 = requests.get(url).json()['current']['temp']
    logger.info(f"Getting one hour earlier ({one_hour_back_unix}) weather data for Budapest. Used URL: {url}")

    api_calls.inc()
    temp_change.set(r1-r2)

    return Response(generate_latest(), mimetype=str('text/plain; charset=utf-8'))


if __name__ == '__main__':
    app.run(debug=True, host='<host IP address>')
