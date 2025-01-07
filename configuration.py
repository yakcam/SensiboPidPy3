from decimal import Decimal
import os


class Configuration:
    def __init__(self):
        self.api_token = ""
        self.device_id = ""
        self.target_temperature = Decimal(0)
        self.gain = Decimal(0)
        self.error = 0

    def read_configuration_from_environment(self):
        self.api_token = os.environ.get("SENSIBO_API_TOKEN")
        self.device_id = os.environ.get("SENSIBO_DEVICE_ID")
        target_temp_string = os.environ.get("TARGET_TEMPERATURE")
        if target_temp_string is not None:
            self.target_temperature = Decimal(target_temp_string)
        gain_string = os.environ.get("GAIN")
        if gain_string is not None:
            self.gain = Decimal(gain_string)

    def check_configuration(self):
        if self.api_token is None or self.api_token == "" or len(self.api_token) < 10:
            self.error = -2
        if self.device_id is None or self.device_id == "" or len(self.device_id) != 8:
            self.error = -3
        if self.target_temperature is None or self.target_temperature < 17 or self.target_temperature > 30:
            self.error = -4
        if self.gain is None:
            self.error = -5
        return self.error

    def __str__(self):
        return (f"ApiToken: ****, DeviceId: {self.device_id}, "
                f"TargetTemperature: {self.target_temperature}, Gain: {self.gain}, Error: {self.error}")