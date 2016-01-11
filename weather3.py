import urllib.request
from xml.dom import minidom

class WeatherReport:
    def __init__(self, high:int, low:int, weather:str):
        self.High = int(high)
        self.Low = int(low)
        self.Weather = weather
        self.xmldoc = None

    def __str__(self):
        return ("High: " + str(self.High) + ", Low: " + str(self.Low) + ", Forecast: " + self.Weather)

    @property
    def Average(self) -> float:
        avg = (self.High + self.Low) / 2.0
        return avg

class WeatherStation:
    def get_Location(self) -> (float,float):
        url = 'http://ip-api.com/csv/?fields=lat,lon'
        with urllib.request.urlopen(url) as http_connection:
            value_array = http_connection.readline().decode().split(',')
        lat = float(value_array[0])
        lon = float(value_array[1])
        return (lat,lon)


    def get_Weather(self, includeXmlDoc:bool=False) -> WeatherReport:
        pos = self.get_Location()
        url = 'http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdBrowserClientByDay.php?lat=' + str(pos[0]) + "&lon=" + str(pos[1]) + '&format=24+hourly&numDays=7'
        with urllib.request.urlopen(url) as http_connection:
            xmldoc = minidom.parseString(http_connection.read())
        xml_values = xmldoc.getElementsByTagName('value')
        weather_forecasts = xmldoc.getElementsByTagName('weather-conditions')
        weatherCond = weather_forecasts[0]._attrs['weather-summary'].firstChild.nodeValue
        report = WeatherReport(high=xml_values[0].firstChild.nodeValue,low=xml_values[7].firstChild.nodeValue,weather=weatherCond)
        if (includeXmlDoc):
            report.xmldoc = xmldoc
        return report