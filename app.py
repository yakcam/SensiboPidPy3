import logging
import sys

from SensiboApiClient import SensiboApiClient
from configuration import Configuration

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

    # Sensibo API
    sensibo = SensiboApiClient(config.api_token)
    device = sensibo.get_device(config.device_id)
    logging.info("The temperature at %s is %s", device['result']['measurements']['time']['time'], device['result']['measurements']['temperature'])

    return 0

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    EXITCODE = main()
    sys.exit(EXITCODE)