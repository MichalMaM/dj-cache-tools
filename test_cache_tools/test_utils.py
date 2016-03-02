from nose import tools

from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache

from cache_tools.utils import get_cached_objects, get_cached_object_or_404

from .models import Question
from .cases import CacheToolsTestCase
from .utils import (
    create_question,
    create_choice,
    get_cached_all_guestions,
)


class TestGetCachedObject404(CacheToolsTestCase):

    def test_object_by_pk_is_cached(self):
        model = Question
        question = create_question(self, question_text="question xxx")

        with self.assertNumQueries(1):
            obj = get_cached_object_or_404(model, pk=question.pk)
        tools.assert_equals(obj, question)

        with self.assertNumQueries(0):
            obj = get_cached_object_or_404(model, pk=question.pk)
        tools.assert_equals(obj, question)

    def test_object_by_pk_reflect_changes(self):
        model = Question
        question = create_question(self, question_text="question xxx")

        with self.assertNumQueries(1):
            obj = get_cached_object_or_404(model, pk=question.pk)
        tools.assert_equals(obj, question)

        with self.assertNumQueries(0):
            obj = get_cached_object_or_404(model, pk=question.pk)
        tools.assert_equals(obj, question)

        question.question_text = "X"
        question.save()

        with self.assertNumQueries(1):
            obj = get_cached_object_or_404(model, pk=question.pk)
        tools.assert_equals(obj.question_text, question.question_text)

    @tools.raises(Http404)
    def test_object_by_pk_raise_404(self):
        model = Question
        get_cached_object_or_404(model, pk=3456)


class TestGetCachedObjects(CacheToolsTestCase):

    def test_objects_are_cached_with_model(self):
        model = Question
        questions = [create_question(self, question_text="question %s" % i) for i in range(1, 5)]

        with self.assertNumQueries(1):
            objects = get_cached_objects(pks=[q.pk for q in questions], model=model)
        tools.assert_equals(objects, questions)

        with self.assertNumQueries(0):
            objects = get_cached_objects(pks=[q.pk for q in questions], model=model)
        tools.assert_equals(objects, questions)

    def test_objects_are_cached_without_model(self):
        questions = [create_question(self, question_text="question %s" % i) for i in range(1, 5)]
        choices = [create_choice(self, self.question, choice_text="choice %s" % i) for i in range(1, 5)]
        all_objects = questions + choices

        with self.assertNumQueries(2):
            objects = get_cached_objects(pks=[
                (ContentType.objects.get_for_model(o).pk, o.pk)
                for o in all_objects
            ])
        tools.assert_equals(objects, all_objects)

        with self.assertNumQueries(0):
            objects = get_cached_objects(pks=[
                (ContentType.objects.get_for_model(o).pk, o.pk)
                for o in all_objects
            ])
        tools.assert_equals(objects, all_objects)


class TestCacheTools(CacheToolsTestCase):

    def setUp(self):
        super(TestCacheTools, self).setUp()
        cache.clear()

    def test_result_is_cached(self):
        for i in range(1, 5):
            create_question(self, question_text="question %s" % i)

        all_questions = list(Question.objects.all().order_by('pk'))

        with self.assertNumQueries(1):
            cached_questions = get_cached_all_guestions()
        tools.assert_equals(cached_questions, all_questions)

        with self.assertNumQueries(0):
            cached_questions = get_cached_all_guestions()
        tools.assert_equals(cached_questions, all_questions)

    def test_result_does_not_reflect_changes(self):
        model = Question
        for i in range(1, 5):
            create_question(self, question_text="question %s" % i)

        all_questions = list(model.objects.all().order_by('pk'))

        with self.assertNumQueries(1):
            cached_questions = get_cached_all_guestions()
        tools.assert_equals(cached_questions, all_questions)

        with self.assertNumQueries(0):
            cached_questions = get_cached_all_guestions()
        tools.assert_equals(cached_questions, all_questions)

        create_question(self, question_text="question 7")
        all_questions_old = all_questions
        all_questions = list(model.objects.all().order_by('pk'))

        with self.assertNumQueries(0):
            cached_questions = get_cached_all_guestions()
        tools.assert_equals(cached_questions, all_questions_old)
        tools.assert_not_equals(cached_questions, all_questions)
        tools.assert_true(len(cached_questions), 6)
        tools.assert_true(len(all_questions), 7)
