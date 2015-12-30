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
                user_id="sheep94lion",
                nickname="zhaoyi",
                headimgurl="1.jpg",
                sex="male",
                age=21,
                height=177,
                weight=87,
                target=10000,
                last_record=12345,
                steps_totalused=1355
        )
        self.factory = RequestFactory()

    def test_NotRegistered(self):
        request = self.factory.get('data/ifregistered/littlepig')
        response = ifregistered(request, "littlepig")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result.get(u'ifregistered'), False)

    def test_DoRegistered(self):
        request = self.factory.get('data/ifregistered/sheep94lion')
        response = ifregistered(request, "sheep94lion")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.encode('utf-8'))
        self.assertEqual(result.get(u'ifregistered'), True)

    def test_NoUsers(self):
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
                user_id="sheep94lion",
                nickname="zhaoyi",
                headimgurl="1.jpg",
                sex="male",
                age=21,
                height=177,
                weight=87,
                target=10000,
                last_record=12345,
                steps_totalused=0
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

    def test_SaveSuccess(self):
        request = self.factory.get('data/saveuserbet?subid=3&openid=sheep94lion&steps=100&choice=A')
        response = save_user_bet(request)
        subject = GuessSubject.objects.all()[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(subject.stepsA, 100)
        record = GuessInfomation.objects.all()[0]
        self.assertEqual(record.user_id, "sheep94lion")
        self.assertEqual(record.choice, 'A')

    def test_SaveNoUser(self):
        request = self.factory.get('data/saveuserbet?subid=3&openid=eeeeee&steps=100&choice=A')
        response = save_user_bet(request)
        subject = GuessSubject.objects.all()[0]
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "failure")

class test_getguesssubject(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.subject1 = GuessSubject.objects.create(
            id=3,
            content="hello_not",
            choiceA="good",
            choiceB="bad",
            stepsA=0,
            stepsB=0,
            result="",
            disabled=False
        )
        self.subject2 = GuessSubject.objects.create(
            id=4,
            content="hello_dis",
            choiceA="good",
            choiceB="bad",
            stepsA=0,
            stepsB=0,
            result="A",
            disabled=True
        )
        self.subject3 = GuessSubject.objects.create(
            id=2,
            content="hello_no_result",
            choiceA="good",
            choiceB="bad",
            stepsA=0,
            stepsB=0,
            result="",
            disabled=True
        )

    def test_GetNotDisabled(self):
        request = self.factory.get('data/getguesssubject')
        response = get_guess_subject(request)
        self.assertContains(response, "hello_not", count=1, status_code=200)

    def test_GetDisabled(self):
        request = self.factory.get('data/getguesssubject')
        response = get_guess_subject(request)
        self.assertNotContains(response, "hello_dis", status_code=200)

    def test_GetNoResult(self):
        request = self.factory.get('data/getguesssubject')
        response = get_guess_subject(request)
        self.assertNotContains(response, "hello_no_result", status_code=200)


class test_freezeactivity(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.subject1 = GuessSubject.objects.create(
            id=3,
            content="hello_not",
            choiceA="good",
            choiceB="bad",
            stepsA=0,
            stepsB=0,
            result="",
            disabled=False
        )
        self.subject2 = GuessSubject.objects.create(
            id=4,
            content="hello_dis",
            choiceA="good",
            choiceB="bad",
            stepsA=0,
            stepsB=0,
            result="A",
            disabled=True
        )
        self.subject3 = GuessSubject.objects.create(
            id=2,
            content="hello_no_result",
            choiceA="good",
            choiceB="bad",
            stepsA=0,
            stepsB=0,
            result="",
            disabled=True
        )


    def test_FreezeNotFreezed(self):
        request = self.factory.get('data/freeze?subid=3')
        response = freeze_activity(request)
        self.assertContains(response, "success", count=1, status_code=200)
        self.subject1 = GuessSubject.objects.filter(id=3)[0]
        self.assertEqual(self.subject1.disabled, True)


    def test_FreezeFreezed(self):
        request = self.factory.get('data/freeze?subid=4')
        response = freeze_activity(request)
        self.assertContains(response, "success", count=1, status_code=200)
        self.subject2 = GuessSubject.objects.filter(id=4)[0]
        self.assertEqual(self.subject2.disabled, True)


    def test_FreezeGetResult(self):
        request = self.factory.get('data/freeze?subid=2')
        response = freeze_activity(request)
        self.assertContains(response, "success", count=1, status_code=200)
        self.subject3 = GuessSubject.objects.filter(id=2)[0]
        self.assertEqual(self.subject3.disabled, True)

    def test_FreezeNotExisted(self):
        request = self.factory.get('data/freeze?subid=100')
        response = freeze_activity(request)
        self.assertContains(response, "failure", count=1, status_code=200)

class test_addguessobject(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_AddGuessObject(self):
        request = self.factory.post('data/addguesssubject', {'content':'hello', 'choiceA':'good', 'choiceB':'bad'})
        response = add_guess_subject(request)
        self.assertContains(response, "success", count=1, status_code=200)
        subject = GuessSubject.objects.filter(id=1)
        self.assertNotEqual(subject, [])
        self.assertEqual(subject[0].content, "hello")

    def test_AddGuessObjectNotComplete(self):
        request = self.factory.post('data/addguesssubject', {'content':'world'})
        response = add_guess_subject(request)
        self.assertContains(response, "failure", count=1, status_code=200)
        subject = GuessSubject.objects.filter(id=1)
        self.assertQuerysetEqual(subject, [])

class test_calculate(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = RingUser.objects.create(
                id=1,
                user_id="czj",
                nickname="zhaoyi",
                headimgurl="1.jpg",
                sex="male",
                age=21,
                height=177,
                weight=87,
                target=10000,
                last_record=12345,
                steps_totalused=100
        )
        self.user2 = RingUser.objects.create(
                id=2,
                user_id="xja",
                nickname="zhaoyi",
                headimgurl="1.jpg",
                sex="male",
                age=21,
                height=177,
                weight=87,
                target=10000,
                last_record=12345,
                steps_totalused=200
        )
        self.information1 = GuessInfomation.objects.create(
            id=1,
            user_id="czj",
            sub_id=1,
            choice='A',
            steps=15
        )
        self.information2 = GuessInfomation.objects.create(
            id=2,
            user_id="czj",
            sub_id=2,
            choice='B',
            steps=20
        )
        self.information3 = GuessInfomation.objects.create(
            id=3,
            user_id="czj",
            sub_id=3,
            choice='B',
            steps=30
        )
        self.information4 = GuessInfomation.objects.create(
            id=4,
            user_id="xja",
            sub_id=1,
            choice='B',
            steps=17
        )
        self.information5 = GuessInfomation.objects.create(
            id=5,
            user_id="xja",
            sub_id=2,
            choice='A',
            steps=16
        )
        self.information6 = GuessInfomation.objects.create(
            id=6,
            user_id="xja",
            sub_id=3,
            choice='B',
            steps=18
        )
        self.subject1 = GuessSubject.objects.create(
            id=1,
            content="hello_not",
            choiceA="good_not",
            choiceB="bad_not",
            stepsA=15,
            stepsB=17,
            result="",
            disabled=False
        )
        self.subject2 = GuessSubject.objects.create(
            id=2,
            content="hello_dis",
            choiceA="good_dis",
            choiceB="bad_dis",
            stepsA=16,
            stepsB=20,
            result="A",
            disabled=True
        )
        self.subject3 = GuessSubject.objects.create(
            id=3,
            content="hello_no_result",
            choiceA="good_no_result",
            choiceB="bad_no_result",
            stepsA=0,
            stepsB=48,
            result="",
            disabled=True
        )

    def test_CalculateNotDisabled(self):
        request = self.factory.get('data/calculate?subid=1&choice=A')
        response = calculate(request)
        self.assertContains(response, "failure")

    def test_CalculateNormalA(self):
        request = self.factory.get('data/calculate?subid=3&choice=A')
        response = calculate(request)
        self.assertContains(response, "success")
        user_info1 = RingUser.objects.filter(id=1)[0]
        user_info2 = RingUser.objects.filter(id=2)[0]
        self.assertEqual(user_info1.steps_totalused, 100)
        self.assertEqual(user_info2.steps_totalused, 200)

    def test_CalculateNormalB(self):
        request = self.factory.get('data/calculate?subid=3&choice=B')
        response = calculate(request)
        self.assertContains(response, "success")
        user_info1 = RingUser.objects.filter(id=1)[0]
        user_info2 = RingUser.objects.filter(id=2)[0]
        self.assertEqual(user_info1.steps_totalused, 70)
        self.assertEqual(user_info2.steps_totalused, 182)

    def test_CalculateAlreadyCalculated(self):
        request = self.factory.get('data/calculate?subid=2&choice=B')
        response = calculate(request)
        self.assertContains(response, "already calculated")
        user_info1 = RingUser.objects.filter(id=1)[0]
        user_info2 = RingUser.objects.filter(id=2)[0]
        self.assertEqual(user_info1.steps_totalused, 100)
        self.assertEqual(user_info2.steps_totalused, 200)


class test_steps_info(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = RingUser.objects.create(
                id=1,
                user_id = "czj",
                nickname = "zhaoyi",
                headimgurl = "1.jpg",
                sex = "male",
                age = 21,
                height = 177,
                weight = 87,
                target = 10000,
                last_record = 12345,
                steps_totalused = 100
        )

    def test_GetStepsInfo(self):
        request = self.factory.get('data/stepsinfo?openid=czj')
        response = steps_info(request)
        data = json.loads(response.content)
        self.assertEqual(isinstance(data["total"], int), True)
        self.assertEqual(isinstance(data["left"], int), True)

    def test_GetStepsInfo(self):
        request = self.factory.get('data/stepsinfo?openid=eeee')
        response = steps_info(request)
        self.assertContains(response, "no user")


class test_follow(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = RingUser.objects.create(
                id=1,
                user_id="czj",
                nickname="zhaoyi",
                headimgurl="1.jpg",
                sex="male",
                age=21,
                height=177,
                weight=87,
                target=10000,
                last_record=12345,
                steps_totalused=100
        )
        self.user2 = RingUser.objects.create(
                id=2,
                user_id="xja",
                nickname="zhaoyi",
                headimgurl="1.jpg",
                sex="male",
                age=21,
                height=177,
                weight=87,
                target=10000,
                last_record=12345,
                steps_totalused=200
        )

    def test_Follow(self):
        message = "czj@xja"
        request = self.factory.get('data/addfollow')
        response = add_follow(request, message)
        self.assertContains(response, "OK", count=1, status_code=200)
        data_none = RecordAttention.objects.filter(source_user_id='xja', target_user_id='czj')
        data = RecordAttention.objects.filter(source_user_id='czj', target_user_id='xja')
        self.assertEqual(len(data), 1)
        self.assertEqual(len(data_none), 0)
        message = "xja@czj"
        request = self.factory.get('data/cancelfollow')
        response = cancel_follow(request, message)
        self.assertContains(response, "OK", count=1, status_code=200)
        data_none = RecordAttention.objects.filter(source_user_id='xja', target_user_id='czj')
        data = RecordAttention.objects.filter(source_user_id='czj', target_user_id='xja')
        self.assertEqual(len(data), 1)
        self.assertEqual(len(data_none), 0)
        message = "czj@xja"
        request = self.factory.get('data/cancelfollow')
        response = cancel_follow(request, message)
        self.assertContains(response, "OK", count=1, status_code=200)
        data_none = RecordAttention.objects.filter(source_user_id='xja', target_user_id='czj')
        data = RecordAttention.objects.filter(source_user_id='czj', target_user_id='xja')
        self.assertEqual(len(data_none), 0)
        self.assertEqual(len(data), 0)


class test_Game(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = RingUser.objects.create(
                id=1,
                user_id="czj",
                nickname="zhaoyi",
                headimgurl="1.jpg",
                sex="male",
                age=21,
                height=177,
                weight=87,
                target=10000,
                last_record=12345,
                steps_totalused=100
        )
        self.user2 = RingUser.objects.create(
                id=2,
                user_id="xja",
                nickname="zhaoyi",
                headimgurl="1.jpg",
                sex="male",
                age=21,
                height=177,
                weight=87,
                target=10000,
                last_record=12345,
                steps_totalused=200
        )
        self.birduser1 = BirdUser.objects.create(
            openid="czj",
            steps_used=500,
            score_today=1000,
            score_total=4000
            )
        self.birduser2 = BirdUser.objects.create(
            openid="xja",
            steps_used=600,
            score_today=1500,
            score_total=2000
            )
        self.jumpuser1 = JumpUser.objects.create(
        	openid="czj",
            steps_used=500,
            score_today=1000,
            score_total=4000
            )
        self.jumpuser2 = JumpUser.objects.create(
            openid="xja",
            steps_used=600,
            score_today=1500,
            score_total=2000
            )

    def test_StartGame(self):
        request = self.factory.get('data/startgame?openid=233&game=bird')
        response = start_game(request)
        self.assertEquals((json.loads(response.content))["result"], "nouser")
        request = self.factory.get('data/startgame?openid=czj&game=bird')
        response = start_game(request)
        gameuser = RingUser.objects.get(user_id="czj")
        self.assertEquals(gameuser.steps_totalused, 1100)
        gameuser = BirdUser.objects.get(openid="czj")
        self.assertEquals(gameuser.steps_used, 1500)
        self.assertEquals((json.loads(response.content))["result"], "success")
        request = self.factory.get('data/startgame?openid=xja&game=jump')
        response = start_game(request)
        self.assertEquals((json.loads(response.content))["result"], "success")
        gameuser = RingUser.objects.get(user_id="xja")
        self.assertEquals(gameuser.steps_totalused, 1200)
        gameuser = JumpUser.objects.get(openid="xja")
        self.assertEquals(gameuser.steps_used, 1600)


    def test_EndGame(self):
        request = self.factory.get('data/endgame?openid=233&game=bird&score=300')
        response = end_game(request)
        self.assertContains(response, "no user")

        gameuser = BirdUser.objects.get(openid="czj")
        score_before_today = gameuser.score_today
        score_before_total = gameuser.score_total
        request = self.factory.get('data/endgame?openid=czj&game=bird&score=400')
        response = end_game(request)
        gameuser = BirdUser.objects.get(openid="czj")
        self.assertEquals(gameuser.score_today, score_before_today + 400)
        self.assertEquals(gameuser.score_total, score_before_total + 400)
        self.assertEquals((json.loads(response.content))["result"], "success")

        gameuser = JumpUser.objects.get(openid="xja")
        score_before_today = gameuser.score_today
        score_before_total = gameuser.score_total
        request = self.factory.get('data/endgame?openid=xja&game=jump&score=200')
        response = end_game(request)
        gameuser = JumpUser.objects.get(openid="xja")
        self.assertEquals(gameuser.score_today, score_before_today + 200)
        self.assertEquals(gameuser.score_total, score_before_total + 200)
        self.assertEquals((json.loads(response.content))["result"], "success")


    def test_IngameRank(self):
        request = self.factory.get('data/ingamerank?openid=233&game=bird')
        response = ingame_rank(request)
        data = json.loads(response.content)
        self.assertEquals(len(data["today"]), 0)
        self.assertEquals(len(data["total"]), 0)

        request = self.factory.get('data/ingamerank?openid=czj&game=bird')
        response = ingame_rank(request)
        data = json.loads(response.content)
        self.assertEquals(len(data["today"]), 2)
        self.assertEquals(len(data["total"]), 2)
        self.assertLessEqual(data["today"][1]["score"], data["today"][0]["score"])
        self.assertLessEqual(data["total"][1]["score"], data["total"][0]["score"])

        request = self.factory.get('data/ingamerank?openid=xja&game=jump')
        response = ingame_rank(request)
        data = json.loads(response.content)
        self.assertEquals(len(data["today"]), 2)
        self.assertEquals(len(data["total"]), 2)
        self.assertLessEqual(data["today"][1]["score"], data["today"][0]["score"])
        self.assertLessEqual(data["total"][1]["score"], data["total"][0]["score"])

    def test_GameRank(self):
        request = self.factory.get('data/gamerank?openid=233')
        response = get_game_rank(request)
        self.assertContains(response, "User Not Exists")

        request = self.factory.get('data/gamerank?openid=czj')
        response = get_game_rank(request)
        data = json.loads(response.content)
        self.assertEquals(len(data["today_bird"]), 2)
        self.assertEquals(len(data["total_bird"]), 2)
        self.assertLessEqual(data["today_bird"][1]["score"], data["today_bird"][0]["score"])
        self.assertLessEqual(data["total_bird"][1]["score"], data["total_bird"][0]["score"])

        request = self.factory.get('data/gamerank?openid=xja')
        response = get_game_rank(request)
        data = json.loads(response.content)
        self.assertEquals(len(data["today_jump"]), 2)
        self.assertEquals(len(data["total_jump"]), 2)
        self.assertLessEqual(data["today_jump"][1]["score"], data["today_jump"][0]["score"])
        self.assertLessEqual(data["total_jump"][1]["score"], data["total_jump"][0]["score"])

class test_more_user_Game(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = RingUser.objects.create(
                id=1,
                user_id="czj",
                nickname="zhaoyi",
                headimgurl="1.jpg",
                sex="male",
                age=21,
                height=177,
                weight=87,
                target=10000,
                last_record=12345,
                steps_totalused=100
        )
        self.user2 = RingUser.objects.create(
                id=2,
                user_id="xja",
                nickname="zhaoyi",
                headimgurl="1.jpg",
                sex="male",
                age=21,
                height=177,
                weight=87,
                target=10000,
                last_record=12345,
                steps_totalused=200
        )
        self.birduser1 = BirdUser.objects.create(
            openid="czj",
            steps_used=500,
            score_today=1000,
            score_total=4000
            )
        self.birduser2 = BirdUser.objects.create(
            openid="xja",
            steps_used=600,
            score_today=1500,
            score_total=2000
            )
        self.jumpuser1 = JumpUser.objects.create(
        	openid="czj",
            steps_used=500,
            score_today=1000,
            score_total=4000
            )
        self.jumpuser2 = JumpUser.objects.create(
            openid="xja",
            steps_used=600,
            score_today=1500,
            score_total=2000
            )
        self.user3 = RingUser.objects.create(
                id=3,
                user_id="zy",
                nickname="zhaoyi",
                headimgurl="1.jpg",
                sex="male",
                age=21,
                height=177,
                weight=87,
                target=10000,
                last_record=12345,
                steps_totalused=100
        )
        self.user4 = RingUser.objects.create(
                id=4,
                user_id="zzc",
                nickname="zhaoyi",
                headimgurl="1.jpg",
                sex="male",
                age=21,
                height=177,
                weight=87,
                target=10000,
                last_record=12345,
                steps_totalused=200
        )
        self.birduser3 = BirdUser.objects.create(
            openid="zy",
            steps_used=500,
            score_today=1250,
            score_total=4600
            )
        self.birduser4 = BirdUser.objects.create(
            openid="zzc",
            steps_used=600,
            score_today=1450,
            score_total=3700
            )
        self.jumpuser3 = JumpUser.objects.create(
        	openid="zy",
            steps_used=500,
            score_today=1350,
            score_total=3800
            )
        self.jumpuser4 = JumpUser.objects.create(
            openid="zzc",
            steps_used=600,
            score_today=1650,
            score_total=3900
            )
        self.user5 = RingUser.objects.create(
                id=5,
                user_id="zhaoyi",
                nickname="zhaoyi",
                headimgurl="1.jpg",
                sex="male",
                age=21,
                height=177,
                weight=87,
                target=10000,
                last_record=12345,
                steps_totalused=100
        )
        self.user6 = RingUser.objects.create(
                id=6,
                user_id="zhuzichen",
                nickname="zhaoyi",
                headimgurl="1.jpg",
                sex="male",
                age=21,
                height=177,
                weight=87,
                target=10000,
                last_record=12345,
                steps_totalused=200
        )
        self.birduser5 = BirdUser.objects.create(
            openid="zhaoyi",
            steps_used=500,
            score_today=1500,
            score_total=3300
            )
        self.birduser6 = BirdUser.objects.create(
            openid="zhuzichen",
            steps_used=600,
            score_today=1200,
            score_total=2400
            )
        self.jumpuser5 = JumpUser.objects.create(
        	openid="zhaoyi",
            steps_used=500,
            score_today=1300,
            score_total=2600
            )
        self.jumpuser6 = JumpUser.objects.create(
            openid="zhuzichen",
            steps_used=600,
            score_today=1350,
            score_total=5000
            )

    def test_IngameRankMore(self):
        request = self.factory.get('data/ingamerank?openid=233&game=bird')
        response = ingame_rank(request)
        data = json.loads(response.content)
        self.assertEquals(len(data["today"]), 0)
        self.assertEquals(len(data["total"]), 0)

        request = self.factory.get('data/ingamerank?openid=czj&game=bird')
        response = ingame_rank(request)
        data = json.loads(response.content)
        self.assertEquals(len(data["today"]), 4)
        self.assertEquals(len(data["total"]), 4)
        self.assertLessEqual(data["today"][1]["score"], data["today"][0]["score"])
        self.assertLessEqual(data["total"][1]["score"], data["total"][0]["score"])
        self.assertLessEqual(data["today"][2]["score"], data["today"][1]["score"])
        self.assertLessEqual(data["total"][2]["score"], data["total"][1]["score"])
        self.assertLessEqual(data["today"][3]["score"], data["today"][2]["score"])
        self.assertLessEqual(data["total"][3]["score"], data["total"][2]["score"])

        request = self.factory.get('data/ingamerank?openid=xja&game=jump')
        response = ingame_rank(request)
        data = json.loads(response.content)
        self.assertEquals(len(data["today"]), 4)
        self.assertEquals(len(data["total"]), 4)
        self.assertLessEqual(data["today"][1]["score"], data["today"][0]["score"])
        self.assertLessEqual(data["total"][1]["score"], data["total"][0]["score"])
        self.assertLessEqual(data["today"][2]["score"], data["today"][1]["score"])
        self.assertLessEqual(data["total"][2]["score"], data["total"][1]["score"])
        self.assertLessEqual(data["today"][3]["score"], data["today"][2]["score"])
        self.assertLessEqual(data["total"][3]["score"], data["total"][2]["score"])

    def test_GameRankMore(self):
        request = self.factory.get('data/ingamerank?openid=233')
        response = get_game_rank(request)
        self.assertContains(response, "User Not Exists")

        request = self.factory.get('data/ingamerank?openid=czj')
        response = get_game_rank(request)
        data = json.loads(response.content)
        self.assertEquals(len(data["today_bird"]), 6)
        self.assertEquals(len(data["total_bird"]), 6)
        self.assertLessEqual(data["today_bird"][1]["score"], data["today_bird"][0]["score"])
        self.assertLessEqual(data["total_bird"][1]["score"], data["total_bird"][0]["score"])
        self.assertLessEqual(data["today_bird"][2]["score"], data["today_bird"][1]["score"])
        self.assertLessEqual(data["total_bird"][2]["score"], data["total_bird"][1]["score"])
        self.assertLessEqual(data["today_bird"][3]["score"], data["today_bird"][2]["score"])
        self.assertLessEqual(data["total_bird"][3]["score"], data["total_bird"][2]["score"])
        self.assertLessEqual(data["today_bird"][4]["score"], data["today_bird"][3]["score"])
        self.assertLessEqual(data["total_bird"][4]["score"], data["total_bird"][3]["score"])
        self.assertLessEqual(data["today_bird"][5]["score"], data["today_bird"][4]["score"])
        self.assertLessEqual(data["total_bird"][5]["score"], data["total_bird"][4]["score"])

        request = self.factory.get('data/ingamerank?openid=xja')
        response = get_game_rank(request)
        data = json.loads(response.content)
        self.assertEquals(len(data["today_jump"]), 6)
        self.assertEquals(len(data["total_jump"]), 6)
        self.assertLessEqual(data["today_jump"][1]["score"], data["today_jump"][0]["score"])
        self.assertLessEqual(data["total_jump"][1]["score"], data["total_jump"][0]["score"])
        self.assertLessEqual(data["today_jump"][2]["score"], data["today_jump"][1]["score"])
        self.assertLessEqual(data["total_jump"][2]["score"], data["total_jump"][1]["score"])
        self.assertLessEqual(data["today_jump"][3]["score"], data["today_jump"][2]["score"])
        self.assertLessEqual(data["total_jump"][3]["score"], data["total_jump"][2]["score"])
        self.assertLessEqual(data["today_jump"][4]["score"], data["today_jump"][3]["score"])
        self.assertLessEqual(data["total_jump"][4]["score"], data["total_jump"][3]["score"])
        self.assertLessEqual(data["today_jump"][5]["score"], data["today_jump"][4]["score"])
        self.assertLessEqual(data["total_jump"][5]["score"], data["total_jump"][4]["score"])

class test_autosave(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = RingUser.objects.create(
                id=1,
                user_id="czj",
                nickname="zhaoyi",
                headimgurl="1.jpg",
                sex="male",
                age=21,
                height=177,
                weight=87,
                target=10000,
                last_record=12345,
                steps_totalused=100
        )
        self.user2 = RingUser.objects.create(
                id=2,
                user_id="xja",
                nickname="zhaoyi",
                headimgurl="1.jpg",
                sex="male",
                age=21,
                height=177,
                weight=87,
                target=10000,
                last_record=12345,
                steps_totalused=200
        )
        self.information1 = GuessInfomation.objects.create(
            id=1,
            user_id="czj",
            sub_id=1,
            choice='A',
            steps=15
        )
        self.information2 = GuessInfomation.objects.create(
            id=2,
            user_id="czj",
            sub_id=2,
            choice='B',
            steps=20
        )
        self.information3 = GuessInfomation.objects.create(
            id=3,
            user_id="czj",
            sub_id=3,
            choice='B',
            steps=30
        )
        self.information4 = GuessInfomation.objects.create(
            id=4,
            user_id="xja",
            sub_id=1,
            choice='B',
            steps=17
        )
        self.information5 = GuessInfomation.objects.create(
            id=5,
            user_id="xja",
            sub_id=2,
            choice='A',
            steps=16
        )
        self.information6 = GuessInfomation.objects.create(
            id=6,
            user_id="xja",
            sub_id=3,
            choice='B',
            steps=18
        )
        self.subject1 = GuessSubject.objects.create(
            id=1,
            content="hello_not",
            choiceA="good_not",
            choiceB="bad_not",
            stepsA=15,
            stepsB=17,
            result="",
            disabled=False
        )
        self.subject2 = GuessSubject.objects.create(
            id=2,
            content="hello_dis",
            choiceA="good_dis",
            choiceB="bad_dis",
            stepsA=16,
            stepsB=20,
            result="A",
            disabled=True
        )
        self.subject3 = GuessSubject.objects.create(
            id=3,
            content="hello_no_result",
            choiceA="good_no_result",
            choiceB="bad_no_result",
            stepsA=0,
            stepsB=48,
            result="",
            disabled=True
        )

    def test_SleepSaveSucceed(self):
        request = self.factory.get('data/autosave?sleep=1&exercise_and_time=0')
        response = auto_save(request)
        self.assertContains(response, "success", count=1, status_code=200)
        data = RecordByDay.objects.all()
        self.assertEqual(len(data), 60)

    def test_ExerciseSaveSucceed(self):
        request = self.factory.get('data/autosave?sleep=0&exercise_and_time=1')
        response = auto_save(request)
        self.assertContains(response, "success", count=1, status_code=200)
        data = RecordByDay.objects.all()
        self.assertEqual(len(data), 60)

    def test_DeleteResultedActivity(self):
        request = self.factory.get('data/autosave?sleep=0&exercise_and_time=1')
        response = auto_save(request)
        self.assertContains(response, "success", count=1, status_code=200)
        subject = GuessSubject.objects.all()
        info = GuessInfomation.objects.all()
        self.assertIn(self.subject1, subject)
        self.assertNotIn(self.subject2, subject)
        self.assertIn(self.subject3, subject)
        self.assertIn(self.information1, info)
        self.assertIn(self.information3, info)
        self.assertNotIn(self.information2, info)
        self.assertNotIn(self.information5, info)
        self.assertIn(self.information4, info)
        self.assertIn(self.information6, info)

    def test_TimeLineSaveSucceed(self):
        request = self.factory.get('data/autosave?sleep=0&exercise_and_time=1')
        response = auto_save(request)
        self.assertContains(response, "success", count=1, status_code=200)
        data = ActivityRecord.objects.all()
        self.assertEqual(len(data), 60)


class test_register(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user2 = RingUser.objects.create(
                id=2,
                user_id="xja",
                nickname="zhaoyi",
                headimgurl="1.jpg",
                sex="male",
                age=21,
                height=177,
                weight=87,
                target=10000,
                last_record=12345,
                steps_totalused=200
        )

    def test_NormalRegister(self):
        request = self.factory.post('data/register?sex=male&age=20&height=182&weight=75&goal_step=100&openid=czj')
        response = register(request)
        self.assertContains(response, "add info successfully", count=1, status_code=200)
        user = RingUser.objects.filter(user_id="czj")
        self.assertEqual(len(user), 1)
        self.assertEqual(user[0].sex, "male")
        self.assertEqual(user[0].user_id, "czj")

    def test_AlreadyRegistered(self):
        request = self.factory.post('data/register?sex=female&age=20&height=182&weight=75&goal_step=100&openid=xja')
        response = register(request)
        self.assertContains(response, "add info successfully", count=1, status_code=200)
        user = RingUser.objects.all()
        self.assertEqual(len(user), 1)
        self.assertNotEqual(user[0].sex, "male")
        self.assertEqual(user[0].sex, "female")
        self.assertNotEqual(user[0].weight, 87)
        self.assertEqual(user[0].weight, 75)
        self.assertEqual(user[0].user_id, "xja")

    def test_NotComplete(self):
        request = self.factory.post('data/register?sex=male&height=182&weight=75&goal_step=100&openid=xja')
        response = register(request)
        self.assertContains(response, "failure", count=1, status_code=200)


class test_datachart(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user2 = RingUser.objects.create(
                id=2,
                user_id="xja",
                nickname="zhaoyi",
                headimgurl="1.jpg",
                sex="male",
                age=21,
                height=177,
                weight=87,
                target=10000,
                last_record=12345,
                steps_totalused=200
        )


    def test_GetSleepDataExistShaveData(self):
        request1 = self.factory.get('data/autosave?sleep=1&exercise_and_time=0')
        request2 = self.factory.get('data/getsleepdata?openid=xja')
        auto_save(request1)
        response = get_sleepdata(request2)
        data = json.loads(response.content)
        self.assertEqual(data["data"]["isnull"], False)

    def test_GetSleepDataNotExists(self):
        request = self.factory.get('data/getsleepdata?openid=czj')
        response = get_sleepdata(request)
        data = json.loads(response.content)
        self.assertEqual(data["isnull"], True)

    def test_GetSleepDataExistsNoData(self):
        request = self.factory.get('data/getsleepdata?openid=xja')
        response = get_sleepdata(request)
        data = json.loads(response.content)
        self.assertEqual(data["data"]["isnull"], True)

    def test_GetExerciseDataExistsHaveData(self):
        request1 = self.factory.get('data/autosave?sleep=0&exercise_and_time=1')
        request2 = self.factory.get('data/getsportsdata?openid=xja')
        auto_save(request1)
        response = get_sportsdata(request2)
        data = json.loads(response.content)
        self.assertEqual(data["data"]["isnull"], False)

    def test_GetExerciseDataNotExists(self):
        request = self.factory.get('data/getsportsdata?openid=czj')
        response = get_sportsdata(request)
        data = json.loads(response.content)
        self.assertEqual(data["isnull"], True)

    def test_GetExerciseDataExistsNoData(self):
        request = self.factory.get('data/getsportsdata?openid=xja')
        response = get_sportsdata(request)
        data = json.loads(response.content)
        self.assertEqual(data["data"]["isnull"], True)

    def test_GetTimeLineDataExistsHaveData(self):
        request1 = self.factory.get('data/autosave?sleep=0&exercise_and_time=1')
        request2 = self.factory.get('data/getTimeLineData?openid=xja')
        auto_save(request1)
        response = get_sportsdata(request2)
        data = json.loads(response.content)
        self.assertEqual(data["data"]["isnull"], False)

    def test_GetTimeLineDataNotExists(self):
        request = self.factory.get('data/getTimeLineData?openid=czj')
        response = get_sportsdata(request)
        data = json.loads(response.content)
        self.assertEqual(data["isnull"], True)

    def test_GetTimeLineDataExistsNoData(self):
        request = self.factory.get('data/getTimeLineData?openid=xja')
        response = get_sportsdata(request)
        data = json.loads(response.content)
        self.assertEqual(data["data"]["isnull"], True)