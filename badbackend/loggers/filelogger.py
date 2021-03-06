"""configures logger to log to file specified in Logger stanza of
`config.yaml`. Does no configuration if stanza not present or 
missing `filename` value"""

import logging
import yaml

config = yaml.load(open("config.yaml"), Loader=yaml.Loader)

if 'Logger' in config and 'filename' in config['Logger']:
    logging.basicConfig(filename=config['Logger']['filename'], 
        level=logging.__dict__.get(config['Logger']['loglevel'].upper()
            if 'loglevel' in config['Logger'] else "INFO", logging.INFO),
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
