import requests
import sys
from datetime import datetime
import json


class Weather:

    def __init__(self, api_key, date=str(datetime.today().date())):
        self.api_key = api_key
        self.date = date
        self.data = self.get_data()

    def get_data(self):
        req_url = 'http://api.weatherapi.com/v1/history.json'
        payload = {'key': self.api_key, "q": "London", "dt": str(self.date)}
        r = requests.get(req_url, params=payload)
        content = r.json()
        return content

    def get_rain_info(self):
        totalprecip_mm = float(self.data['forecast']['forecastday'][0]['day']
                               ['totalprecip_mm'])
        return self.get_rain_chance(totalprecip_mm)


    def get_rain_chance(totalprecip_mm):
        if totalprecip_mm > 0.0:
            return 'Bedzie padac'
        elif totalprecip_mm == 0.0:
            return 'Nie bedzie padac'
        else:
            return 'Nie wiem!'


weather = Weather(api_key=sys.argv[1], date=sys.argv[2])
with open("forecast.json", 'r') as file:
    odczyt = json.load(file)
    if str(sys.argv[2]) not in odczyt.keys():
        odczyt[sys.argv[2]] = weather.get_rain_info()

print(odczyt[sys.argv[2]])

with open("forecast.json", "w") as forecast2:
    json.dump(odczyt, forecast2)
