# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2019/1/7 20:01


class BaseResponse(Exception):
    def __init__(self):
        self.msg = None
        self.code = 1000
        self.error = ""

    @property
    def response_dict(self):
        return self.__dict__