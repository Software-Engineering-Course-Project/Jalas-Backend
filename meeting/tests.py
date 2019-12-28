from django.test import TestCase
from django.test import RequestFactory

# Create your tests here.
from django.test import Client
from django.urls import resolve
from poll.models import Poll, Select
from meeting.models import Meeting
from poll.Serializer import SelectSerializer
from .views import ShowMeeting
from rest_framework.test import APIRequestFactory

import json

# Create your tests here.

class MeetingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Meeting.objects.create(title='poll11')

    def test_first_name_max_length(self):
        meeting = Meeting.objects.get(id=1)
        max_length = meeting._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)


# class ShowMeetingTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         Meeting.objects.create(title='poll11')
#         Poll.objects.create(title='poll 1', meeting_id='1')
#         Select.objects.create(date='2222-02-22', startTime='2:2:1', endTime='3:3:3', poll_id='1')

    # def test_selectIdIsGiven_getMeetingCalled_expectMeetingInfo(self):
    #     response = self.client.get('/api/meeting/show_meeting/1')
    #     content = json.loads(response.content)
    #     # print(content[0]['fields']['title'])
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(content[0]['fields']['title'], 'poll11')