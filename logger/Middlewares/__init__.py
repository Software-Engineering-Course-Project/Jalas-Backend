import time

from django.utils import timezone

from logger.models import Response, Throughput


def time_log_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        start_time = time.time()
        response = get_response(request)
        throughput = Throughput(create_date=timezone.now())
        throughput.save()
        end_time = time.time()
        response_time = Response(duration=(end_time - start_time))
        response_time.save()
        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware