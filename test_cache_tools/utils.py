from django.utils.timezone import now
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from cache_tools.utils import cache_this

from .models import Question, ExtraQuestion, Choice


def create_obj(model, defaults, commit=True, **kwargs):
    defaults.update(kwargs)
    obj = model(**defaults)
    if commit:
        obj.save()
    return obj


def create_question(test_case, **kwargs):
    defaults = dict(
        site=Site.objects.get_current(),
        content_type=ContentType.objects.get_for_model(Question),
        question_text="Test text question",
        pub_date=now(),
    )
    return create_obj(Question, defaults=defaults, **kwargs)


def create_extra_question(test_case, question, **kwargs):
    defaults = dict(
        question=question,
    )
    return create_obj(ExtraQuestion, defaults=defaults, **kwargs)


def create_choice(test_case, question, **kwargs):
    defaults = dict(
        related_ct=ContentType.objects.get_for_model(Question),
        related_id=question.pk,
        question=question,
        choice_text="Text choice",
    )
    return create_obj(Choice, defaults=defaults, **kwargs)


def get_all_guestions():
    return list(Question.objects.all().order_by('pk'))


@cache_this(lambda *args, **kwargs: 'test_all_questions')
def get_cached_all_guestions():
    return get_all_guestions()
