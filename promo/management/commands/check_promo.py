import os
import json

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('promo', type=str, help=u'Промо-код')

    def handle(self, *args, **kwargs):
        promo = kwargs['promo']
        i = 0
        found = False
        try:
            with open('promo/result/result.json', 'r') as r:
                promo_check = json.load(r)
                while i in range(len(promo_check["promo"])) and found is not True:
                    group = promo_check["promo"][i]
                    for key in group:
                        if promo not in group[key]:
                            found = False
                        else:
                            print('Promo-code found! Group=%s' % key)
                            found = True
                            break
                    i += 1
                if found is False:
                    print('Promo-code not found!')
        except OSError as e:
            print(e)

