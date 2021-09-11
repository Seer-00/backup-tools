# -*- coding:utf-8 -*-

import time


class Statistic:
    def __init__(self):
        self.mode = 'COPY'
        self.same = 'SKIP'
        self.existence = 'OVERWRITE'

        # self.source_count = 0
        # self.ignore_count = 0
        self.skip_count = 0
        # self.copy_count = 0
        # self.overwrite_count = 0

        self.copy_list = []
        self.overwrite_list = []
        self.warning_list = []

        self.start_time = time.time()
        self.end_time = None

    def get_duration(self):
        self.end_time = time.time()
        return f'{self.end_time - self.start_time:.2f} s'

    def get_overwrite_count(self):
        return len(self.overwrite_list)

    def get_copy_count(self):
        return len(self.copy_list)

    def get_warning_count(self):
        return len(self.warning_list)


stat = Statistic()
