from logging import getLogger


log = getLogger(__name__)


def get_logger(name, log_file_name="current.log"):
    import os
    import logging
    import json
    # https://docs.python.org/3/library/logging.handlers.html
    # from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
    from concurrent_log_handler import ConcurrentRotatingFileHandler
    LOG_DIR = 'log/'
    log_format: str = '%(asctime)s - %(name)s.%(funcName)s:%(lineno)d - %(levelname)s - %(message)s'
    os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create handlers
    # c_handler = logging.StreamHandler()
    one_mb_byte = pow(2, 20)
    f_handler = ConcurrentRotatingFileHandler(LOG_DIR+log_file_name, maxBytes=one_mb_byte * 10, backupCount=100)

    f_format = logging.Formatter(log_format)
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)
    logger.propagate = False
    return logger
