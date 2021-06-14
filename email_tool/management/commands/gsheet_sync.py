import json
import orjson

from email_tool.models import Customer

# TODO:
# Monkey patch Django Gsheets to use a serializer that can handle UUID
# and datetimes necessary for syncing
# This will be fixed eventually
json.dumps = orjson.dumps
json.loads = orjson.loads

from gsheets.management.commands.syncgsheets import Command as SyncGsheetsCommand  # noqa


class Command(SyncGsheetsCommand):
    def find_syncable_models(self):
        """Overloads the base class implementation
        to implicitly control which models sync.
        """
        return [Customer]
