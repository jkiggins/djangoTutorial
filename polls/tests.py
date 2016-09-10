from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

import datetime

from .models import Question


def create_question(question_text, days):
    '''Creates a question days in the future'''

    time = timezone.now() + datetime.timedelta(days=days)

    return Question.objects.create(question_text=question_text, pub_date=time)


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


class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        '''If no questions exist, the appropirate message should be displayed'''
        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")

        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        '''Questions with a pub_date in the past should be displayed'''
        create_question(question_text="Past Question.", days=-30)

        response=self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past Question.>'])

    def test_index_view_with_a_future_question(self):
        '''Questions with a pub_date in the future should not be displayed'''
        create_question(question_text="This is a future question", days=30)

        response = self.client.get(reverse('polls:index'))

        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        '''Make sure past question is displayed and future question isn't'''
        create_question(question_text="Past Question.", days=-30)
        create_question(question_text="This is a future question", days=30)

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past Question.>'])

    def test_index_view_with_two_past_questions(self):
        '''Make sure two past questions are displayed and ordered'''
        create_question(question_text="Past Question 2", days=-30)
        create_question(question_text="Past Question 1", days=-20)

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past Question 1>', '<Question: Past Question 2>'])


class QuestionDetailViewTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """The detail view of a question with a pub_date in the future should return a 404 not found."""

        future_question = create_question("This is a future question", 20)

        url = reverse(viewname='polls:detail', args=(future_question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """The detail view of a question with a pub_date in the past should display the question's text."""
        past_question = create_question("This is a past question", -20)

        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)

        self.assertContains(response, past_question.question_text)


class QuestionResultsViewTests(TestCase):
    def test_results_view_with_a_future_question(self):
        """The detail view of a question with a pub_date in the future should return a 404 not found."""

        future_question = create_question("This is a future question", 20)

        url = reverse(viewname='polls:results', args=(future_question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_results_view_with_a_past_question(self):
        """The detail view of a question with a pub_date in the past should display the question's text."""
        past_question = create_question("This is a past question", -20)

        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)

        self.assertContains(response, past_question.question_text)






