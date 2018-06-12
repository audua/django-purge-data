import logging
import re
from distutils.util import strtobool

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone


class Command(BaseCommand):

    help = 'Purges the given model data in the given app based on the given criteria'

    # pylint: disable=no-self-use
    def add_arguments(self, parser):
        parser.add_argument('app_name_dot_model_name', help='the name of the app and the model')
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-a', '--all', action='store_true', help='purges all records')
        group.add_argument('-filter', '--filter', nargs='*', help='pass a filter to the model')

    # pylint: disable=unused-argument, no-self-use
    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)

        try:
            app_name, model_name = options['app_name_dot_model_name'].split('.')
        except ValueError:
            choices = ', '.join([app for app in apps.app_configs])
            logger.error(f"Enter the app name followed by a dot followed by the model name. "
                         f"Example purgedata.meter App choices are: {choices}")
            return

        try:
            model = apps.get_model(app_name, model_name)
        except LookupError:
            logger.error(f"{model_name} is not a valid model name or {app_name} is not a valid app name")
            return

        queryset = model.objects.all()

        if options['filter']:
            filters = ' '.join(options['filter'])
            filters = re.split(r'[, ]\s*(?=[^]]*(?:\[|$))', filters)  # splits commas and spaces not in lists
            filters = dict(item.split("=") for item in filters)

            truth_values = ['y', 'yes', 't', 'true', 'on', '1', 'n', 'no', 'f', 'false', 'off', '0']

            for field, val in filters.items():
                field_parts = field.split('__')
                field_ = model._meta.get_field(field_parts[0])  # pylint: disable=protected-access
                field_type = field_.get_internal_type()
                field_types = ['DateField', 'DateTimeField']
                is_bool = True
                if len(field_parts) > 1 and field_type in field_types and val.isdigit():
                    if set(field_.class_lookups.keys()).isdisjoint(set(field_parts[1:])):
                        time = timezone.now() - timezone.timedelta(days=int(val))
                        filters[field] = time
                        is_bool = False

                if isinstance(val, str):
                    if val.startswith('[') and val.endswith(']'):
                        filters[field] = re.split(r'[, ]\s*(?=[^]]*(?:\[|$))', val.lstrip('[').rstrip(']'))
                    elif val.lower() in truth_values and is_bool:
                        filters[field] = bool(strtobool(val))
            queryset = queryset.filter(Q(**filters))

        if queryset.exists():
            logger.info(f"purging {model_name} data: {queryset}")
            queryset.delete()