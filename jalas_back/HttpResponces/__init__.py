from django.http import HttpResponse


class HttpResponse500Error(HttpResponse):
    status_code = 500


class HttpResponse404Error(HttpResponse):
    status_code = 404


class HttpResponse401Error(HttpResponse):
    status_code = 401


class HttpResponse400Error(HttpResponse):
    status_code = 400

class HttpResponse405Error(HttpResponse):
    status_code = 405

class HttpResponse999Error(HttpResponse):
    status_code = 999