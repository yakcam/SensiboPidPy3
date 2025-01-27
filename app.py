import logging
import sys
import time

from simple_pid import PID
from SensiboApiClient import SensiboApiClient
from configuration import Configuration
from SensiboDevice import SensiboDevice

def gather_configuration():
    config = Configuration()
    config.read_configuration_from_environment()
    config.check_configuration()
    return config

def main():
    # Read and check config
    logging.info("Reading configuration...")
    config = gather_configuration()
    logging.debug(config)
    if config.error != 0:
        print("Error in configuration")
        return config.error
    logging.info("Configuration is valid")

    # Sensibo API - current state
    sensibo = SensiboApiClient(config.api_token)
    device = SensiboDevice()
    device.parse(sensibo.get_device(config.device_id))
    logging.info("Temperature is %s at %s", device.temperature, device.time)

    # PID controller
    pid = PID(config.gain, 0, 0, setpoint=config.target_temperature, output_limits=(17, 30))
    target_temp = pid(device.temperature)
    logging.info("Target temperature is %s", target_temp)

    # Loop and update pid, control sensibo with output
    while True:
        device.parse(sensibo.get_device(config.device_id))

        # If the device is off, slow loop
        if device.on is False:
            logging.info("Device is off, waiting for 2 minutes")
            time.sleep(120)
            continue

        # Device is on, continue with control loop
        time.sleep(15)
        logging.info("Temperature is %s at %s", device.temperature, device.time)
        target_temp = round(pid(device.temperature))
        logging.info("Target temperature is %s", target_temp)

        # Some logic about fan
        if target_temp > config.target_temperature:
            fan_level = "high"
        else:
            fan_level = "auto"

        # Send commands if needed
        if device.fan_level != fan_level:
            sensibo.set_ac_state(config.device_id, fan_level, "fanLevel")
        if device.temperature != target_temp:
            sensibo.set_target_temperature(config.device_id, target_temp)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    EXITCODE = main()
    sys.exit(EXITCODE)
