from django.http import HttpResponse


class HttpResponce500Error(HttpResponse):
    status_code = 500


class HttpResponce404Error(HttpResponse):
    status_code = 404


class HttpResponce400Error(HttpResponse):
    status_code = 400