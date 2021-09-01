# -*- coding:utf-8 -*-

import os
import shutil
import src.utils as utils
from src.logger import logger
from src.statistics import stat


def get_file_info(filepath: str):
    file_info = os.stat(filepath)
    return {
        'size': utils.format_byte(file_info.st_size),
        'access_time': utils.format_time(file_info.st_atime),
        'modify_time': utils.format_time(file_info.st_mtime),
        'create_time': utils.format_time(file_info.st_ctime)
    }


def is_same_files(fp1, fp2):
    f1, f2 = get_file_info(fp1), get_file_info(fp2)
    return f1['size'] == f2['size'] and f1['modify_time'] == f2['modify_time']


def copy(src_paths, dst_root_path):
    src_paths, dst_root_path = utils.format_check_src_dst(src_paths, dst_root_path)
    dst_root_path = utils.format_dst_root_path(dst_root_path)
    for src in src_paths:
        try:
            logger.info(f'>>>>> [Begin] to copy ({src}) >>>>>')
            try_to_copy(src, dst_root_path)
            logger.info(f'<<<<< [Finish] to copy ({src}) <<<<<')
        except Exception as e:
            logger.exception(e)
            return


def try_to_copy(src, dst_root_path):
    dst = utils.join_dst_path(src=src, dst_root=dst_root_path)
    # dst exist
    if os.path.exists(dst):
        if os.path.isdir(src):
            cp_exist_dir(src, dst_root_path)  # recursively try to copy sub-items
        else:
            cp_exist_file(src, dst)
    # dst not exist
    else:
        if os.path.isdir(src):
            cp_not_exist_dir(src, dst)
        else:
            cp_not_exist_file(src, dst)


def cp_not_exist_dir(src, dst):
    shutil.copytree(src, dst)
    stat.copy_list.append(src)
    logger.info(f'[Copy] ({src}) -> ({dst})')


def cp_not_exist_file(src, dst):
    dst_parent_path = os.path.dirname(dst)
    # create new dir
    if not os.path.exists(dst_parent_path):
        os.makedirs(dst_parent_path)
        logger.info(f'[Create] new directory ({dst_parent_path})')
    # copy file
    shutil.copy2(src, dst)
    stat.copy_list.append(src)
    logger.info(f'[Copy] ({src}) -> ({dst})')


def cp_exist_dir(src, dst_root_path):
    for sub_item in os.listdir(src):  # recursively try to copy sub-items
        sub_src = os.path.join(src, sub_item).replace('\\', '/')
        try:
            # logger.info(f'>>>>> [Begin] to copy ({sub_src}) >>>>>')
            try_to_copy(sub_src, dst_root_path)
            # logger.info(f'<<<<< [Finish] to copy ({sub_src}) <<<<<')
        except Exception as e:
            logger.exception(e)
            return


def cp_exist_file(src, dst):
    logger.info(f'[Exist] ({src}) ({dst})')
    if is_same_files(src, dst):
        stat.skip_count += 1
        logger.info(f'[Skip] same size & modify_time')
    else:
        shutil.copy2(src, dst)
        stat.overwrite_list.append(src)
        logger.info(f'[Overwrite] ({dst})')
