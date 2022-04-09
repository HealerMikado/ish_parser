from ish_parser import Temperature
from ish_parser.Components import BaseComponent


class ExtremeAirTemperature(BaseComponent):
    """
    For KAx with x in [1;4]
    """
    CODE = {
        'N': 'Minimum',
        'M': 'Maximum',
        'O': 'Estimate minimum',
        'P': 'Estimate maximum',
        '9': 'MISSING',
    }
    def loads(self, string):
        self.precipitation = {
            'hours': int(string[0:3]),
            'code': string[3:4],
            'temperature': Temperature(string[4:9], Temperature.CELSIUS,string[9:10] )}

    def __repr__(self):
        return str(self.precipitation)

    def __str__(self):
        return str(self.precipitation)
    def toJson(self):
        return {
            'hours': self.precipitation['hours'],
            'code': self.precipitation['code'],
            'temperature': self.precipitation['temperature'].toJson()
        }