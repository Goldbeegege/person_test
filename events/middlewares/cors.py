# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2018/12/28 19:43

class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class CorsMiddleWares(MiddlewareMixin):
    def process_response(self,request,response):
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Origin"] = "http://127.0.0.1:8080"
        response["Access-Control-Allow-Methods"] = "DELETE"
        if request.method == "OPTIONS":
            response["Access-Control-Allow-Headers"] = "content-type"
        return response