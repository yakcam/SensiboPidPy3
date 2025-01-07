from decimal import Decimal
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
    print("Reading configuration...")
    config = gather_configuration()
    print(config)
    if config.error != 0:
        print("Error in configuration")
        return config.error
    
    # Sensibo API
    sensibo = SensiboApiClient(config.api_token)
    device = sensibo.get_device(config.device_id)
    print(device)

    return 0

if __name__ == "__main__":
    EXITCODE = main()
    sys.exit(EXITCODE)