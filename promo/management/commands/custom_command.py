from django.core.management.base import BaseCommand
from promo.forms import PromoGenerationForm


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('amount', type=int, help=u'Кол-во кодов')
        parser.add_argument('group', type=str, help=u'Название группы')

    def handle(self, *args, **kwargs):
        count = kwargs['amount']
        group = kwargs['group']
        PromoGenerationForm(data={'group': group, 'count': count}).generate()
