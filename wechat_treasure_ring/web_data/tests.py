# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import TestCase, RequestFactory
from wechat_response.models import *
from web_data.views import *
import json

# Create your tests here.
class test_ifregistered(TestCase):
	def setUp(self):
		self.user = RingUser.objects.create(
				user_id = "sheep94lion",
				nickname = "zhaoyi",
				headimgurl = "1.jpg",
				sex = "male",
				age = 21,
				height = 177,
				weight = 87,
				target = 10000,
				last_record = 12345,
				steps_totalused = 1355
		)
		self.factory = RequestFactory()

	def test_notregistered(self):
		request = self.factory.get('data/ifregistered/littlepig')
		response = ifregistered(request, "littlepig")
		self.assertEqual(response.status_code, 200)
		result = json.loads(response.content)
		self.assertEqual(result.get(u'ifregistered'), False)

	def test_doregistered(self):
		request = self.factory.get('data/ifregistered/sheep94lion')
		response = ifregistered(request, "sheep94lion")
		self.assertEqual(response.status_code, 200)
		result = json.loads(response.content.encode('utf-8'))
		self.assertEqual(result.get(u'ifregistered'), True)

	def test_nousers(self):
		self.user.delete()
		request = self.factory.get('data/ifregistered/littlepig')
		response = ifregistered(request, "littlepig")
		self.assertEqual(response.status_code, 200)
		result = json.loads(response.content)
		self.assertEqual(result.get(u'ifregistered'), False)

class test_saveuserbet(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		self.user = RingUser.objects.create(
				user_id = "sheep94lion",
				nickname = "zhaoyi",
				headimgurl = "1.jpg",
				sex = "male",
				age = 21,
				height = 177,
				weight = 87,
				target = 10000,
				last_record = 12345,
				steps_totalused = 0
			)
		self.subject = GuessSubject.objects.create(
				id=3,
				content='1',
				choiceA='1',
				choiceB='1',
				stepsA=0,
				stepsB=0,
				result='',
				disabled=False
			)

	def test_savesuccess(self):
		request = self.factory.get('data/saveuserbet?subid=3&openid=sheep94lion&steps=100&choice=A')
		response = save_user_bet(request)
		subject = GuessSubject.objects.all()[0]
		self.assertEqual(response.status_code, 200)
		self.assertEqual(subject.stepsA, 100)
		record = GuessInfomation.objects.all()[0]
		self.assertEqual(record.user_id, "sheep94lion")
		self.assertEqual(record.choice, 'A')


class test_get_guess_subject(TestCase):
	def setUp(self):
		self.factory = RequestFactory

	def test_

