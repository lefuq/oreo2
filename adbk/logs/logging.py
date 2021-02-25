import logging


def set_config(logger):
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filename='adbk/logs/CUlogs.log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
