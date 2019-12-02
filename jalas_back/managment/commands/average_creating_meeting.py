from django.core.management import BaseCommand

from jalas_back.models import ReservationTime


class Command(BaseCommand):

    help = 'Get average time of each reservation from set date and time to set room and finish reservation'

    def handle(self, *args, **options):
        overall_time = 0
        reservatoinTimes = ReservationTime.objects.all()
        for reserve in reservatoinTimes:
            start = reserve.reservationStartTime.timestamp()
            end = reserve.reservationEndTime.timestamp()
            overall_time += (end - start)
        print('Average time duration for each reservation', overall_time / len(reservatoinTimes))