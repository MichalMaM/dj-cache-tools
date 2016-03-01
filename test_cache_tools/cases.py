from django.test import TestCase
from .utils import create_choice, create_question, create_extra_question


class CacheToolsTestCase(TestCase):
    def setUp(self):
        super(CacheToolsTestCase, self).setUp()
        self.question = create_question(self)
        self.extra_question = create_extra_question(self, self.question)
        self.choice = create_choice(self, self.question)
