import requests
import sys
from datetime import datetime, timedelta
import json



class WeatherForecast:



    def __init__(self, api_key, date=str(datetime.today().date()+timedelta(1))):
        self.api_key = api_key
        self.date = date
        self.data = self.get_data()
        self.weather = self.weather_info()


    def weather_info(self):
        with open("forecast.json", 'r') as file:
            odczyt = json.load(file)
        return odczyt


    def get_data(self):
        req_url = f'https://api.meteomatics.com/{self.date}T12:00:00+01:00/precip_24h:mm/51.509865,-0.118092/json'
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


    def get_dates(self):
        with open('forecast.json', 'r') as file3:
            daty = []
            odczyt = json.load(file3)
            for key in odczyt.keys():
                daty.append(key)
            print(daty)


    def items(self):
        for date, value in self.weather.items():
            yield (date, value)


    def __getitem__(self, item):
        return self.weather.get(item, "Nie wiem")


    def __iter__(self):
        return iter(self.weather.keys())


wf = WeatherForecast(sys.argv[1])

with open("forecast.json", 'r') as file:
    odczyt=json.load(file)


if len(sys.argv) > 2:
    if str(sys.argv[2]) not in odczyt.keys():

        try:
            weather = WeatherForecast(api_key=sys.argv[1], date=sys.argv[2])
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
            weather = WeatherForecast(api_key=sys.argv[1], date = date)
            odczyt[date] = weather.get_rain_chance()
            print(weather.get_rain_chance())
        except:
            print("nie wiem")
    else:
        print(odczyt[date])

with open('forecast.json', 'w') as file:
    json.dump(odczyt, file)

# python weather.py xxx_lop:Dl4J21CzabiMX

print(wf.get_rain_chance().replace('\n', ''))
for data, pogoda in wf.items():
    print(data, pogoda)
print("Daty dla ktorych generowana byla pogoda to:")
for v in wf:
    print(v)

