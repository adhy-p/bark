from db import DatabaseManager
from typing import Dict
from datetime import datetime
import sys


dbm = DatabaseManager('bookmarks.db')


class CreateBookmarksTableCommand:
    def execute(self):
        dbm.create_table('bookmarks', {
            'id': 'integer primary key autoincrement',
            'title': 'text not null',
            'url': 'text not null',
            'notes': 'text',
            'date_added': 'text not null',
          })


class AddBookmarkCommand:
    def execute(self, columns: Dict[str, str]):
        columns['date_added'] = datetime.utcnow().isoformat()
        dbm.add('bookmarks', columns)
        return '200 OK added'


class ListBookmarkCommand:
    def __init__(self, order_by: str = 'date_added'):
        self.order_by = order_by

    def execute(self):
        return dbm.select('bookmarks', order_by=self.order_by).fetchall()


class DeleteBookmarkCommand:
    def execute(self, id: int):
        dbm.delete('bookmarks', {'id': id})
        return '200 OK deleted'


class QuitCommand:
    def execute(self):
        sys.exit()
