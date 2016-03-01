from nose import tools

import django
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from utils import create_question, create_choice
from .models import Choice, Question, ExtraQuestion
from .cases import CacheToolsTestCase


class TestCachedForeignKey(CacheToolsTestCase):

    def test_foreign_key_is_cached(self):
        choice = Choice.objects.get(pk=self.choice.pk)

        with self.assertNumQueries(1):
            question = choice.question
        tools.assert_equals(question, self.question)

        with self.assertNumQueries(0):
            question = choice.question
        tools.assert_equals(question, self.question)

        choice = Choice.objects.get(pk=self.choice.pk)

        with self.assertNumQueries(0):
            question = choice.question
        tools.assert_equals(question, self.question)

    def test_foreign_key_reflect_changes(self):
        choice = Choice.objects.get(pk=self.choice.pk)

        with self.assertNumQueries(1):
            question = choice.question
        tools.assert_equals(question, self.question)

        with self.assertNumQueries(0):
            question = choice.question
        tools.assert_equals(question, self.question)

        choice = Choice.objects.get(pk=self.choice.pk)

        with self.assertNumQueries(0):
            question = choice.question
        tools.assert_equals(question, self.question)

        self.question.question_text = "3"
        self.question.save()

        choice = Choice.objects.get(pk=self.choice.pk)

        with self.assertNumQueries(1):
            question = choice.question
        tools.assert_equals(question.question_text, "3")

    def test_content_type_fk_is_cached(self):
        with self.assertNumQueries(2):
            question = create_question(self, content_type=ContentType.objects.get_for_model(User))

        with self.assertNumQueries(0):
            ct = question.content_type
        tools.assert_equals(ct, ContentType.objects.get_for_model(User))

        question = Question.objects.get(pk=question.pk)

        with self.assertNumQueries(0):
            ct = question.content_type
        tools.assert_equals(ct, ContentType.objects.get_for_model(User))

    def test_site_fk_is_cached(self):
        with self.assertNumQueries(1):
            question = create_question(self, question_text="hi all")

        with self.assertNumQueries(0):
            site = question.site
        tools.assert_equals(site, Site.objects.get_current())

        question = Question.objects.get(pk=question.pk)

        with self.assertNumQueries(2 if django.VERSION[:2] < (1, 8) else 0):
            site = question.site
        tools.assert_equals(site, Site.objects.get_current())


class TestCachedGenericForeignKey(CacheToolsTestCase):

    def test_foreign_key_is_cached(self):
        question = create_question(self, question_text="hi all!!!")
        choice = create_choice(self, self.question, related_ct=ContentType.objects.get_for_model(Question), related_id=question.pk)

        with self.assertNumQueries(1):
            related_question = choice.related
        tools.assert_equals(question, related_question)

        with self.assertNumQueries(0):
            related_question = choice.related
        tools.assert_equals(question, related_question)

        choice = Choice.objects.get(pk=choice.pk)

        with self.assertNumQueries(0):
            related_question = choice.related
        tools.assert_equals(question, related_question)

    def test_foreign_key_reflect_changes(self):
        question = create_question(self, question_text="hi all!!!")
        choice = create_choice(self, self.question, related_ct=ContentType.objects.get_for_model(Question), related_id=question.pk)

        with self.assertNumQueries(1):
            related_question = choice.related
        tools.assert_equals(question, related_question)

        with self.assertNumQueries(0):
            related_question = choice.related
        tools.assert_equals(question, related_question)

        choice = Choice.objects.get(pk=choice.pk)

        with self.assertNumQueries(0):
            related_question = choice.related
        tools.assert_equals(question, related_question)

        question.question_text = "5"
        question.save()

        choice = Choice.objects.get(pk=choice.pk)

        with self.assertNumQueries(1):
            related_question = choice.related
        tools.assert_equals(related_question.question_text, "5")


class TestCachedOneToOneField(CacheToolsTestCase):

    def test_foreign_key_is_cached(self):
        with self.assertNumQueries(1):
            extra_question = ExtraQuestion.objects.get(pk=self.extra_question.pk)

        with self.assertNumQueries(1):
            question = extra_question.question
        tools.assert_equals(question, self.question)

        with self.assertNumQueries(0):
            question = extra_question.question
        tools.assert_equals(question, self.question)

        extra_question = ExtraQuestion.objects.get(pk=self.extra_question.pk)

        with self.assertNumQueries(0):
            question = extra_question.question
        tools.assert_equals(question, self.question)

    def test_foreign_key_reflect_changes(self):
        with self.assertNumQueries(1):
            extra_question = ExtraQuestion.objects.get(pk=self.extra_question.pk)

        with self.assertNumQueries(1):
            question = extra_question.question
        tools.assert_equals(question, self.question)

        with self.assertNumQueries(0):
            question = extra_question.question
        tools.assert_equals(question, self.question)

        extra_question = ExtraQuestion.objects.get(pk=self.extra_question.pk)

        with self.assertNumQueries(0):
            question = extra_question.question
        tools.assert_equals(question, self.question)

        self.question.question_text = "3"
        self.question.save()

        extra_question = ExtraQuestion.objects.get(pk=self.extra_question.pk)

        with self.assertNumQueries(1):
            question = extra_question.question
        tools.assert_equals(question.question_text, "3")
