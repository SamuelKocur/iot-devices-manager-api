import logging

from iot_devices_manager.settings import LOOKBACK_URL

logger = logging.getLogger(__name__)


def call_recalculation_endpoint():
    import requests
    url = f'{LOOKBACK_URL}api/data-warehouse/recalculate-collected-data/'
    response = requests.get(url)
    if response.status_code == 200:
        logger.info('Successfully called recalculation endpoint')
    else:
        logger.info(f'Failed to call recalculation endpoint: {response.status_code}')
