# -*- coding:utf-8 -*-

import os
import time
from src.logger import logger


def format_time(longtime):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(longtime))


def format_byte(byte_cnt):
    s = str(byte_cnt)[::-1]  # reverse
    s = ','.join(s[i:i + 3] for i in range(0, len(s), 3))
    return s[::-1] + ' B'  # reverse again


def format_src_paths(src_paths: list):
    _ = list(map(lambda x: x.strip('/ '), src_paths))  # strip all ' ' and '/'
    return [x + '/' if os.path.isdir(x) else x for x in _]  # for dir: append one '/'


def format_dst_root_path(dst: str):
    # strip all ' ' and '/', then append one '/'
    return dst.strip('/ ') + '/'


def join_dst_path(src: str, dst_root: str):
    # e.g. (C:/src/file, D:/dst/) -> D:/dst/src/file
    pos = src.find(':/') + 2
    return dst_root + src[pos:]


def check_not_exist_paths(paths: list):
    not_exist_paths = [p for p in paths if not os.path.exists(p)]
    if not_exist_paths:
        logger.error('The following paths do not exist:\n' + '\n'.join(not_exist_paths))
        raise Exception('Invalid source paths. Please check log.')


def check_dst_root_path(dst: str):
    err_msg = None
    if not os.path.exists(dst):
        err_msg = f'Destination Path ({dst}) does not exist.'
    elif not os.path.isdir(dst):
        err_msg = f'Destination Path ({dst}) is not a directory.'
    if err_msg:
        logger.error(err_msg)
        raise Exception('Invalid destination. Please check log.')


def format_check_src_dst(src_paths, dst_root_path):
    src_paths = format_src_paths(src_paths)
    dst_root_path = format_dst_root_path(dst_root_path)
    check_dst_root_path(dst_root_path)
    check_not_exist_paths(src_paths)
    return src_paths, dst_root_path
