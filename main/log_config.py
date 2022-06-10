"""Configurate flask logger"""
import logging
import os


def log_config(app):
    """logger config"""
    dir_name = "logs/api.log"
    os.makedirs(os.path.dirname(dir_name), exist_ok=True)
    hdlr = logging.FileHandler('logs/api.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    app.logger.addHandler(hdlr)
