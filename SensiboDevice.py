import datetime

class SensiboDevice:
    def __init__(self):
        self.temperature = 0.0
        self.time = datetime.datetime.now()
        self.fan_level = ""
        self.target_temperature = 0
        self.on = False

    def parse(self, device_json):
        self.temperature = float(device_json['result']['measurements']['temperature'])
        self.time = device_json['result']['measurements']['time']['time']
        self.fan_level = device_json['result']['acState']['fanLevel']
        if 'targetTemperature' in device_json['result']['acState']:
            self.target_temperature = int(device_json['result']['acState']['targetTemperature'])
        self.on = device_json['result']['acState']['on'] is True
