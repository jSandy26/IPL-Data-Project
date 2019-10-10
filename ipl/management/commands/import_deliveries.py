from ipl.models import Delivery
from django.core.management.base import BaseCommand
from django.db import transaction

class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **kwargs):
        # Since the CSV headers match the model fields,
        # you only need to provide the file's path (or a Python file object)
        insert_count = Delivery.objects.from_csv('/home/jsandy/django_projects/dataproject/deliveries.csv',drop_constraints=False, drop_indexes=False)
        print ("{} records inserted".format(insert_count))