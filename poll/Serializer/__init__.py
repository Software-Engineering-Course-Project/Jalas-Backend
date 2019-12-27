import json

from django.core import serializers


class SelectSerializer:

    @staticmethod
    def makeSerial(selects):
        selects_json = serializers.serialize('json', selects)
        selects_list = json.loads(selects_json)
        for index, val in enumerate(selects_list):
            selects_list[index]['fields']['agree'] = selects[index].agree if selects[index].agree else 0
            selects_list[index]['fields']['disagree'] = selects[index].disagree if selects[index].disagree else 0
        return json.dumps(selects_list)

class CommentSerializer:

    @staticmethod
    def makeSerial(comments):
        comments_json = serializers.serialize('json', comments)
        comments_list = json.loads(comments_json)
        for index, val in enumerate(comments_list):
            comments_list[index]['fields']['username'] = comments[index].owner.username if comments[index].owner.username else 'Unknown'
        return json.dumps(comments_list)