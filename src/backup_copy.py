# -*- coding:utf-8 -*-

import os
import shutil
import src.utils as utils
from src.config import handle_config
from src.logger import logger
from src.statistics import stat


class BackupCopy:
    NO_IGNORE = 0
    HIT_IGNORE = 1
    CONTAIN_IGNORE = 2

    def __init__(self, config):
        config, err = handle_config(config)
        if err:
            for e in err:
                logger.error(e)
            raise Exception('Errors in handling config. Please check log.')

        self.src_paths = config.backup_source
        self.ign_paths = config.backup_ignore
        self.dst_root_path = config.backup_destination

    def copy(self):
        for src in self.src_paths:
            try:
                logger.info(f'>>>>> [Begin] to copy ({src}) >>>>>')
                self.try_to_copy(src)
                logger.info(f'<<<<< [Finish] to copy ({src}) <<<<<\n')
            except Exception as e:
                logger.exception(e)
                return

    def try_to_copy(self, src):
        dst = utils.join_dst_path(src=src, dst_root=self.dst_root_path)
        # dst exist
        if os.path.exists(dst):
            if os.path.isdir(src):
                self.cp_exist_dir(src)
            else:
                self.cp_exist_file(src, dst)
        # dst not exist
        else:
            if os.path.isdir(src):
                self.cp_not_exist_dir(src, dst)
            else:
                self.cp_not_exist_file(src, dst)

    def cp_not_exist_dir(self, src, dst):
        if in_ignores(src, self.ign_paths) == BackupCopy.NO_IGNORE:
            shutil.copytree(src, dst)
            stat.copy_list.append(src)
            logger.info(f'[Copy] ({src}) -> ({dst})')
        elif in_ignores(src, self.ign_paths) == BackupCopy.CONTAIN_IGNORE:
            # Create new dir for current destination.
            os.makedirs(dst)
            logger.info(f'[Create] new directory ({dst})')
            # Let cp_exist_dir do recursive jobs.
            self.cp_exist_dir(src)
        else:
            return  # HIT_IGNORE

    def cp_not_exist_file(self, src, dst):
        if in_ignores(src, self.ign_paths) == BackupCopy.HIT_IGNORE:
            return
        # create new dir
        dst_parent_path = os.path.dirname(dst)
        if not os.path.exists(dst_parent_path):
            os.makedirs(dst_parent_path)
            logger.info(f'[Create] new directory ({dst_parent_path})')
        # copy file
        shutil.copy2(src, dst)
        stat.copy_list.append(src)
        logger.info(f'[Copy] ({src}) -> ({dst})')

    def cp_exist_dir(self, src):
        for sub_item in os.listdir(src):  # recursively try to copy sub-items
            sub_src = os.path.join(src, sub_item).replace('\\', '/')
            try:
                # logger.info(f'>>>>> [Begin] to copy ({sub_src}) >>>>>')
                self.try_to_copy(sub_src)
                # logger.info(f'<<<<< [Finish] to copy ({sub_src}) <<<<<\n')
            except Exception as e:
                logger.exception(e)
                return

    def cp_exist_file(self, src, dst):
        if in_ignores(src, self.ign_paths) == BackupCopy.HIT_IGNORE:
            return
        if are_same_files(src, dst):
            stat.skip_count += 1
            logger.info(f'[Skip] ({src})')
        else:
            shutil.copy2(src, dst)
            stat.overwrite_list.append(src)
            logger.info(f'[Overwrite] ({dst})')


def get_file_info(filepath: str):
    file_info = os.stat(filepath)
    return {
        'size': utils.format_byte(file_info.st_size),
        'access_time': utils.format_time(file_info.st_atime),
        'modify_time': utils.format_time(file_info.st_mtime),
        'create_time': utils.format_time(file_info.st_ctime)
    }


def are_same_files(fp1, fp2):
    f1, f2 = get_file_info(fp1), get_file_info(fp2)
    return f1['size'] == f2['size'] and f1['modify_time'] == f2['modify_time']


def in_ignores(src_path, ignore_paths):
    """
        more info: See src.config.handle_config
    """
    ignore_contained = [i for i in ignore_paths if i.startswith(src_path)]
    if not ignore_paths or not ignore_contained:
        return BackupCopy.NO_IGNORE

    if src_path in ignore_contained:  # e.g. src=D:/A/a.txt, ignore_contained=[D:/A/a.txt] (only one item)
        ignore_paths.remove(src_path)  # no use anymore
        logger.info(f'[Ignore] {src_path}')
        return BackupCopy.HIT_IGNORE

    return BackupCopy.CONTAIN_IGNORE  # e.g. src=D:/A, ignore_contained=[D:/A/a.txt, D:/A/b.txt]
