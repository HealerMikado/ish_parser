from .BaseComponent import BaseComponent


class PresentWeatherConditionComponent(BaseComponent):
    ''' handle any AU Type'''
    CONDITION = {
        '00': 'No significant weather observed',
        '01': 'Clouds generally dissolving or becoming less developed',
        '02': 'State of sky on the whole unchanged during the past hour',
        '03': 'Clouds generally forming or developing during the past hour',
        '04': 'Haze, smoke, or dust in suspension in the air, visibility equal to or greater than 1km',
        '05': 'Smoke',
        '07': 'Dust or sand raised by wind at or near the station at the time of observation, but no other event',
        '10': 'Mist',
        '11': 'Diamond dust',
        '12': 'Distant lightning',
        '18': 'Squalls',
        '20': 'Fog',
        '21': 'Precipitation',
        '22': 'Drizzle (not freezing) or snow grains',
        '23': 'Rain (not freezing)',
        '24': 'Snow',
        '25': 'Freezing drizzle or freezing rain',
        '26': 'Thunderstorm (with or without precipitation)',
        '27': 'Blowing or drifting snow or sand',
        '28': 'Blowing or drifting snow or sand, visibility equal to or greater than 1 km',
        '29': 'Blowing or drifting snow or sand, visibility less than 1 km',
        '30': 'Fog',
        '31': 'Fog or ice fog in patches',
        '32': 'Fog or ice fog, has become thinner during the past hour',
        '33': 'Fog or ice fog, no appreciable change during the past hour',
        '34': 'Fog or ice fog, has begun or become thicker during the past hour',
        '35': 'Fog, depositing rime',
        '40': 'Precipitation',
        '41': 'Precipitation, slight or moderate',
        '42': 'Precipitation, heavy',
        '43': 'Liquid precipitation, slight or moderate',
        '44': 'Liquid precipitation, heavy',
        '45': 'Solid precipitation, slight or moderate',
        '46': 'Solid precipitation, heavy',
        '47': 'Freezing precipitation, slight or moderate',
        '48': 'Freezing precipitation, heavy',
        '50': 'Drizzle',
        '51': 'Drizzle, not freezing, slight',
        '52': 'Drizzle, not freezing, moderate',
        '53': 'Drizzle, not freezing, heavy',
        '54': 'Drizzle, freezing, slight',
        '55': 'Drizzle, freezing, moderate',
        '56': 'Drizzle, freezing, heavy',
        '57': 'Drizzle and rain, slight',
        '58': 'Drizzle and rain, moderate or heavy',
        '60': 'Rain',
        '61': 'Rain, not freezing, slight',
        '62': 'Rain, not freezing, moderate',
        '63': 'Rain, not freezing, heavy',
        '64': 'Rain, freezing, slight',
        '65': 'Rain, freezing, moderate',
        '66': 'Rain, freezing, heavy',
        '67': 'Rain or drizzle and snow, slight',
        '68': 'Rain or drizzle and snow, moderate or heavy',
        '70': 'Snow',
        '71': 'Snow, slight',
        '72': 'Snow, moderate',
        '73': 'Snow, heavy',
        '74': 'Ice pellets, slight',
        '75': 'Ice pellets, moderate',
        '76': 'Ice pellets, heavy',
        '77': 'Snow grains',
        '78': 'Ice crystals',
        '80': 'Showers or intermittent precipitation',
        '81': 'Rain showers or intermittent rain, slight',
        '82': 'Rain showers or intermittent rain, moderate',
        '83': 'Rain showers or intermittent rain, heavy',
        '84': 'Rain showers or intermittent rain, violent',
        '85': 'Snow showers or intermittent snow, slight',
        '86': 'Snow showers or intermittent snow, moderate',
        '87': 'Snow showers or intermittent snow, heavy',
        '89': 'Hail',
        '90': 'Thunderstorm',
        '91': 'Thunderstorm, slight or moderate, with no precipitation',
        '92': 'Thunderstorm, slight or moderate, with rain showers and/or snow showers',
        '93': 'Thunderstorm, slight or moderate, with hail',
        '94': 'Thunderstorm, heavy, with no precipitation',
        '95': 'Thunderstorm, heavy, with rain showers and/or snow',
        '96': 'Thunderstorm, heavy, with hail',
        '99': 'Tornado'
    }

    def loads(self, string):
        try:
            self.present_weather_condition = self.CONDITION[string[0:2]]
        except:
            self.present_weather_condition = "UNKNOWN"

    def __repr__(self):
        return str(self.present_weather_condition)

    def __str__(self):
        return str(self.present_weather_condition)

    def toJson(self):
        return {"present_weather_condition": self.present_weather_condition}
