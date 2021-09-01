# -*- coding:utf-8 -*-

import src.backup_copy as backup_copy
from src.config import config
from src.logger import log_stat


if __name__ == '__main__':
    if config.is_config_exist():
        backup_copy.copy(config.backup_source, config.backup_destination)
        log_stat()
    else:
        config.create_config_json()
