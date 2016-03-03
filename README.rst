Django cache tools
##################

Django cache tools originally developed for `Ella CMS <https://github.com/ella/ella>`_.
It contains few helpful caching tools (such as cached ForeignKey, functions for caching object/objects, decorator for caching function/method, etc.)

Usage for models
****************

In models.py you can use `CachedForeignKey`::

    from __future__ import unicode_literals
    from django.db import models
    from cache_tools.fields import CachedForeignKey


    @python_2_unicode_compatible
    class Question(models.Model):
        question_text = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')

        def __str__(self):
            return self.question_text


    @python_2_unicode_compatible
    class Choice(models.Model):
        question = CachedForeignKey(Question, on_delete=models.CASCADE)
        choice_text = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)

        def __str__(self):
            return self.choice_text

Usage for caching function
**************************

In whatever.py you can use `cache_this`::

    from cache_tools.utils import cache_this
    from .models import Question


    @cache_this(lambda *args, **kwargs: 'my_app_all_questions_cache_key')
    def get_all_guestions():
        return list(Question.objects.all().order_by('pk'))

Build status
************

:Master branch:

  .. image:: https://secure.travis-ci.org/MichalMaM/dj-cache-tools.svg?branch=master
     :alt: Travis CI - Distributed build platform for the open source community
     :target: http://travis-ci.org/#!/MichalMaM/dj-cache-tools
