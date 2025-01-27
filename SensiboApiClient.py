import requests
import SensiboDevice

class SensiboApiClient:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://home.sensibo.com/api/v2"

    def _get_headers(self):
        return {
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip"
        }

    def get_device(self, device_id):
        url = f"{self.base_url}/pods/{device_id}?fields=location,measurements,acState&apiKey={self.api_token}"
        response = requests.get(url, headers=self._get_headers(), timeout=30)
        response.raise_for_status()
        return response.json()

    def set_target_temperature(self, device_id, temperature):
        url = f"{self.base_url}/pods/{device_id}/acStates/targetTemperature?apiKey={self.api_token}"
        payload = {
            "newValue": temperature
        }
        response = requests.patch(url, json=payload, headers=self._get_headers(), timeout=30)
        response.raise_for_status()
        return response.json()

    def set_ac_state(self, device_id, state, property_name):
        url = f"{self.base_url}/pods/{device_id}/acStates/{property_name}?apiKey={self.api_token}"
        payload = {
            "newValue": f"{state}"
        }
        response = requests.patch(url, json=payload, headers=self._get_headers(), timeout=30)
        response.raise_for_status()
        return response.json()