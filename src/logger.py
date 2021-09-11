# -*- coding:utf-8 -*-

import os
import time
import logging
from src.config import config
from src.statistics import stat


def format_list_to_str(origin_list):
    return ('\n' + '\n'.join(origin_list) + '\n') if origin_list else '无\n'


def log_stat():
    _copy_list = format_list_to_str(stat.copy_list)
    _overwrite_list = format_list_to_str(stat.overwrite_list)
    _warning_list = format_list_to_str(stat.warning_list)

    logger.info(
        '\n------------------ 统计信息 -----------------\n'
        f'工作模式: {stat.mode}\n'
        f'同名文件一致时: {stat.same}\n'
        f'同名文件更新时: {stat.existence}\n'
        f'跳过数: {stat.skip_count}\n'
        f'复制数: {stat.get_copy_count()} 复制: {_copy_list}'
        f'覆盖数: {stat.get_overwrite_count()} 覆盖: {_overwrite_list}'
        f'总耗时: {stat.get_duration()}\n'
        f'警告：{_warning_list}'
    )


class Logger:
    instance = None  # 记录第一个创建的实例
    logs_path = config.logs_path

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self._logger = logging.getLogger()
        self.init_logger()

    def get_logger(self):
        return self._logger

    def init_logger(self):
        self._logger.setLevel(logging.DEBUG)  # 输出的最低日志等级
        if not os.path.exists(self.logs_path):
            os.mkdir(self.logs_path)

        cur_time = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
        log_path = self.logs_path + cur_time + '.log'

        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        file_handler = logging.FileHandler(log_path, mode='w', encoding="utf-8")
        file_handler.setLevel(logging.INFO)  # 输出到文件的最低日志等级
        file_handler.setFormatter(formatter)  # 输出到文件的日志格式

        self._logger.addHandler(file_handler)


logger = Logger().get_logger()
