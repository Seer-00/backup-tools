# -*- coding:utf-8 -*-

import os
import json
import src.utils as utils


def check_redundant_paths(paths: list, err: list, kind=''):
    # TODO: better efficiency
    redundants = set()
    for i, p in enumerate(paths):
        for j in paths[i+1:]:
            if j.startswith(p) or p.startswith(j):
                redundants.add(j)
                redundants.add(p)

    for r in sorted(list(redundants)):  # sorted for better format
        err.append(f'[Redundant] ({kind} {r})')


def check_conflict_paths(srcs: list, igns: list, err: list):
    for i in igns:
        for s in srcs:
            if s.startswith(i):
                err.append(f'[Conflict] (source {s}) but (ignore {i})')


def handle_config(cfg):
    cfg.src_paths = utils.handle_src(config.backup_source)
    cfg.ign_paths = utils.handle_src(config.backup_ignore)
    cfg.backup_destination = utils.handle_dst(config.backup_destination)

    err = []
    # conflict paths. e.g. source: D:/A/B, D:/A/c.txt BUT ignore: D:/A
    check_conflict_paths(cfg.src_paths, cfg.ign_paths, err)

    # redundant paths. e.g. D:/A/a, D:/A
    check_redundant_paths(cfg.src_paths, err, kind='source')
    check_redundant_paths(cfg.ign_paths, err, kind='ignore')

    cfg.ign_paths = set(cfg.ign_paths)  # list->set: more efficient query
    return cfg, err


class Config:
    _json_path = os.getcwd().replace('\\', '/') + '/config.json'
    _default_config = {
        'backup_source': ['D:/directory', 'E:/文件夹/文件名.txt'],
        'backup_ignore': ['D:/directory', 'E:/文件夹/文件名.txt'],
        'backup_destination': 'D:/备份目的地文件夹',
        'logs_path': os.getcwd().replace('\\', '/') + '/logs/'
    }

    def __init__(self):
        config_json = self.load_config_json()
        self.backup_source = config_json['backup_source']  # 备份源路径
        self.backup_ignore = config_json['backup_ignore']  # 忽略的文件、文件夹
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
