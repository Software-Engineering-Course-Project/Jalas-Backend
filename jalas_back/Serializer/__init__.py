import json

from django.core import serializers


class SelectSerializer:

    @staticmethod
    def makeSerial(selects):
        selects_json = serializers.serialize('json', selects)
        selects_list = json.loads(selects_json)
        for index, val in enumerate(selects_list):
            selects_list[index]['fields']['agree'] = selects[index].getAgree if selects[index].agree else 0
            selects_list[index]['fields']['disAgree'] = selects[index].disAgree if selects[index].disAgree else 0
        return json.dumps(selects_list)