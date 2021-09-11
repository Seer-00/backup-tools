# -*- coding:utf-8 -*-

from src.backup_copy import BackupCopy
from src.config import config
from src.logger import log_stat


if __name__ == '__main__':
    if config.is_config_exist():
        backup_copy = BackupCopy(config=config)
        backup_copy.copy()
        log_stat()
    else:
        config.create_config_json()
