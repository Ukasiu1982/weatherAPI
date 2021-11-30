import requests
import sys
from datetime import datetime, timedelta
import json



class Weather:

    def __init__(self, api_key, date=str(datetime.today().date()+timedelta(1))):
        self.api_key = api_key
        self.date = date
        self.data = self.get_data()

    def get_data(self):
        req_url = f'https://api.meteomatics.com/{self.date}T12:00:00+01:00/precip_24h:mm/50.255689,19.022147/json'
        payload = {'key': self.api_key, "q": "London", "dt": str(self.date)}
        r = requests.get(req_url, auth=(self.api_key.split(':')[0], self.api_key.split(':')[1]))
        return r.json()['data'][0]['coordinates'][0]['dates']


    def get_rain_chance(self):
        totalprecip_mm = float(self.data[0]['value'])
        if totalprecip_mm > 0.0:
            return 'Bedzie padac'
        elif totalprecip_mm == 0.0:
            return 'Nie bedzie padac'
        else:
            return 'Nie wiem!'

with open("forecast.json", 'r') as file:
    odczyt=json.load(file)

if len(sys.argv) > 2:
    if str(sys.argv[2]) not in odczyt.keys():

        try:
            weather = Weather(api_key=sys.argv[1], date=sys.argv[2])
            odczyt[sys.argv[2]] = weather.get_rain_chance()
            print(weather.get_rain_chance())
        except:
            print('Nie wiem')

    else:
        print(odczyt[sys.argv[2]])
else:
    date = str(datetime.today().date() + timedelta(1))
    if date not in odczyt.keys():
        try:
            weather = Weather(api_key=sys.argv[1], date = date)
            odczyt[date] = weather.get_rain_chance()
            print(weather.get_rain_chance())
        except:
            print("nie wiem")
    else:
        print(odczyt[date])

with open('forecast.json', 'w') as file:
    json.dump(odczyt, file)

# python weather.py xxx_lop:Dl4J21CzabiMX  2022-11-11


