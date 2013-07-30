from optparse import make_option

from django.core.management.base import AppCommand


class Command(AppCommand):
    option_list = AppCommand.option_list + (make_option(
        '--err-stderr',
        action='store_true',
        dest='err',
        default=False,
        help='duplicate output to stderr'),)

    requires_model_validation = True
    help = 'Prints model names and objects count'
    #args = '[appname ...]'

    def handle_app(self, **options):
        from django.db.models import get_models

        for model in get_models():
            err = options.get('err')
            val = model.__name__ + \
                  " - %s objects" % model._default_manager.count()
            #if err:
            self.stdout.write(val)
            self.stderr.write('error:%s' % val)
            #else:
            #    self.stdout.write(val)
