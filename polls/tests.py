from django.test import TestCase
from django.utils import timezone

import datetime

from .models import Question

class QuestionMethodTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        '''
        was_published_recently() should return False for questions whoes pub_date is in the future.
        '''

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        '''
        was_published_recently() should return False for questions > 1 day old
        '''
        time = timezone.now() - datetime.timedelta(days=30)

        past_question = Question(pub_date=time)

        self.assertEqual(past_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        '''
        was_published_recently() should return True for questions < 1 day old
        '''

        time = timezone.now() - datetime.timedelta(hours=1)

        recent_question = Question(pub_date=time)

        self.assertEqual(recent_question.was_published_recently(), True)


