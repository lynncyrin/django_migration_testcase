from django.test import TransactionTestCase
from django.core.management import call_command


class BaseMigrationTestCase(TransactionTestCase):
    __abstract__ = True

    before = None
    after = None
    app_name = None

    def __init__(self, *args, **kwargs):
        super(BaseMigrationTestCase, self).__init__(*args, **kwargs)
        # if self.app_name is None, then assume self.before is a list
        # of 2-tuples. This is more explicit (and easier to document).
        # TODO: add more sanity checks
        if self.app_name:
            self.before = [(self.app_name, self.before)]
            self.after = [(self.app_name, self.after)]

    def tearDown(self):
        # We do need to tidy up and take the database to its final
        # state so that we don't get errors when the final truncating
        # happens.
        for app_name, _ in self.after:
            call_command('migrate', app_name,
                         verbosity=0, no_initial_data=True)
        super(BaseMigrationTestCase, self).tearDown()

    def get_model_before(self, model_name):
        raise NotImplementedError()

    def get_model_after(self, model_name):
        raise NotImplementedError()

    def run_migration(self):
        raise NotImplementedError()

    def _get_app_and_model_name(self, model_name):
        if '.' in model_name:
            app_name, model_name = model_name.split('.', 2)
        elif self.app_name:
            app_name = self.app_name
        else:
            raise ValueError('Must specify app name')
        return app_name, model_name