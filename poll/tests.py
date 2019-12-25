from django.test import TestCase
from django.test import Client
from django.urls import resolve
from poll.models import Poll, Select
from meeting.models import Meeting
from django.contrib.auth.models import User
from poll.Serializer import SelectSerializer
import json

# Create your tests here.
class PollUrlsTest(TestCase):
    def test_polls_URL_connect_to_PollsView(self):
        resolver = resolve('/api/poll/polls/')
        self.assertEqual(resolver.view_name, 'poll.views.PollsView')

    def test_poll_URL_connect_to_PollView(self):
        resolver = resolve('/api/poll/poll/2')
        self.assertEqual(resolver.view_name, 'poll.views.PollView')


class PollModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Meeting.objects.create(title='poll11')
        Poll.objects.create(title='poll1', meeting_id='1')

    def test_first_name_max_length(self):
        poll = Poll.objects.get(id=1)
        max_length = poll._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)


class PollListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_polls = 2
        Meeting.objects.create(title='poll11')
        User.objects.create(username='test', password='test')
        for id in range(number_of_polls):
            Poll.objects.create(title=f'poll {id}', meeting_id='1')

    # def setUp(self):
        # print(User.objects.get(id=1).username)
        # print(User.objects.get(id=1).password)
        # response = self.client.get('api/auth/login/test/test/')
        # print(response)
        # self.token = response.data['access']
        # print(self.token)
        # self.api_authentication()

    # def api_authentication(self):
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_view_url_exists_at_desired_location_unauth(self):
        response = self.client.get('/api/poll/polls/')
        self.assertEqual(response.status_code, 401)

    def test_view_response_isvalid_unauth(self):
        # self.client.login(username="test", password="test")
        response = self.client.get('/api/poll/polls/')
        # content = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        # self.assertEqual(len(content), 2)

class PollViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Meeting.objects.create(title='poll11')
        Poll.objects.create(title='poll 1', meeting_id='1')

    def test_view_url_exists_at_desired_location_unauth(self):
        # self.client.login(username="test", password="test")
        response = self.client.get('/api/poll/poll/1')
        self.assertEqual(response.status_code, 401)

    def test_view_non_exists_poll_unauth(self):
        # self.client.login(username="test", password="test")
        response = self.client.get('/api/poll/poll/20')
        self.assertEqual(response.status_code, 401)

    def test_view_response_to_get_isvalid_unauth(self):
        self.client.login(username="test", password="test")
        response = self.client.get('/api/poll/poll/1')
        # content = json.loads(response.content)
        # print(content)
        self.assertEqual(response.status_code, 401)
        # self.assertEqual(len(content), 1)
        # self.assertEqual(content[0]['pk'], 1)

class CreatePollViewTest(TestCase):

    def test_view_url_exists_at_desired_location_unauth(self):
        content = {'title': 'meeting 1', 'text': '1', 'participants': ['a'],
                   'selects': [{'date': '2222-04-22', 'start_time': '12:09', 'end_time': '12:1'}]}
        self.client.login(username="test", password="test")
        response = self.client.post('/api/poll/create_poll', content)
        self.assertEqual(response.status_code, 301)

    def test_view_action_isvalid_unauth(self):
        content = {'title': 'meeting 1', 'text': '1', 'participants': ['a'],
                   'selects': [{'date': '2222-04-22', 'start_time': '12:09:00', 'end_time': '12:01:00'}]}
        self.client.login(username="test", password="test")
        response = self.client.post('/api/poll/create_poll', content)
        option = Select.objects.filter(poll_id=1)
        print(SelectSerializer.makeSerial(option))
        # self.assertEqual(option, 200)
        # self.assertEqual(len(option), 2)

class VoteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Meeting.objects.create(title='poll11')
        Poll.objects.create(title='poll 1', meeting_id='1')
        Select.objects.create(date='2222-02-22', startTime='2:2:1', endTime='3:3:3', poll_id='1')
        Select.objects.create(date='2019-02-22', startTime='2:2:1', endTime='3:3:3', poll_id='1')

    def setUp(self):
        self.content = {'selects' : {"1":1, "2":2}}

    # def test_view_url_exists_at_desired_location(self):
    #     self.client.login(username="test", password="test")
    #     response = self.client.post('/api/poll/vote/1', self.content)
    #     print(response.content)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_view_action_isvalid(self):
    #     self.client.login(username="test", password="test")
    #     response = self.client.post('/api/poll/vote/1', self.content)
    #     option = Select.objects.filter(poll_id=1)
    #     print(SelectSerializer.makeSerial(option))
    #     self.assertEqual(option, 200)
    #     self.assertEqual(len(content), 2)