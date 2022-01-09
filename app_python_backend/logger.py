import logging
from conf import CONF

# create logger with 'spam_application'
logger = logging.getLogger(CONF.APP_NAME)
logger.setLevel(CONF.LOGGING_LEVEL)

# create console handler with a higher log level
ch = logging.StreamHandler()

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(ch)