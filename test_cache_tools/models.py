from __future__ import unicode_literals

from django.db import models

from cache_tools.fields import (
    CachedForeignKey,
    SiteForeignKey,
    ContentTypeForeignKey,
    CachedGenericForeignKey,
    CachedOneToOneField,
)


class Question(models.Model):
    site = SiteForeignKey(verbose_name='Site', on_delete=models.CASCADE)
    content_type = ContentTypeForeignKey(on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class ExtraQuestion(models.Model):
    question = CachedOneToOneField(Question, on_delete=models.CASCADE)
    extra_text = models.CharField(max_length=200, default="Yes")


class Choice(models.Model):
    related_ct = ContentTypeForeignKey(on_delete=models.CASCADE)
    related_id = models.IntegerField()
    related = CachedGenericForeignKey('related_ct', 'related_id')

    question = CachedForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
