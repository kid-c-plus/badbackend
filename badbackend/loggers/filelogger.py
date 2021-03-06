"""configures logger to log to file specified in Logger stanza of
`config.yaml`. Does no configuration if stanza not present or 
missing `filename` value"""

import logging

def configure_logging(config: dict) -> None :
    if 'filename' in config:
        logging.basicConfig(filename=config['filename'], 
            level=logging.__dict__.get(config['loglevel'].upper()
                if 'loglevel' in config else "INFO", logging.INFO),
            format='%(asctime)s %(levelname)-8s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
