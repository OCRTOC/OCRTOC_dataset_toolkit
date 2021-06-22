import logging
import colorlog

LOGGER_NAME = 'OCRTOC Dataset Toolkit'

log_fmt = "{log_color}{asctime} [{name}][{levelname}]:{message}"
log_level = logging.INFO
main_logger = logging.getLogger(LOGGER_NAME)

def set_log_level(level='WARNING'):
    """Setup the log level for the logger

    Args:
        level(string): a string of log level among 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'. 'WARNING' is the default.
    """
    level=level.upper()
    global log_level
    if level == 'DEBUG':
        log_level = logging.DEBUG
    elif level == 'INFO':
        log_level = logging.INFO
    elif level == 'WARNING':
        log_level = logging.WARNING
    elif level == 'ERROR':
        log_level = logging.ERROR
    elif level == 'CRITICAL':
        log_level = logging.CRITICAL
    else:
        raise ValueError("Unknown log level %s, which should one of 'DEBUG','INFO','WARNING','ERROR','CRITICAL'" % (log_level,))
    change_main_logger()

def get_main_logger():
    '''Get the logger
    
    Returns:
        logger: The logger instance
    '''
    global main_logger
    return main_logger

def change_main_logger():
    global main_logger, log_level
    colorlog.basicConfig(
        level=log_level,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'white',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        },
        style="{",
        format=log_fmt,
        datefmt='%m-%d %H:%M:%S',
        stream=None
    )
    main_logger = logging.getLogger(LOGGER_NAME)
    main_logger.setLevel(log_level)

change_main_logger()