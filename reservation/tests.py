from django.test import TestCase
from poll.models import Poll, Select
from meeting.models import Meeting
import unittest
from unittest.mock import patch

# Create your tests here.
class SetDateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Meeting.objects.create(title='poll11')
        Poll.objects.create(title='poll 1', meeting_id='1')
        Select.objects.create(date='2222-02-22', startTime='2:2:1', endTime='3:3:3', poll_id='1')

    def test_selectIdIsGiven_setDateCalled_expectSetingDate(self):
        response = self.client.get('/api/reservation/set_date/1')
        self.assertEqual(response.status_code, 301)


class RoomsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Meeting.objects.create(title='poll11')
        Poll.objects.create(title='poll 1', meeting_id='1')
        Select.objects.create(date='2222-02-22', startTime='2:2:1', endTime='3:3:3', poll_id='1')


    @patch('requests.get')
    def test_selectIdIsGiven_setDateCalled_expectSetingDate(self, mock_get):
        mock_get.return_value.status_code = 500
        response = self.client.get('/api/reservation/available_room/1')
        self.assertEqual(response.status_code, 301)

    def test_selectIdIsGiven_setDateCalled_expectSetingDate(self):
        response = self.client.get('/api/reservation/available_room/1')
        self.assertEqual(response.status_code, 301)