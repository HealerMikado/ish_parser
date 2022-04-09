from ish_parser.Units import Units
from ish_parser.Temperature import Temperature
from .BaseComponent import BaseComponent

class ExtremeAirTemperature(BaseComponent):
    """
    For KAx with x in [1;4]
    """
    TEMPERATURE_SCALE = 10.0
    CODE = {
        'N': 'Minimum',
        'M': 'Maximum',
        'O': 'Estimate minimum',
        'P': 'Estimate maximum',
        '9': 'MISSING',
    }

    def loads(self, string):
        self.extreme_temperature = {
            'hours': int(string[0:3]),
            'code': string[3:4],
            'temperature': Temperature(int(string[4:9]) / self.TEMPERATURE_SCALE, Units.CELSIUS, string[9:10])}

    def __repr__(self):
        return str(self.extreme_temperature)

    def __str__(self):
        return str(self.extreme_temperature)

    def toJson(self):
        return {
            'hours': self.extreme_temperature['hours'],
            'code': self.extreme_temperature['code'],
            'temperature': self.extreme_temperature['temperature'].asJson()
        }
