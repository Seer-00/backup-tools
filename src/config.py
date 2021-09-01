# -*- coding:utf-8 -*-

import os
import json


class Config:
    _json_path = os.getcwd().replace('\\', '/') + '/config.json'
    _default_config = {
        'backup_source': ['D:/directory', 'E:/文件夹/文件名.txt'],
        'backup_destination': 'D:/备份目的地',
        'logs_path': os.getcwd().replace('\\', '/') + '/logs/'
    }

    def __init__(self):
        config_json = self.load_config_json()
        self.backup_source = config_json['backup_source']  # 备份源路径
        self.backup_destination = config_json['backup_destination']  # 备份目的地根目录
        self.logs_path = config_json['logs_path']  # 日志文件夹路径

    def is_config_exist(self):
        return os.path.exists(self._json_path)

    def load_config_json(self):
        if self.is_config_exist():
            with open(self._json_path, mode='r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return self._default_config

    def create_config_json(self):
        with open(self._json_path, mode='w', encoding='utf-8') as f:
            json.dump(self._default_config, f, indent=4, ensure_ascii=False)


config = Config()
