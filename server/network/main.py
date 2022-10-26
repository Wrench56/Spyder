import logging
import logging.config

import yaml

if __name__ == '__main__':
    with open('./config/logger.config.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    logger = logging.getLogger()
    logger.info('Server starting...')
    
