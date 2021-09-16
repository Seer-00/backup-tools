# -*- coding:utf-8 -*-

import os
import time
import re
from src.logger import logger


def format_time(longtime):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(longtime))


def format_byte(byte_cnt):
    s = str(byte_cnt)[::-1]  # reverse
    s = ','.join(s[i:i + 3] for i in range(0, len(s), 3))
    return s[::-1] + ' B'  # reverse again


def format_path(path: str):
    if not path.endswith('/') and os.path.isdir(path):
        return path + '/'
    else:
        return path


def format_paths(paths: list):
    _ = list(map(lambda x: re.sub(r'\\+', '/', x.strip(r'\/ ')), paths))  # replace '\', '\\' to '/'
    return list(map(format_path, _))  # for dir: append one '/'


def format_dst_root_path(dst: str):
    return re.sub(r'\\+', '/', dst.strip(r'\/ ')) + '/'


def join_dst_path(src: str, dst_root: str):
    # e.g. (C:/src/file, D:/dst/) -> D:/dst/src/file
    # e.g. (C:/src/dir/, D:/dst/) -> D:/dst/src/dir/
    pos = src.find(':/') + 2
    return dst_root + src[pos:]


def check_not_exist_paths(paths: list):
    not_exist_paths = [p for p in paths if not os.path.exists(p)]
    if not_exist_paths:
        logger.error('The following paths do not exist:\n' + '\n'.join(not_exist_paths))
        raise Exception('Invalid paths. Please check log.')


def check_dst_root_path(dst: str):
    err_msg = None
    if not os.path.exists(dst):
        err_msg = f'Destination Path ({dst}) does not exist.'
    elif not os.path.isdir(dst):
        err_msg = f'Destination Path ({dst}) is not a directory.'
    if err_msg:
        logger.error(err_msg)
        raise Exception('Invalid destination. Please check log.')


def handle_src(src_paths):
    src_paths = format_paths(src_paths)
    check_not_exist_paths(src_paths)
    return src_paths


def handle_ignore(ignore_paths):
    ignore_paths = format_paths(ignore_paths)
    check_not_exist_paths(ignore_paths)
    return ignore_paths


def handle_dst(dst_root_path):
    dst_root_path = format_dst_root_path(dst_root_path)
    check_dst_root_path(dst_root_path)
    return dst_root_path
