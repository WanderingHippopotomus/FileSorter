# Built by WanderingHippopotomus

import logging

logging.basicConfig(
    format = '%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] - %(message)s',
    level = logging.DEBUG,
    filename = 'logs.txt'
)

logger = logging.getLogger(__name__)