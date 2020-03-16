"""we're going to have a management command to the core
out of our django project the management command is going to be
a help of command allows us to wait for the database
to be available before continue in and running other commands
We're going to use this command in our docker a composed file when
starting our Django app The reason that we need this command is
because I find that sometimes when using Postgres with
Doc composed in a Django app sometimes the django out fails
to start because of a database error It turns out that this is
because once the postgres services started there were a few
some extra set up tasks that need to be done on the postgres
before is ready to accept connections So what this means is an
Django app will try and connect to our database before the
database is ready and therefore it will fail with an exception
We're going to add this helper command that we can put in
front of all of the commands we run in docker complies and that
will ensure that a database is up and ready to accept connections
Before we try and access the database This will make our
application a lot more reliable when running
"""

# testing using mocking is a way to know
# if the function got called and how many times it did
# we pass the function to the patch class and then
# we get an object with all the needed info and we can add
# side effect to the calling
from unittest.mock import patch
# for calling the command that's gonna handle the db waiting
from django.core.management import call_command
# an error from the db we use it to know
# how to act when we get it
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTest(TestCase):

    # test that the command wait_for_db is exist and callable
    def test_wait_for_db_ready(self):
        # this function get called every time we try to get
        # an item from the db so we simulating this behavior
        # by calling the func and mock it up using patch()
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            # defining the return value
            gi.return_value = True
            # calling the command
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    # using patch this way will work exactly like using it normally
    # but this way short the code and pass the patch object to the
    # method as an argument
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            # making the func return a OperationalError for 5 times
            # and make sure that the command handles it
            # and then we pass true
            gi.side_effect = [OperationalError] * 5 + [True]
            # calling the command
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
