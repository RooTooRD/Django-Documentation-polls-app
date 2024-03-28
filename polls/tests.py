from django.test import TestCase
from django.utils import timezone
import datetime
from .models import Question
from django.urls import reverse


class QuestionModelTest(TestCase):
    def test_was_recently_published_future_question(self):
        
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_recently_published_old_question(self):

        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_recently_published_recent_question(self):

        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)



def create_question(text, days):
    time = timezone.now() + datetime.timedelta(days)
    return Question.objects.create(question_text=text, pub_date=time)


class QusetionIndexViweTest(TestCase):
    # this is a test for the index view that check if the view return also futur question
    # futur question are the question that have pub_date > timezone() and which will be 
    # displyed when their pub_date come (it's like a timer) 

    def test_no_question(self):
        # check the case where no question is there 
        # Normal --> 200 status code with 'No polls are availble.' response and no question displayed

        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_questions_list'], [])

    def test_futur_question(self):
        # check the case where there is one futur question in the database
        # Normal --> no question displayed (because there only the futur question in the database)

        create_question(text='futur question', days=1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_questions_list'], [])

    def test_past_question(self):
        # check the case where there is past question in the database
        # Normal --> the question should be displayed 

        question = create_question(text='futur question', days=-1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_questions_list'], [question], )

    def test_futur_and_past_question(self):
        # check the case where there is one futur question and one past question in the database
        # Normal --> display past question only

        question = create_question(text='past question', days=-1)
        create_question(text='futur question', days=1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_questions_list'], [question], )

    def test_two_past_question(self):
        # check the case where there is two past question in the database
        # Normal --> display two question

        question1 = create_question(text='past question 1', days=-1)
        question2 = create_question(text='past question 2', days=-2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_questions_list'], [question1, question2],)


class QuestionDetailViewTest(TestCase):

    def test_futur_question(self):
        question = create_question(text='futur question', days=1)
        response = self.client.get(reverse('polls:detail', args=(question.id,) ))
        self.assertEqual(response.status_code, 404)


    def test_past_question(self):
        question = create_question(text='past question', days=-1)
        response = self.client.get(reverse('polls:detail', args=(question.id,) ))
        self.assertContains(response, question.question_text) 

    


    