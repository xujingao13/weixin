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
