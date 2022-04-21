import json
import os

from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase


def file_decorator(func):
    def wrapper(self, *args, **kwargs):
        if os.path.isfile('promo/result/result.json'):
            os.remove('promo/result/result.json')
            func(self, *args, **kwargs)
        else:
            func(self, *args, **kwargs)
    return wrapper


class CommandsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def check_result(self):
        path = 'promo/result/result.json'
        all_promo = 0
        all_group = 0
        with open(path, 'r') as r:
            json_check = json.load(r)
            for i in range(0, 3, 1):
                if list(json_check['promo'][i].keys())[0] == self.group[i]:
                    print("Json key %s are equal test key %s" % (list(json_check['promo'][i].keys())[0], self.group[i]))
                    all_group += 1
                else:
                    raise ValidationError("Invalid keys in Json file! Excepted %s but got %s" %
                                          (list(json_check['promo'][i].keys())[0], self.group[i]))
            for i in range(0, 3, 1):
                if len(json_check['promo'][i][self.group[i]]) == self.count[i]:
                    print("Json promo-code amount=%s, group=%s" % (self.count[i], self.group[i]))
                    all_promo += len(json_check['promo'][i][self.group[i]])
                else:
                    raise ValidationError("Invalid promo-code amount in Json group=%s! Excepted %s but got %s" %
                                          (self.group[i], self.count[i], len(json_check['promo'][0][self.group[i]])))
            print("Json all promo-code amount=%s and all group count=%s" % (all_promo, all_group))

    @file_decorator
    def test_custom_command(self):
        self.group = ['asdfvb', 'same', 'group1']
        self.count = [8, 3, 11]
        for i in range(0, 3, 1):
            args = [self.count[i], self.group[i]]
            opts = {}
            call_command('custom_command', *args, **opts)
        self.check_result()
