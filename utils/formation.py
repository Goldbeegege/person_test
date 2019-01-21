# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2019/1/14 21:07

import json

class StringFormation:
    def __init__(self,json_string):
        self.string = json_string

    @property
    def data(self):
        return json.loads(self.string)

