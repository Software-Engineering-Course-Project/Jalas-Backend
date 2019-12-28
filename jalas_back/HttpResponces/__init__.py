from django.http import HttpResponse


class HttpResponse500Error(HttpResponse):
    status_code = 500


class HttpResponse404Error(HttpResponse):
    status_code = 404


class HttpResponse400Error(HttpResponse):
    status_code = 400

class HttpResponse405Error(HttpResponse):
    status_code = 405

class HttpResponse407Error(HttpResponse):
    status_code = 407