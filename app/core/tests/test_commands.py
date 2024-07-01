from django.test import SimpleTestCase
from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError

class CommandsTests(SimpleTestCase):

    @patch('core.management.commands.checkdb.connection')
    def test_checkdb_ready(self, connection_mock):
        connection_mock.ensure_connection.return_value = True
        call_command('checkdb')
        self.assertTrue(connection_mock.ensure_connection.called)
        connection_mock.ensure_connection.assert_called_once()

    @patch('core.management.commands.checkdb.time')
    @patch('core.management.commands.checkdb.connection')
    def test_checkdb_not_ready(self, connection_mock, time_mock):
        # Raise a mocked exception, fail the ensure_connection by setting the side effect attribute to exception
        connection_mock.ensure_connection.side_effect = [OperationalError] * 6
        call_command('checkdb')
        self.assertEqual(6, connection_mock.ensure_connection.call_count)
        self.assertTrue(time_mock.sleep.called)
